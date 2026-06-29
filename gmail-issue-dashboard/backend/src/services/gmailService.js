const { google } = require('googleapis');

// ============================================================
// Gmail OAuth2 client setup
// Configure GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and
// GOOGLE_REDIRECT_URI in your .env file
// ============================================================
function createOAuthClient() {
  return new google.auth.OAuth2(
    process.env.GOOGLE_CLIENT_ID,
    process.env.GOOGLE_CLIENT_SECRET,
    process.env.GOOGLE_REDIRECT_URI
  );
}

function getAuthUrl() {
  const oauth2Client = createOAuthClient();
  return oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: [
      'https://www.googleapis.com/auth/gmail.readonly',
      'https://www.googleapis.com/auth/gmail.send',
      'https://www.googleapis.com/auth/userinfo.email',
    ],
    prompt: 'consent',
  });
}

async function getTokensFromCode(code) {
  const oauth2Client = createOAuthClient();
  const { tokens } = await oauth2Client.getToken(code);
  return tokens;
}

async function getGmailClient(tokens) {
  const oauth2Client = createOAuthClient();
  oauth2Client.setCredentials(tokens);
  return google.gmail({ version: 'v1', auth: oauth2Client });
}

// Issue-related keywords for filtering emails
const ISSUE_KEYWORDS = [
  'issue', 'problem', 'error', 'bug', 'complaint', 'request', 'support',
  'help', 'urgent', 'critical', 'follow up', 'follow-up', 'pending',
  'delay', 'delayed', 'escalat', 'not working', 'broken', 'failed',
  'failure', 'incident', 'ticket', 'case', 'concern', 'resolve', 'fix',
];

function buildSearchQuery(receiverEmail, options = {}) {
  const parts = [];

  if (options.senderFilter) {
    parts.push(`from:${options.senderFilter}`);
  }

  if (options.dateFrom) {
    const d = new Date(options.dateFrom);
    parts.push(`after:${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()}`);
  }
  if (options.dateTo) {
    const d = new Date(options.dateTo);
    parts.push(`before:${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()}`);
  }

  if (options.keyword) {
    parts.push(`"${options.keyword}"`);
  }

  // Default: fetch all emails; AI does the issue classification
  return parts.length > 0 ? parts.join(' ') : 'in:inbox';
}

function decodeBase64(data) {
  return Buffer.from(data.replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('utf-8');
}

function extractBodyFromParts(parts) {
  if (!parts) return '';
  for (const part of parts) {
    if (part.mimeType === 'text/plain' && part.body?.data) {
      return decodeBase64(part.body.data);
    }
    if (part.parts) {
      const nested = extractBodyFromParts(part.parts);
      if (nested) return nested;
    }
  }
  // Fallback to HTML part
  for (const part of parts) {
    if (part.mimeType === 'text/html' && part.body?.data) {
      return decodeBase64(part.body.data).replace(/<[^>]+>/g, ' ');
    }
  }
  return '';
}

function parseEmailMessage(message) {
  const headers = message.payload?.headers || [];
  const getHeader = (name) =>
    headers.find((h) => h.name.toLowerCase() === name.toLowerCase())?.value || '';

  const subject = getHeader('Subject');
  const from = getHeader('From');
  const date = getHeader('Date');
  const to = getHeader('To');
  const messageId = getHeader('Message-ID');

  let body = '';
  if (message.payload?.body?.data) {
    body = decodeBase64(message.payload.body.data);
  } else if (message.payload?.parts) {
    body = extractBodyFromParts(message.payload.parts);
  }

  // Extract sender name and email
  const fromMatch = from.match(/^(.*?)\s*<(.+?)>$/) || [null, from, from];
  const senderName = fromMatch[1]?.trim() || from;
  const senderEmail = fromMatch[2]?.trim() || from;

  return {
    id: message.id,
    threadId: message.threadId,
    messageId,
    subject,
    from,
    senderName,
    senderEmail,
    to,
    date: new Date(date).toISOString(),
    snippet: message.snippet || '',
    body: body.substring(0, 3000), // Limit body for AI analysis
    labelIds: message.labelIds || [],
  };
}

async function fetchEmails(tokens, options = {}) {
  const gmail = await getGmailClient(tokens);
  const query = buildSearchQuery(options.receiverEmail, options);

  const listResponse = await gmail.users.messages.list({
    userId: 'me',
    q: query,
    maxResults: options.maxResults || 50,
  });

  const messages = listResponse.data.messages || [];
  if (messages.length === 0) return [];

  // Fetch full details for each message
  const emailDetails = await Promise.all(
    messages.map(async (msg) => {
      try {
        const detail = await gmail.users.messages.get({
          userId: 'me',
          id: msg.id,
          format: 'full',
        });
        return parseEmailMessage(detail.data);
      } catch (err) {
        console.error(`Failed to fetch message ${msg.id}:`, err.message);
        return null;
      }
    })
  );

  return emailDetails.filter(Boolean);
}

async function sendEmail(tokens, { to, subject, body, replyToMessageId }) {
  const gmail = await getGmailClient(tokens);

  const rawMessage = [
    `To: ${to}`,
    `Subject: ${subject}`,
    'Content-Type: text/plain; charset=utf-8',
    '',
    body,
  ].join('\r\n');

  const encoded = Buffer.from(rawMessage)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');

  const sendParams = {
    userId: 'me',
    requestBody: { raw: encoded },
  };

  if (replyToMessageId) {
    sendParams.requestBody.threadId = replyToMessageId;
  }

  const result = await gmail.users.messages.send(sendParams);
  return result.data;
}

async function getUserEmail(tokens) {
  const oauth2Client = createOAuthClient();
  oauth2Client.setCredentials(tokens);
  const oauth2 = google.oauth2({ version: 'v2', auth: oauth2Client });
  const info = await oauth2.userinfo.get();
  return info.data.email;
}

module.exports = {
  getAuthUrl,
  getTokensFromCode,
  fetchEmails,
  sendEmail,
  getUserEmail,
};
