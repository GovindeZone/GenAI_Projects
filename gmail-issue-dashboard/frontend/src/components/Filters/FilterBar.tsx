import { Search, X } from 'lucide-react';
import type { FilterState } from '../../types';

interface FilterBarProps {
  filters: FilterState;
  onChange: (filters: FilterState) => void;
  onReset: () => void;
}

const CATEGORY_OPTIONS = ['All', 'New Ticket', 'In-Progress', 'Resolved', 'Escalation'];
const PRIORITY_OPTIONS = ['All', 'Critical', 'High', 'Medium', 'Low'];

export default function FilterBar({ filters, onChange, onReset }: FilterBarProps) {
  const set = (key: keyof FilterState, value: string) =>
    onChange({ ...filters, [key]: value });

  const hasActiveFilters = Object.values(filters).some((v) => v !== '' && v !== 'All');

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <div className="flex flex-wrap items-center gap-3">
        {/* Keyword search */}
        <div className="relative flex-1 min-w-[180px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search subject, sender..."
            value={filters.keyword}
            onChange={(e) => set('keyword', e.target.value)}
            className="w-full pl-9 pr-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          />
        </div>

        {/* Category */}
        <select
          value={filters.category}
          onChange={(e) => set('category', e.target.value)}
          className="px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
        >
          {CATEGORY_OPTIONS.map((c) => (
            <option key={c} value={c === 'All' ? '' : c}>{c}</option>
          ))}
        </select>

        {/* Priority */}
        <select
          value={filters.priority}
          onChange={(e) => set('priority', e.target.value)}
          className="px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
        >
          {PRIORITY_OPTIONS.map((p) => (
            <option key={p} value={p === 'All' ? '' : p}>{p}</option>
          ))}
        </select>

        {/* Sender */}
        <input
          type="text"
          placeholder="Sender email..."
          value={filters.sender}
          onChange={(e) => set('sender', e.target.value)}
          className="px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 w-44"
        />

        {/* Date range */}
        <div className="flex items-center gap-2">
          <input
            type="date"
            value={filters.dateFrom}
            onChange={(e) => set('dateFrom', e.target.value)}
            className="px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
          />
          <span className="text-slate-500 text-xs">to</span>
          <input
            type="date"
            value={filters.dateTo}
            onChange={(e) => set('dateTo', e.target.value)}
            className="px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
          />
        </div>

        {hasActiveFilters && (
          <button
            onClick={onReset}
            className="flex items-center gap-1.5 px-3 py-2 text-sm text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg transition-colors"
          >
            <X className="w-3.5 h-3.5" />
            Reset
          </button>
        )}
      </div>
    </div>
  );
}
