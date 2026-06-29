const express = require('express');
const router = express.Router();
const gmailService = require('../services/gmailService');

// In-memory token store (replace with a DB or session store in production)
const tokenStore = new Map();

// GET /api/gmail/auth-url
// Returns the Google OAuth2 authorization URL
router.get('/auth-url', (req, res) => {
  try {
    const url = gmailService.getAuthUrl();
    res.json({ url });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/gmail/oauth/callback
// Handles OAuth2 callback, exchanges code for tokens
router.get('/oauth/callback', async (req, res) => {
  const { code, error } = req.query;

  if (error) {
    return res.redirect(`${process.env.FRONTEND_URL}?auth_error=${encodeURIComponent(error)}`);
  }

  try {
    const tokens = await gmailService.getTokensFromCode(code);
    const email = await gmailService.getUserEmail(tokens);

    // Store tokens keyed by email
    tokenStore.set(email, tokens);

    res.redirect(`${process.env.FRONTEND_URL}?auth_success=true&email=${encodeURIComponent(email)}`);
  } catch (err) {
    console.error('OAuth callback error:', err.message);
    res.redirect(`${process.env.FRONTEND_URL}?auth_error=${encodeURIComponent(err.message)}`);
  }
});

// POST /api/gmail/disconnect
// Removes stored tokens for a given email
router.post('/disconnect', (req, res) => {
  const { email } = req.body;
  if (email && tokenStore.has(email)) {
    tokenStore.delete(email);
  }
  res.json({ success: true });
});

// GET /api/gmail/status
// Returns whether the given email has stored tokens
router.get('/status', (req, res) => {
  const { email } = req.query;
  const connected = email ? tokenStore.has(email) : false;
  res.json({ connected, email: email || null });
});

// Export token store so other routes can access it
router.tokenStore = tokenStore;

module.exports = router;
