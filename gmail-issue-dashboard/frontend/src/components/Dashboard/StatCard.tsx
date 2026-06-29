import type { LucideIcon } from 'lucide-react';

interface StatCardProps {
  label: string;
  value: number;
  icon: LucideIcon;
  color: string;
  bgColor: string;
  borderColor: string;
  onClick?: () => void;
}

export default function StatCard({ label, value, icon: Icon, color, bgColor, borderColor, onClick }: StatCardProps) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-5 rounded-xl border ${borderColor} ${bgColor} hover:scale-[1.02] transition-transform cursor-pointer`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-400 mb-1">{label}</p>
          <p className={`text-3xl font-bold ${color}`}>{value}</p>
        </div>
        <div className={`p-2 rounded-lg ${bgColor} border ${borderColor}`}>
          <Icon className={`w-5 h-5 ${color}`} />
        </div>
      </div>
    </button>
  );
}
