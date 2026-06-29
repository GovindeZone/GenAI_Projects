const express = require('express');
const router = express.Router();
const aiService = require('../services/aiService');

// POST /api/analyze/emails
// Analyzes an array of emails using AI and returns enriched data
router.post('/emails', async (req, res) => {
  const { emails } = req.body;

  if (!emails || !Array.isArray(emails)) {
    return res.status(400).json({ error: 'emails array is required' });
  }

  try {
    const results = await Promise.all(
      emails.map(async (email) => {
        try {
          const analysis = await aiService.analyzeEmail(email);
          return { ...email, analysis, analyzed: true };
        } catch (err) {
          console.error(`Analysis failed for email ${email.id}:`, err.message);
          return {
            ...email,
            analysis: {
              isIssueRelated: true,
              category: 'New Ticket',
              priority: 'Medium',
              summary: email.snippet || 'Analysis unavailable',
              keyPoints: [],
              suggestedAction: 'Review manually',
              sentiment: 'Neutral',
              topic: 'General',
            },
            analyzed: false,
          };
        }
      })
    );

    // Only return issue-related emails
    const issueEmails = results.filter((e) => e.analysis.isIssueRelated);

    const stats = {
      total: issueEmails.length,
      newTicket: issueEmails.filter((e) => e.analysis.category === 'New Ticket').length,
      inProgress: issueEmails.filter((e) => e.analysis.category === 'In-Progress').length,
      resolved: issueEmails.filter((e) => e.analysis.category === 'Resolved').length,
      escalation: issueEmails.filter((e) => e.analysis.category === 'Escalation').length,
    };

    res.json({ emails: issueEmails, stats });
  } catch (err) {
    console.error('Analyze error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// POST /api/analyze/generate-reply
// Generates an AI email reply draft
router.post('/generate-reply', async (req, res) => {
  const { email, analysis, companyName, assignerEmail, category } = req.body;

  if (!email || !companyName) {
    return res.status(400).json({ error: 'email and companyName are required' });
  }

  try {
    const reply = await aiService.generateReply(
      email,
      analysis,
      companyName,
      assignerEmail,
      category || analysis?.category || 'New Ticket'
    );
    res.json({ reply });
  } catch (err) {
    console.error('Generate reply error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// POST /api/analyze/generate-escalation
// Generates an AI escalation email draft
router.post('/generate-escalation', async (req, res) => {
  const { email, analysis, companyName, escalationEmail, assignerEmail } = req.body;

  if (!email || !companyName || !escalationEmail) {
    return res.status(400).json({ error: 'email, companyName, and escalationEmail are required' });
  }

  try {
    const escalationDraft = await aiService.generateEscalationEmail(
      email,
      analysis,
      companyName,
      escalationEmail,
      assignerEmail
    );
    res.json({ escalationDraft });
  } catch (err) {
    console.error('Generate escalation error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
