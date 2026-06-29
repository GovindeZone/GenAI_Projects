import { useState, useMemo } from 'react';
import { RefreshCw, Download } from 'lucide-react';
import FilterBar from '../components/Filters/FilterBar';
import EmailTable from '../components/EmailTable/EmailTable';
import EmailDetail from '../components/EmailDetail/EmailDetail';
import type { Email, AppConfig, FilterState } from '../types';

interface EmailsPageProps {
  emails: Email[];
  config: AppConfig;
  loading: boolean;
  onRefresh: (filters: Partial<FilterState>) => void;
  initialCategoryFilter?: string;
}

const DEFAULT_FILTERS: FilterState = {
  category: '',
  priority: '',
  sender: '',
  keyword: '',
  dateFrom: '',
  dateTo: '',
};

export default function EmailsPage({ emails, config, loading, onRefresh, initialCategoryFilter }: EmailsPageProps) {
  const [filters, setFilters] = useState<FilterState>({
    ...DEFAULT_FILTERS,
    category: initialCategoryFilter || '',
  });
  const [selectedEmail, setSelectedEmail] = useState<Email | null>(null);

  const filteredEmails = useMemo(() => {
    return emails.filter((email) => {
      if (filters.category && email.analysis?.category !== filters.category) return false;
      if (filters.priority && email.analysis?.priority !== filters.priority) return false;
      if (filters.sender && !email.senderEmail.toLowerCase().includes(filters.sender.toLowerCase()) &&
          !email.senderName.toLowerCase().includes(filters.sender.toLowerCase())) return false;
      if (filters.keyword) {
        const kw = filters.keyword.toLowerCase();
        if (!email.subject.toLowerCase().includes(kw) &&
            !email.snippet.toLowerCase().includes(kw) &&
            !(email.analysis?.summary || '').toLowerCase().includes(kw)) return false;
      }
      if (filters.dateFrom && new Date(email.date) < new Date(filters.dateFrom)) return false;
      if (filters.dateTo && new Date(email.date) > new Date(filters.dateTo + 'T23:59:59')) return false;
      return true;
    });
  }, [emails, filters]);

  function handleRefresh() {
    onRefresh({
      keyword: filters.keyword,
      sender: filters.sender,
      dateFrom: filters.dateFrom,
      dateTo: filters.dateTo,
    });
  }

  function exportCSV() {
    const headers = ['Sender', 'Email', 'Subject', 'Category', 'Priority', 'Summary', 'Date'];
    const rows = filteredEmails.map((e) => [
      e.senderName,
      e.senderEmail,
      `"${e.subject.replace(/"/g, '""')}"`,
      e.analysis?.category,
      e.analysis?.priority,
      `"${(e.analysis?.summary || '').replace(/"/g, '""')}"`,
      new Date(e.date).toLocaleDateString(),
    ]);
    const csv = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `gmail-issues-${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Email Queue</h1>
          <p className="text-slate-400 text-sm mt-0.5">{filteredEmails.length} issues shown</p>
        </div>
        <div className="flex items-center gap-2">
          {filteredEmails.length > 0 && (
            <button
              onClick={exportCSV}
              className="flex items-center gap-2 px-3 py-2 text-sm text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg transition-colors"
            >
              <Download className="w-4 h-4" />
              Export CSV
            </button>
          )}
          <button
            onClick={handleRefresh}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 rounded-lg transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            {loading ? 'Fetching...' : 'Refresh'}
          </button>
        </div>
      </div>

      <FilterBar filters={filters} onChange={setFilters} onReset={() => setFilters(DEFAULT_FILTERS)} />

      <EmailTable
        emails={filteredEmails}
        assignerEmail={config.assignerEmail}
        onViewEmail={setSelectedEmail}
        loading={loading}
      />

      {selectedEmail && (
        <EmailDetail
          email={selectedEmail}
          config={config}
          onClose={() => setSelectedEmail(null)}
        />
      )}
    </div>
  );
}
