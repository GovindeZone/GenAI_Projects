const Anthropic = require('@anthropic-ai/sdk');

// ============================================================
// Configure ANTHROPIC_API_KEY in your .env file
// Get your key at: https://console.anthropic.com/
// ============================================================
const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

const CATEGORY_VALUES = ['New Ticket', 'In-Progress', 'Resolved', 'Escalation'];
const PRIORITY_VALUES = ['Critical', 'High', 'Medium', 'Low'];

async function analyzeEmail(email) {
  const prompt = `You are an expert IT support and customer service analyst. Analyze the following email and extract structured information.

Email Details:
- From: ${email.senderName} <${email.senderEmail}>
- Subject: ${email.subject}
- Date: ${email.date}
- Body: ${email.body || email.snippet}

Analyze this email and respond with ONLY valid JSON (no markdown, no explanation) in this exact format:
{
  "isIssueRelated": true/false,
  "category": "New Ticket" | "In-Progress" | "Resolved" | "Escalation",
  "priority": "Critical" | "High" | "Medium" | "Low",
  "summary": "2-3 sentence summary of the issue",
  "keyPoints": ["point1", "point2"],
  "suggestedAction": "recommended next action",
  "sentiment": "Positive" | "Neutral" | "Negative" | "Urgent",
  "topic": "brief topic tag (e.g. Technical Issue, Billing, Access Request, Bug Report)"
}

Rules:
- isIssueRelated: true if the email is about a problem, complaint, request, bug, support need, follow-up, escalation, or any work item requiring action.
- category rules:
  * New Ticket: fresh issue, first contact, new request
  * In-Progress: follow-up, status check, reminder on existing issue
  * Resolved: confirmation of fix, thank you, issue closed
  * Escalation: urgent/critical, unresolved after time, mentions manager/escalate/frustrated
- priority rules:
  * Critical: system down, data loss, security breach, very urgent language
  * High: significant impact, strong urgency, deadline mentioned
  * Medium: moderate impact, standard support request
  * Low: minor issue, general inquiry, FYI
`;

  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-6',
    max_tokens: 600,
    messages: [{ role: 'user', content: prompt }],
  });

  const text = response.content[0].text.trim();

  try {
    const parsed = JSON.parse(text);
    return {
      isIssueRelated: parsed.isIssueRelated ?? true,
      category: CATEGORY_VALUES.includes(parsed.category) ? parsed.category : 'New Ticket',
      priority: PRIORITY_VALUES.includes(parsed.priority) ? parsed.priority : 'Medium',
      summary: parsed.summary || email.snippet,
      keyPoints: parsed.keyPoints || [],
      suggestedAction: parsed.suggestedAction || 'Review and respond',
      sentiment: parsed.sentiment || 'Neutral',
      topic: parsed.topic || 'General',
    };
  } catch {
    // Fallback if AI returns malformed JSON
    return {
      isIssueRelated: true,
      category: 'New Ticket',
      priority: 'Medium',
      summary: email.snippet || 'Unable to analyze email.',
      keyPoints: [],
      suggestedAction: 'Review manually',
      sentiment: 'Neutral',
      topic: 'General',
    };
  }
}

async function generateReply(email, analysis, companyName, assignerEmail, category) {
  const templates = {
    'New Ticket': `acknowledgment email confirming ticket creation and that the team will respond within SLA`,
    'In-Progress': `update email informing the sender that their issue is actively being worked on`,
    'Resolved': `resolution email confirming the issue has been resolved and asking for feedback`,
    'Escalation': `escalation acknowledgment email expressing urgency and that senior team is handling it`,
  };

  const prompt = `You are a professional customer support agent at ${companyName}.
Write a ${templates[category] || templates['New Ticket']} for the following email.

Original Email:
- From: ${email.senderName} <${email.senderEmail}>
- Subject: ${email.subject}
- Summary: ${analysis.summary}
- Priority: ${analysis.priority}
- Assigned To: ${assignerEmail}

Requirements:
- Professional, empathetic tone
- Include ticket reference (use the email ID: ${email.id.substring(0, 8).toUpperCase()})
- Sign off as "${companyName} Support Team"
- Keep it concise (3-5 paragraphs max)
- Do NOT include subject line in the body
- Plain text only, no markdown

Write only the email body:`;

  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-6',
    max_tokens: 500,
    messages: [{ role: 'user', content: prompt }],
  });

  return response.content[0].text.trim();
}

async function generateEscalationEmail(email, analysis, companyName, escalationEmail, assignerEmail) {
  const prompt = `You are a professional support manager at ${companyName}.
Write an internal escalation email to the escalation team.

Issue Details:
- Original Sender: ${email.senderName} <${email.senderEmail}>
- Subject: ${email.subject}
- Date Received: ${new Date(email.date).toLocaleDateString()}
- Priority: ${analysis.priority}
- Issue Summary: ${analysis.summary}
- Key Points: ${analysis.keyPoints.join('; ')}
- Sentiment: ${analysis.sentiment}
- Current Handler: ${assignerEmail}
- Escalation Recipient: ${escalationEmail}

Write a formal escalation email that includes:
1. Subject (on first line as "Subject: ...")
2. Issue summary and background
3. Reason for escalation
4. Impact assessment
5. Recommended next action
6. Timeline expectation
7. Sign off as "${companyName} Support Management"

Plain text only:`;

  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-6',
    max_tokens: 600,
    messages: [{ role: 'user', content: prompt }],
  });

  return response.content[0].text.trim();
}

module.exports = { analyzeEmail, generateReply, generateEscalationEmail };
