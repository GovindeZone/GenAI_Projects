const express = require('express');
const router = express.Router();
const gmailService = require('../services/gmailService');
const gmailRouter = require('./gmail');

function getTokens(email) {
  return gmailRouter.tokenStore.get(email);
}

// POST /api/emails/fetch
// Fetches emails from Gmail inbox with optional filters
router.post('/fetch', async (req, res) => {
  const {
    receiverEmail,
    senderFilter,
    dateFrom,
    dateTo,
    keyword,
    maxResults = 50,
  } = req.body;

  if (!receiverEmail) {
    return res.status(400).json({ error: 'receiverEmail is required' });
  }

  const tokens = getTokens(receiverEmail);
  if (!tokens) {
    return res.status(401).json({
      error: 'Not authenticated. Please connect Gmail first.',
      requiresAuth: true,
    });
  }

  try {
    const emails = await gmailService.fetchEmails(tokens, {
      receiverEmail,
      senderFilter,
      dateFrom,
      dateTo,
      keyword,
      maxResults,
    });
    res.json({ emails, count: emails.length });
  } catch (err) {
    console.error('Email fetch error:', err.message);
    if (err.message?.includes('invalid_grant') || err.message?.includes('Token')) {
      gmailRouter.tokenStore.delete(receiverEmail);
      return res.status(401).json({
        error: 'Gmail session expired. Please reconnect.',
        requiresAuth: true,
      });
    }
    res.status(500).json({ error: err.message });
  }
});

// POST /api/emails/send
// Sends an email reply via Gmail
router.post('/send', async (req, res) => {
  const { receiverEmail, to, subject, body, threadId } = req.body;

  if (!receiverEmail || !to || !subject || !body) {
    return res.status(400).json({ error: 'receiverEmail, to, subject, and body are required' });
  }

  const tokens = getTokens(receiverEmail);
  if (!tokens) {
    return res.status(401).json({ error: 'Not authenticated', requiresAuth: true });
  }

  try {
    const result = await gmailService.sendEmail(tokens, { to, subject, body, replyToMessageId: threadId });
    res.json({ success: true, messageId: result.id });
  } catch (err) {
    console.error('Send email error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
