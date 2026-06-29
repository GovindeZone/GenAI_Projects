import { ChevronUp, ChevronDown, Eye, Mail, TrendingUp } from 'lucide-react';
import { format } from 'date-fns';
import type { Email } from '../../types';

interface EmailTableProps {
  emails: Email[];
  assignerEmail: string;
  onViewEmail: (email: Email) => void;
  loading?: boolean;
}

const categoryBadge: Record<string, string> = {
  'New Ticket': 'text-blue-300 bg-blue-900/50 border-blue-700/50',
  'In-Progress': 'text-yellow-300 bg-yellow-900/50 border-yellow-700/50',
  'Resolved': 'text-emerald-300 bg-emerald-900/50 border-emerald-700/50',
  'Escalation': 'text-red-300 bg-red-900/50 border-red-700/50',
};

const priorityBadge: Record<string, string> = {
  Critical: 'text-red-300 bg-red-900/40',
  High: 'text-orange-300 bg-orange-900/40',
  Medium: 'text-yellow-300 bg-yellow-900/40',
  Low: 'text-slate-300 bg-slate-700/40',
};

export default function EmailTable({ emails, assignerEmail, onViewEmail, loading }: EmailTableProps) {
  if (loading) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center">
        <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-slate-400 text-sm">Analyzing emails...</p>
      </div>
    );
  }

  if (emails.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center">
        <Mail className="w-10 h-10 text-slate-700 mx-auto mb-3" />
        <p className="text-slate-400">No emails match your filters.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
      <div className="overflow-x-auto scrollbar-thin">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-800 text-left">
              {['Sender', 'Subject', 'Summary', 'Category', 'Priority', 'Assigned To', 'Date', 'Action'].map((h) => (
                <th key={h} className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide whitespace-nowrap">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {emails.map((email) => (
              <tr key={email.id} className="hover:bg-slate-800/40 transition-colors group">
                {/* Sender */}
                <td className="px-4 py-3 whitespace-nowrap">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-full bg-slate-700 flex items-center justify-center text-xs font-medium text-slate-300 shrink-0">
                      {email.senderName?.charAt(0)?.toUpperCase() || '?'}
                    </div>
                    <div className="min-w-0">
                      <p className="text-slate-200 font-medium truncate max-w-[110px]">{email.senderName}</p>
                      <p className="text-xs text-slate-500 truncate max-w-[110px]">{email.senderEmail}</p>
                    </div>
                  </div>
                </td>

                {/* Subject */}
                <td className="px-4 py-3 max-w-[180px]">
                  <p className="text-slate-300 truncate" title={email.subject}>{email.subject}</p>
                </td>

                {/* Summary */}
                <td className="px-4 py-3 max-w-[220px]">
                  <p className="text-slate-400 text-xs line-clamp-2">{email.analysis?.summary}</p>
                </td>

                {/* Category */}
                <td className="px-4 py-3 whitespace-nowrap">
                  <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs border font-medium ${categoryBadge[email.analysis?.category] || ''}`}>
                    {email.analysis?.category === 'Escalation' && <TrendingUp className="w-3 h-3" />}
                    {email.analysis?.category}
                  </span>
                </td>

                {/* Priority */}
                <td className="px-4 py-3 whitespace-nowrap">
                  <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${priorityBadge[email.analysis?.priority] || ''}`}>
                    {email.analysis?.priority}
                  </span>
                </td>

                {/* Assigned To */}
                <td className="px-4 py-3 whitespace-nowrap">
                  <p className="text-slate-400 text-xs truncate max-w-[130px]" title={assignerEmail}>
                    {assignerEmail || '—'}
                  </p>
                </td>

                {/* Date */}
                <td className="px-4 py-3 whitespace-nowrap">
                  <p className="text-slate-400 text-xs">
                    {email.date ? format(new Date(email.date), 'MMM dd, yyyy') : '—'}
                  </p>
                  <p className="text-slate-600 text-xs">
                    {email.date ? format(new Date(email.date), 'hh:mm a') : ''}
                  </p>
                </td>

                {/* Action */}
                <td className="px-4 py-3 whitespace-nowrap">
                  <button
                    onClick={() => onViewEmail(email)}
                    className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium rounded-lg transition-colors"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="px-4 py-2 border-t border-slate-800 text-xs text-slate-500">
        Showing {emails.length} issue{emails.length !== 1 ? 's' : ''}
      </div>
    </div>
  );
}
