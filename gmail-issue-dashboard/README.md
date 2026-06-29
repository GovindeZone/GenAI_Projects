# Gmail Issue Automation Dashboard

A full-stack SaaS dashboard that reads your Gmail inbox, uses Claude AI to classify and analyze issue-related emails, and automates professional email responses.

## Features

- **Gmail OAuth2** — Secure Google authentication (no password stored)
- **AI Email Analysis** — Claude categorizes emails as New Ticket / In-Progress / Resolved / Escalation
- **Smart Filtering** — Filter by category, priority, sender, date, keyword
- **Auto-Reply Generation** — AI drafts professional replies per category
- **Escalation Emails** — AI generates full escalation emails with context
- **Manual Review** — Edit drafts before sending; no auto-send
- **CSV Export** — Download filtered results

## Quick Start

### 1. Clone / open the project

```
D:\genai_projects\gmail-issue-dashboard\
```

### 2. Configure backend credentials

```bash
cd backend
copy .env.example .env
# Edit .env with your credentials (see below)
```

### 3. Set up Google OAuth2

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project → **APIs & Services** → **Enable Gmail API**
3. **Credentials** → **Create OAuth 2.0 Client ID** (Web application)
4. Add `http://localhost:5000/api/gmail/oauth/callback` as an Authorized Redirect URI
5. Copy Client ID and Secret into `backend/.env`

### 4. Get Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Create an API key
3. Paste into `backend/.env` as `ANTHROPIC_API_KEY`

### 5. Start the app

**Windows (double-click):**
```
start.bat
```

**Manual:**
```bash
# Terminal 1 — Backend
cd backend && npm install && npm run dev

# Terminal 2 — Frontend
cd frontend && npm run dev
```

Open **http://localhost:5173**

## Project Structure

```
gmail-issue-dashboard/
├── backend/
│   ├── src/
│   │   ├── server.js               # Express app entry point
│   │   ├── routes/
│   │   │   ├── gmail.js            # OAuth2 flow, token management
│   │   │   ├── emails.js           # Fetch & send Gmail messages
│   │   │   └── analyze.js          # AI analysis & reply generation
│   │   └── services/
│   │       ├── gmailService.js     # Gmail API wrapper
│   │       └── aiService.js        # Claude AI integration
│   └── .env.example
├── frontend/
│   └── src/
│       ├── App.tsx                 # Root app, state management
│       ├── types/index.ts          # TypeScript interfaces
│       ├── services/api.ts         # Axios API client
│       ├── components/
│       │   ├── Sidebar/            # Navigation sidebar
│       │   ├── Dashboard/          # Stats cards & overview
│       │   ├── EmailTable/         # Issues table
│       │   ├── EmailDetail/        # Detail modal + reply/escalation
│       │   └── Filters/            # Filter bar
│       └── pages/
│           ├── EmailsPage.tsx      # Email queue page
│           └── SettingsPage.tsx    # Config & OAuth connect
└── start.bat                       # One-click launcher (Windows)
```

## Environment Variables (backend/.env)

| Variable | Description |
|---|---|
| `GOOGLE_CLIENT_ID` | Google OAuth2 Client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth2 Client Secret |
| `GOOGLE_REDIRECT_URI` | `http://localhost:5000/api/gmail/oauth/callback` |
| `ANTHROPIC_API_KEY` | Claude AI API key |
| `PORT` | Backend port (default: 5000) |
| `FRONTEND_URL` | Frontend URL (default: http://localhost:5173) |
