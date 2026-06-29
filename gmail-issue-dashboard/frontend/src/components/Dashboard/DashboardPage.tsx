import { Mail, AlertCircle, Clock, CheckCircle, TrendingUp } from 'lucide-react';
import StatCard from './StatCard';
import type { DashboardStats, Email } from '../../types';

interface DashboardPageProps {
  stats: DashboardStats;
  emails: Email[];
  onFilterCategory: (cat: string) => void;
  onNavigateToEmails: () => void;
}

const categoryColors: Record<string, string> = {
  'New Ticket': 'text-blue-400 bg-blue-400/10 border-blue-400/20',
  'In-Progress': 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20',
  'Resolved': 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20',
  'Escalation': 'text-red-400 bg-red-400/10 border-red-400/20',
};

const priorityColors: Record<string, string> = {
  Critical: 'text-red-400 bg-red-400/10',
  High: 'text-orange-400 bg-orange-400/10',
  Medium: 'text-yellow-400 bg-yellow-400/10',
  Low: 'text-slate-400 bg-slate-400/10',
};

export default function DashboardPage({ stats, emails, onFilterCategory, onNavigateToEmails }: DashboardPageProps) {
  const recentEmails = [...emails].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()).slice(0, 5);

  const criticalCount = emails.filter(e => e.analysis?.priority === 'Critical').length;
  const highCount = emails.filter(e => e.analysis?.priority === 'High').length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Dashboard Overview</h1>
        <p className="text-slate-400 text-sm mt-1">Real-time view of your Gmail issue tracking</p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard
          label="Total Emails"
          value={stats.total}
          icon={Mail}
          color="text-indigo-400"
          bgColor="bg-indigo-950/40"
          borderColor="border-indigo-800/40"
          onClick={onNavigateToEmails}
        />
        <StatCard
          label="New Tickets"
          value={stats.newTicket}
          icon={AlertCircle}
          color="text-blue-400"
          bgColor="bg-blue-950/40"
          borderColor="border-blue-800/40"
          onClick={() => { onFilterCategory('New Ticket'); onNavigateToEmails(); }}
        />
        <StatCard
          label="In-Progress"
          value={stats.inProgress}
          icon={Clock}
          color="text-yellow-400"
          bgColor="bg-yellow-950/40"
          borderColor="border-yellow-800/40"
          onClick={() => { onFilterCategory('In-Progress'); onNavigateToEmails(); }}
        />
        <StatCard
          label="Resolved"
          value={stats.resolved}
          icon={CheckCircle}
          color="text-emerald-400"
          bgColor="bg-emerald-950/40"
          borderColor="border-emerald-800/40"
          onClick={() => { onFilterCategory('Resolved'); onNavigateToEmails(); }}
        />
        <StatCard
          label="Escalations"
          value={stats.escalation}
          icon={TrendingUp}
          color="text-red-400"
          bgColor="bg-red-950/40"
          borderColor="border-red-800/40"
          onClick={() => { onFilterCategory('Escalation'); onNavigateToEmails(); }}
        />
      </div>

      {/* Priority Breakdown */}
      {stats.total > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h3 className="text-sm font-semibold text-slate-300 mb-4">Category Distribution</h3>
            <div className="space-y-3">
              {[
                { label: 'New Ticket', value: stats.newTicket, color: 'bg-blue-500' },
                { label: 'In-Progress', value: stats.inProgress, color: 'bg-yellow-500' },
                { label: 'Resolved', value: stats.resolved, color: 'bg-emerald-500' },
                { label: 'Escalation', value: stats.escalation, color: 'bg-red-500' },
              ].map(({ label, value, color }) => (
                <div key={label}>
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>{label}</span>
                    <span>{stats.total > 0 ? Math.round((value / stats.total) * 100) : 0}%</span>
                  </div>
                  <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${color} rounded-full transition-all duration-500`}
                      style={{ width: stats.total > 0 ? `${(value / stats.total) * 100}%` : '0%' }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h3 className="text-sm font-semibold text-slate-300 mb-4">Priority Summary</h3>
            <div className="grid grid-cols-2 gap-3">
              {[
                { label: 'Critical', count: criticalCount, style: 'text-red-400 bg-red-950/50 border-red-800/40' },
                { label: 'High', count: highCount, style: 'text-orange-400 bg-orange-950/50 border-orange-800/40' },
                { label: 'Medium', count: emails.filter(e => e.analysis?.priority === 'Medium').length, style: 'text-yellow-400 bg-yellow-950/50 border-yellow-800/40' },
                { label: 'Low', count: emails.filter(e => e.analysis?.priority === 'Low').length, style: 'text-slate-400 bg-slate-800/50 border-slate-700' },
              ].map(({ label, count, style }) => (
                <div key={label} className={`rounded-lg border p-3 ${style}`}>
                  <p className="text-2xl font-bold">{count}</p>
                  <p className="text-xs opacity-75">{label} Priority</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Recent Emails */}
      {recentEmails.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-300">Recent Issues</h3>
            <button onClick={onNavigateToEmails} className="text-xs text-indigo-400 hover:text-indigo-300">
              View All →
            </button>
          </div>
          <div className="space-y-2">
            {recentEmails.map((email) => (
              <div key={email.id} className="flex items-start gap-3 p-3 rounded-lg hover:bg-slate-800/60 transition-colors">
                <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-xs font-medium text-slate-300 shrink-0 mt-0.5">
                  {email.senderName?.charAt(0)?.toUpperCase() || '?'}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-sm font-medium text-slate-200 truncate">{email.senderName}</span>
                    <span className={`text-xs px-2 py-0.5 rounded-full border ${categoryColors[email.analysis?.category] || ''}`}>
                      {email.analysis?.category}
                    </span>
                    <span className={`text-xs px-1.5 py-0.5 rounded ${priorityColors[email.analysis?.priority] || ''}`}>
                      {email.analysis?.priority}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 truncate mt-0.5">{email.subject}</p>
                </div>
                <span className="text-xs text-slate-500 shrink-0">
                  {new Date(email.date).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {stats.total === 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center">
          <Mail className="w-12 h-12 text-slate-700 mx-auto mb-4" />
          <p className="text-slate-400">No emails analyzed yet.</p>
          <p className="text-slate-500 text-sm mt-1">Configure your settings and fetch emails to get started.</p>
        </div>
      )}
    </div>
  );
}
