import { useState, useEffect, useCallback } from 'react';
import Sidebar from './components/Sidebar/Sidebar';
import DashboardPage from './components/Dashboard/DashboardPage';
import EmailsPage from './pages/EmailsPage';
import SettingsPage from './pages/SettingsPage';
import { gmailApi, emailsApi, analyzeApi } from './services/api';
import type { Email, AppConfig, DashboardStats, FilterState } from './types';

const DEFAULT_CONFIG: AppConfig = {
  receiverEmail: '',
  assignerEmail: '',
  escalationEmail: '',
  companyName: '',
};

const DEFAULT_STATS: DashboardStats = {
  total: 0, newTicket: 0, inProgress: 0, resolved: 0, escalation: 0,
};

const STORAGE_KEY = 'gmail_dashboard_config';

export default function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const [config, setConfig] = useState<AppConfig>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? { ...DEFAULT_CONFIG, ...JSON.parse(stored) } : DEFAULT_CONFIG;
    } catch { return DEFAULT_CONFIG; }
  });
  const [connected, setConnected] = useState(false);
  const [connectedEmail, setConnectedEmail] = useState('');
  const [emails, setEmails] = useState<Email[]>([]);
  const [stats, setStats] = useState<DashboardStats>(DEFAULT_STATS);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');

  // Check auth status on load and handle OAuth callback
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const authSuccess = params.get('auth_success');
    const authEmail = params.get('email');
    const authError = params.get('auth_error');

    if (authSuccess && authEmail) {
      const decoded = decodeURIComponent(authEmail);
      setConnected(true);
      setConnectedEmail(decoded);
      // Update config with connected email if not set
      setConfig((c) => ({ ...c, receiverEmail: c.receiverEmail || decoded }));
      window.history.replaceState({}, '', '/');
    } else if (authError) {
      setError(`OAuth error: ${decodeURIComponent(authError)}`);
      window.history.replaceState({}, '', '/');
    } else if (config.receiverEmail) {
      // Check existing connection
      gmailApi.getStatus(config.receiverEmail)
        .then((res) => {
          setConnected(res.data.connected);
          if (res.data.connected) setConnectedEmail(res.data.email || config.receiverEmail);
        })
        .catch(() => {});
    }
  }, []);

  function saveConfig(newConfig: AppConfig) {
    setConfig(newConfig);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newConfig));
  }

  const fetchAndAnalyze = useCallback(async (filterOverrides: Partial<FilterState> = {}) => {
    if (!config.receiverEmail) {
      setError('Please configure the Receiver Email in Settings first.');
      setActivePage('settings');
      return;
    }
    if (!connected) {
      setError('Please connect your Gmail account in Settings first.');
      setActivePage('settings');
      return;
    }

    setLoading(true);
    setError('');
    try {
      // Step 1: Fetch raw emails
      const fetchRes = await emailsApi.fetch({ ...config, ...filterOverrides, maxResults: 50 });
      const rawEmails = fetchRes.data.emails;

      if (rawEmails.length === 0) {
        setEmails([]);
        setStats(DEFAULT_STATS);
        return;
      }

      // Step 2: Analyze with AI (batched in groups of 10 to avoid timeouts)
      const BATCH = 10;
      let allAnalyzed: Email[] = [];
      let combinedStats = { ...DEFAULT_STATS };

      for (let i = 0; i < rawEmails.length; i += BATCH) {
        const batch = rawEmails.slice(i, i + BATCH);
        const analyzeRes = await analyzeApi.analyzeEmails(batch);
        allAnalyzed = [...allAnalyzed, ...analyzeRes.data.emails];
        const s = analyzeRes.data.stats;
        combinedStats = {
          total: combinedStats.total + s.total,
          newTicket: combinedStats.newTicket + s.newTicket,
          inProgress: combinedStats.inProgress + s.inProgress,
          resolved: combinedStats.resolved + s.resolved,
          escalation: combinedStats.escalation + s.escalation,
        };
      }

      setEmails(allAnalyzed);
      setStats(combinedStats);
    } catch (err: any) {
      const msg = err.response?.data?.error || err.message || 'Failed to fetch emails';
      setError(msg);
      if (err.response?.data?.requiresAuth) {
        setConnected(false);
        setConnectedEmail('');
      }
    } finally {
      setLoading(false);
    }
  }, [config, connected]);

  // Auto-fetch when connected and config is ready
  useEffect(() => {
    if (connected && config.receiverEmail) {
      fetchAndAnalyze();
    }
  }, [connected]);

  function handleFilterCategory(cat: string) {
    setCategoryFilter(cat);
  }

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar activePage={activePage} onNavigate={setActivePage} connected={connected} />

      <main className="ml-64 flex-1 p-6 min-w-0">
        {error && (
          <div className="mb-4 p-4 bg-red-950/50 border border-red-800/50 rounded-xl text-red-400 text-sm flex items-start justify-between gap-3">
            <span>{error}</span>
            <button onClick={() => setError('')} className="shrink-0 text-red-600 hover:text-red-400">✕</button>
          </div>
        )}

        {activePage === 'dashboard' && (
          <DashboardPage
            stats={stats}
            emails={emails}
            onFilterCategory={handleFilterCategory}
            onNavigateToEmails={() => setActivePage('emails')}
          />
        )}

        {activePage === 'emails' && (
          <EmailsPage
            emails={emails}
            config={config}
            loading={loading}
            onRefresh={fetchAndAnalyze}
            initialCategoryFilter={categoryFilter}
          />
        )}

        {activePage === 'settings' && (
          <SettingsPage
            config={config}
            connected={connected}
            connectedEmail={connectedEmail}
            onSave={saveConfig}
            onConnectionChange={(c, e) => { setConnected(c); setConnectedEmail(e); }}
          />
        )}
      </main>
    </div>
  );
}
