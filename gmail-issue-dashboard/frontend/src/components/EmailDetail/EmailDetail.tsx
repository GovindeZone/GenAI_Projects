import { useState } from 'react';
import { X, Send, Zap, TrendingUp, Copy, CheckCircle, AlertCircle, Clock, Mail } from 'lucide-react';
import { format } from 'date-fns';
import { analyzeApi, emailsApi } from '../../services/api';
import type { Email, AppConfig } from '../../types';

interface EmailDetailProps {
  email: Email;
  config: AppConfig;
  onClose: () => void;
}

const categoryColors: Record<string, string> = {
  'New Ticket': 'text-blue-400 bg-blue-900/40 border-blue-700/40',
  'In-Progress': 'text-yellow-400 bg-yellow-900/40 border-yellow-700/40',
  'Resolved': 'text-emerald-400 bg-emerald-900/40 border-emerald-700/40',
  'Escalation': 'text-red-400 bg-red-900/40 border-red-700/40',
};

const priorityColors: Record<string, string> = {
  Critical: 'text-red-400',
  High: 'text-orange-400',
  Medium: 'text-yellow-400',
  Low: 'text-slate-400',
};

export default function EmailDetail({ email, config, onClose }: EmailDetailProps) {
  const [replyDraft, setReplyDraft] = useState('');
  const [escalationDraft, setEscalationDraft] = useState('');
  const [generating, setGenerating] = useState<'reply' | 'escalation' | null>(null);
  const [sending, setSending] = useState<'reply' | 'escalation' | null>(null);
  const [sentStatus, setSentStatus] = useState<'reply' | 'escalation' | null>(null);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<'details' | 'reply' | 'escalation'>('details');

  const a = email.analysis;

  async function handleGenerateReply() {
    setGenerating('reply');
    setError('');
    try {
      const res = await analyzeApi.generateReply({
        email,
        analysis: a,
        companyName: config.companyName,
        assignerEmail: config.assignerEmail,
        category: a.category,
      });
      setReplyDraft(res.data.reply);
      setActiveTab('reply');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to generate reply');
    } finally {
      setGenerating(null);
    }
  }

  async function handleGenerateEscalation() {
    setGenerating('escalation');
    setError('');
    try {
      const res = await analyzeApi.generateEscalation({
        email,
        analysis: a,
        companyName: config.companyName,
        escalationEmail: config.escalationEmail,
        assignerEmail: config.assignerEmail,
      });
      setEscalationDraft(res.data.escalationDraft);
      setActiveTab('escalation');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to generate escalation');
    } finally {
      setGenerating(null);
    }
  }

  async function handleSendReply() {
    if (!replyDraft.trim()) return;
    setSending('reply');
    setError('');
    try {
      await emailsApi.send({
        receiverEmail: config.receiverEmail,
        to: email.senderEmail,
        subject: `Re: ${email.subject}`,
        body: replyDraft,
        threadId: email.threadId,
      });
      setSentStatus('reply');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to send reply');
    } finally {
      setSending(null);
    }
  }

  async function handleSendEscalation() {
    if (!escalationDraft.trim()) return;
    setSending('escalation');
    setError('');
    // Extract subject from escalation draft
    const lines = escalationDraft.split('\n');
    const subjectLine = lines.find((l) => l.toLowerCase().startsWith('subject:'));
    const subject = subjectLine ? subjectLine.replace(/^subject:\s*/i, '') : `Escalation: ${email.subject}`;
    const body = subjectLine ? lines.filter((l) => !l.toLowerCase().startsWith('subject:')).join('\n').trim() : escalationDraft;

    try {
      await emailsApi.send({
        receiverEmail: config.receiverEmail,
        to: config.escalationEmail,
        subject,
        body,
      });
      setSentStatus('escalation');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to send escalation');
    } finally {
      setSending(null);
    }
  }

  function copyToClipboard(text: string) {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="w-full max-w-3xl max-h-[90vh] bg-slate-900 border border-slate-700 rounded-2xl flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800 shrink-0">
          <div className="flex-1 min-w-0 pr-4">
            <div className="flex items-center gap-2 flex-wrap mb-1">
              <span className={`text-xs px-2.5 py-0.5 rounded-full border font-medium ${categoryColors[a?.category] || ''}`}>
                {a?.category}
              </span>
              <span className={`text-xs font-semibold ${priorityColors[a?.priority] || ''}`}>
                {a?.priority} Priority
              </span>
              {a?.topic && (
                <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400">{a.topic}</span>
              )}
            </div>
            <h2 className="text-lg font-semibold text-white truncate">{email.subject}</h2>
            <p className="text-sm text-slate-400 mt-0.5">
              From <span className="text-slate-300">{email.senderName}</span> &lt;{email.senderEmail}&gt;
            </p>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors shrink-0">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800 shrink-0">
          {(['details', 'reply', 'escalation'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-5 py-3 text-sm font-medium capitalize transition-colors border-b-2 ${
                activeTab === tab
                  ? 'border-indigo-500 text-indigo-400'
                  : 'border-transparent text-slate-500 hover:text-slate-300'
              }`}
            >
              {tab === 'reply' ? 'Reply Draft' : tab === 'escalation' ? 'Escalation' : 'Details'}
            </button>
          ))}
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto scrollbar-thin p-5">
          {error && (
            <div className="mb-4 p-3 bg-red-950/50 border border-red-800/50 rounded-lg text-red-400 text-sm flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              {error}
            </div>
          )}

          {activeTab === 'details' && (
            <div className="space-y-5">
              {/* Meta */}
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="p-3 bg-slate-800/50 rounded-lg">
                  <p className="text-slate-500 text-xs mb-1">Date Received</p>
                  <p className="text-slate-200">{email.date ? format(new Date(email.date), 'PPP p') : '—'}</p>
                </div>
                <div className="p-3 bg-slate-800/50 rounded-lg">
                  <p className="text-slate-500 text-xs mb-1">Ticket ID</p>
                  <p className="text-slate-200 font-mono">{email.id.substring(0, 12).toUpperCase()}</p>
                </div>
                <div className="p-3 bg-slate-800/50 rounded-lg">
                  <p className="text-slate-500 text-xs mb-1">Assigned To</p>
                  <p className="text-slate-200 truncate">{config.assignerEmail || '—'}</p>
                </div>
                <div className="p-3 bg-slate-800/50 rounded-lg">
                  <p className="text-slate-500 text-xs mb-1">Sentiment</p>
                  <p className="text-slate-200">{a?.sentiment || '—'}</p>
                </div>
              </div>

              {/* AI Summary */}
              <div>
                <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">AI Summary</h4>
                <p className="text-slate-300 text-sm leading-relaxed bg-slate-800/40 rounded-lg p-3">{a?.summary}</p>
              </div>

              {/* Key Points */}
              {a?.keyPoints?.length > 0 && (
                <div>
                  <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Key Points</h4>
                  <ul className="space-y-1.5">
                    {a.keyPoints.map((point, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                        <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-2 shrink-0" />
                        {point}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Suggested Action */}
              {a?.suggestedAction && (
                <div>
                  <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Suggested Action</h4>
                  <p className="text-slate-300 text-sm bg-indigo-950/30 border border-indigo-800/30 rounded-lg p-3">{a.suggestedAction}</p>
                </div>
              )}

              {/* Original Email */}
              <div>
                <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Original Email</h4>
                <div className="bg-slate-800/40 rounded-lg p-3 max-h-48 overflow-y-auto scrollbar-thin">
                  <p className="text-slate-400 text-xs whitespace-pre-wrap font-mono leading-relaxed">
                    {email.body || email.snippet}
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'reply' && (
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="text-sm font-medium text-slate-300">Reply to: {email.senderEmail}</label>
                  {replyDraft && (
                    <button onClick={() => copyToClipboard(replyDraft)} className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-white">
                      {copied ? <CheckCircle className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                      {copied ? 'Copied' : 'Copy'}
                    </button>
                  )}
                </div>
                <textarea
                  value={replyDraft}
                  onChange={(e) => setReplyDraft(e.target.value)}
                  rows={14}
                  placeholder="Click 'Generate Reply' to draft an AI-powered response, or write your own reply here..."
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500 resize-none font-mono leading-relaxed"
                />
              </div>
              {sentStatus === 'reply' && (
                <div className="flex items-center gap-2 p-3 bg-emerald-950/50 border border-emerald-800/50 rounded-lg text-emerald-400 text-sm">
                  <CheckCircle className="w-4 h-4" />
                  Reply sent successfully!
                </div>
              )}
            </div>
          )}

          {activeTab === 'escalation' && (
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="text-sm font-medium text-slate-300">Escalation to: {config.escalationEmail}</label>
                  {escalationDraft && (
                    <button onClick={() => copyToClipboard(escalationDraft)} className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-white">
                      {copied ? <CheckCircle className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                      {copied ? 'Copied' : 'Copy'}
                    </button>
                  )}
                </div>
                <textarea
                  value={escalationDraft}
                  onChange={(e) => setEscalationDraft(e.target.value)}
                  rows={14}
                  placeholder="Click 'Generate Escalation' to create an AI-drafted escalation email..."
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500 resize-none font-mono leading-relaxed"
                />
              </div>
              {sentStatus === 'escalation' && (
                <div className="flex items-center gap-2 p-3 bg-emerald-950/50 border border-emerald-800/50 rounded-lg text-emerald-400 text-sm">
                  <CheckCircle className="w-4 h-4" />
                  Escalation email sent to {config.escalationEmail}!
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between gap-3 p-4 border-t border-slate-800 bg-slate-950/50 shrink-0 flex-wrap">
          <div className="flex items-center gap-2">
            <button
              onClick={handleGenerateReply}
              disabled={!!generating}
              className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
            >
              {generating === 'reply' ? (
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Zap className="w-4 h-4" />
              )}
              Generate Reply
            </button>
            <button
              onClick={handleSendReply}
              disabled={!replyDraft || !!sending || sentStatus === 'reply'}
              className="flex items-center gap-2 px-4 py-2 bg-emerald-700 hover:bg-emerald-600 disabled:opacity-40 text-white text-sm font-medium rounded-lg transition-colors"
            >
              {sending === 'reply' ? (
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
              Send Reply
            </button>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleGenerateEscalation}
              disabled={!!generating}
              className="flex items-center gap-2 px-4 py-2 bg-orange-700 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
            >
              {generating === 'escalation' ? (
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <TrendingUp className="w-4 h-4" />
              )}
              Generate Escalation
            </button>
            <button
              onClick={handleSendEscalation}
              disabled={!escalationDraft || !!sending || sentStatus === 'escalation'}
              className="flex items-center gap-2 px-4 py-2 bg-red-700 hover:bg-red-600 disabled:opacity-40 text-white text-sm font-medium rounded-lg transition-colors"
            >
              {sending === 'escalation' ? (
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
              Send Escalation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
