import { useState } from 'react';
import { Save, Link, Unlink, ExternalLink, Info } from 'lucide-react';
import { gmailApi } from '../services/api';
import type { AppConfig } from '../types';

interface SettingsPageProps {
  config: AppConfig;
  connected: boolean;
  connectedEmail: string;
  onSave: (config: AppConfig) => void;
  onConnectionChange: (connected: boolean, email: string) => void;
}

export default function SettingsPage({ config, connected, connectedEmail, onSave, onConnectionChange }: SettingsPageProps) {
  const [form, setForm] = useState<AppConfig>(config);
  const [saved, setSaved] = useState(false);
  const [disconnecting, setDisconnecting] = useState(false);

  const set = (key: keyof AppConfig, value: string) => setForm((f) => ({ ...f, [key]: value }));

  function handleSave() {
    onSave(form);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  }

  async function handleConnect() {
    try {
      const res = await gmailApi.getAuthUrl();
      window.open(res.data.url, '_blank', 'width=600,height=700');
    } catch (err) {
      console.error('Failed to get auth URL:', err);
    }
  }

  async function handleDisconnect() {
    setDisconnecting(true);
    try {
      await gmailApi.disconnect(connectedEmail);
      onConnectionChange(false, '');
    } catch (err) {
      console.error('Disconnect error:', err);
    } finally {
      setDisconnecting(false);
    }
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Settings</h1>
        <p className="text-slate-400 text-sm mt-1">Configure your Gmail connection and automation preferences</p>
      </div>

      {/* Gmail Connection Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h2 className="text-base font-semibold text-white mb-1">Gmail Connection</h2>
        <p className="text-slate-500 text-xs mb-4">Authenticate with Google OAuth2 to read and send emails.</p>

        {connected ? (
          <div className="flex items-center justify-between p-4 bg-emerald-950/40 border border-emerald-800/40 rounded-lg">
            <div className="flex items-center gap-3">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
              <div>
                <p className="text-sm font-medium text-emerald-300">Connected</p>
                <p className="text-xs text-slate-400">{connectedEmail}</p>
              </div>
            </div>
            <button
              onClick={handleDisconnect}
              disabled={disconnecting}
              className="flex items-center gap-2 px-3 py-1.5 text-sm text-red-400 hover:text-red-300 bg-red-950/40 hover:bg-red-900/40 border border-red-800/40 rounded-lg transition-colors"
            >
              <Unlink className="w-3.5 h-3.5" />
              {disconnecting ? 'Disconnecting...' : 'Disconnect'}
            </button>
          </div>
        ) : (
          <div>
            <div className="flex items-start gap-2 p-3 bg-slate-800/50 border border-slate-700 rounded-lg mb-3 text-xs text-slate-400">
              <Info className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
              <p>
                Click "Connect Gmail" to open Google's OAuth2 authorization page.
                After granting access, you'll be redirected back automatically.
                Make sure <code className="text-indigo-300">GOOGLE_CLIENT_ID</code> and <code className="text-indigo-300">GOOGLE_CLIENT_SECRET</code> are set in the backend <code className="text-indigo-300">.env</code> file.
              </p>
            </div>
            <button
              onClick={handleConnect}
              className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium rounded-lg transition-colors"
            >
              <Link className="w-4 h-4" />
              Connect Gmail
              <ExternalLink className="w-3.5 h-3.5 opacity-60" />
            </button>
          </div>
        )}
      </div>

      {/* Configuration Form */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <h2 className="text-base font-semibold text-white">Inbox Configuration</h2>

        {[
          {
            key: 'receiverEmail' as const,
            label: 'Receiver Email',
            placeholder: 'inbox@yourcompany.com',
            help: 'The Gmail inbox to read and analyze.',
          },
          {
            key: 'assignerEmail' as const,
            label: 'Assigner Email',
            placeholder: 'support@yourcompany.com',
            help: 'Responsible team/person for handling issues.',
          },
          {
            key: 'escalationEmail' as const,
            label: 'Escalation Email',
            placeholder: 'manager@yourcompany.com',
            help: 'Where escalation emails will be sent.',
          },
          {
            key: 'companyName' as const,
            label: 'Company Name',
            placeholder: 'Acme Corporation',
            help: 'Used in auto-generated email signatures.',
          },
        ].map(({ key, label, placeholder, help }) => (
          <div key={key}>
            <label className="block text-sm font-medium text-slate-300 mb-1">{label}</label>
            <input
              type={key === 'companyName' ? 'text' : 'email'}
              value={form[key]}
              onChange={(e) => set(key, e.target.value)}
              placeholder={placeholder}
              className="w-full px-3 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
            />
            <p className="text-xs text-slate-500 mt-1">{help}</p>
          </div>
        ))}

        <button
          onClick={handleSave}
          className={`flex items-center gap-2 px-5 py-2.5 text-sm font-medium rounded-lg transition-all ${
            saved
              ? 'bg-emerald-700 text-white'
              : 'bg-indigo-600 hover:bg-indigo-500 text-white'
          }`}
        >
          <Save className="w-4 h-4" />
          {saved ? 'Saved!' : 'Save Settings'}
        </button>
      </div>

      {/* API Keys Info */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h2 className="text-base font-semibold text-white mb-3">API Configuration</h2>
        <div className="space-y-2 text-xs text-slate-400">
          <div className="flex items-center gap-2 p-3 bg-slate-800/50 rounded-lg font-mono">
            <span className="text-indigo-400">GOOGLE_CLIENT_ID</span>
            <span className="text-slate-600">—</span>
            <span>Google OAuth2 client ID from Google Cloud Console</span>
          </div>
          <div className="flex items-center gap-2 p-3 bg-slate-800/50 rounded-lg font-mono">
            <span className="text-indigo-400">GOOGLE_CLIENT_SECRET</span>
            <span className="text-slate-600">—</span>
            <span>Google OAuth2 client secret</span>
          </div>
          <div className="flex items-center gap-2 p-3 bg-slate-800/50 rounded-lg font-mono">
            <span className="text-indigo-400">ANTHROPIC_API_KEY</span>
            <span className="text-slate-600">—</span>
            <span>Claude AI API key from console.anthropic.com</span>
          </div>
          <p className="text-slate-500 pt-2">
            Configure these in <code className="text-indigo-300">backend/.env</code>. Never expose them in the frontend.
          </p>
        </div>
      </div>
    </div>
  );
}
