"use client";

import { CollegeResult } from "@/services/api";

interface ResultsTableProps {
  results: CollegeResult[];
  userRank: number;
}

export default function ResultsTable({ results, userRank }: ResultsTableProps) {
  if (results.length === 0) {
    return (
      <div className="bg-white p-12 text-center rounded-2xl border border-slate-200 shadow-sm">
        <div className="text-slate-300 mb-4 flex justify-center">
          <svg className="w-16 h-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-slate-900">No colleges matched your criteria</h3>
        <p className="mt-2 text-slate-500 max-w-md mx-auto">
          Your rank ({userRank.toLocaleString()}) might be higher than the closing ranks, or your selected filters might be too restrictive.
        </p>
      </div>
    );
  }

  // Visual cues for safety margin (rank gap)
  const getGapColor = (gap: number) => {
    if (gap < 0) return "text-red-700 bg-red-50 border-red-200"; // Negative
    if (gap < 200) return "text-orange-700 bg-orange-50 border-orange-200"; // Close call
    return "text-emerald-700 bg-emerald-50 border-emerald-200"; // Safe
  };

  const getChanceColor = (chance: string) => {
    switch(chance) {
      case "Safe": return "bg-emerald-100 text-emerald-800 border-emerald-200";
      case "Moderate": return "bg-amber-100 text-amber-800 border-amber-200";
      case "Dream": return "bg-fuchsia-100 text-fuchsia-800 border-fuchsia-200";
      default: return "bg-slate-100 text-slate-800 border-slate-200";
    }
  };

  const getTypeColor = (type: string) => {
    switch(type) {
      case "IIT": return "bg-blue-100 text-blue-800 border-blue-200";
      case "NIT": return "bg-purple-100 text-purple-800 border-purple-200";
      case "IIIT": return "bg-teal-100 text-teal-800 border-teal-200";
      case "GFTI": return "bg-rose-100 text-rose-800 border-rose-200";
      default: return "bg-slate-100 text-slate-800 border-slate-200";
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse whitespace-nowrap">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-xs uppercase tracking-wider font-semibold">
              <th className="py-4 px-6">Institute</th>
              <th className="py-4 px-6">Branch</th>
              <th className="py-4 px-6">Category</th>
              <th className="py-4 px-6 text-center">Chance</th>
              <th className="py-4 px-6 text-right">Opening</th>
              <th className="py-4 px-6 text-right">Closing</th>
              <th className="py-4 px-6 text-right">Gap</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {results.map((result, idx) => {
              const isTopMatch = idx === 0;
              
              return (
                <tr 
                  key={`${result.institute}-${result.program}-${result.quota}-${idx}`}
                  className={`transition-colors hover:bg-slate-50 ${isTopMatch ? 'bg-blue-50/40 relative' : ''}`}
                >
                  <td className="py-4 px-6">
                    {/* Top match indicator strip */}
                    {isTopMatch && <div className="absolute left-0 top-0 bottom-0 w-1 bg-blue-500 rounded-l-2xl"></div>}
                    
                    <div className="font-semibold text-slate-900 whitespace-normal min-w-[200px]" title={result.institute}>
                      {result.institute}
                      {isTopMatch && (
                        <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-200 uppercase tracking-wide">
                          Top Match
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="py-4 px-6 whitespace-normal min-w-[200px]">
                    <div className="font-medium text-slate-700" title={result.program}>
                      {result.branch}
                    </div>
                    <div className="text-xs text-slate-500 mt-1 capitalize">
                      {result.program_type}
                    </div>
                  </td>
                  <td className="py-4 px-6">
                    <div className="flex flex-col gap-1.5 items-start">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold border ${getTypeColor(result.college_type)}`}>
                        {result.college_type}
                      </span>
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold bg-slate-100 text-slate-600 border border-slate-200">
                        {result.quota} Quota
                      </span>
                    </div>
                  </td>
                  <td className="py-4 px-6 text-center">
                    <span 
                      className={`inline-flex items-center justify-center px-3 py-1 rounded-md text-xs font-bold border ${getChanceColor(result.chance_category)} shadow-sm`}
                    >
                      {result.chance_category}
                    </span>
                  </td>
                  <td className="py-4 px-6 text-right text-slate-500 font-medium text-sm">
                    {result.opening_rank > 0 ? result.opening_rank.toLocaleString() : '-'}
                  </td>
                  <td className="py-4 px-6 text-right font-bold text-slate-900">
                    {result.closing_rank.toLocaleString()}
                  </td>
                  <td className="py-4 px-6 text-right">
                    <span 
                      className={`inline-flex items-center justify-center px-2.5 py-1 rounded-md text-xs font-bold border ${getGapColor(result.rank_gap)} bg-white`}
                      title="Margin between your rank and the closing rank"
                    >
                      {result.rank_gap > 0 ? '+' : ''}{result.rank_gap.toLocaleString()}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
