"use client";

import { useState } from "react";
import { PredictRequest, Category, CollegeType, Gender, ExamType } from "@/services/api";

const INDIAN_STATES = [
  "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
  "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
  "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
  "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
  "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
  "West Bengal", "Delhi", "Jammu & Kashmir", "Ladakh", "Puducherry",
  "Chandigarh",
];

interface InputPanelProps {
  onPredict: (req: PredictRequest) => void;
  isLoading: boolean;
}

export default function InputPanel({ onPredict, isLoading }: InputPanelProps) {
  const [examType, setExamType] = useState<ExamType>("JEE_MAIN");
  const [rank, setRank] = useState<number | "">("");
  const [category, setCategory] = useState<Category>("OPEN");
  const [collegeType, setCollegeType] = useState<CollegeType>("ALL");
  const [gender, setGender] = useState<Gender>("Gender-Neutral");
  const [homeState, setHomeState] = useState<string>("");
  const [includeFiveYear, setIncludeFiveYear] = useState<boolean>(true);

  // Home State is relevant mainly for NITs and GFTIs
  const showHomeState = collegeType === "NIT" || collegeType === "GFTI" || collegeType === "ALL";

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!rank || rank <= 0) return;
    
    onPredict({
      exam_type: examType,
      rank: Number(rank),
      category,
      college_type: collegeType,
      gender,
      home_state: showHomeState ? (homeState || null) : null,
      include_five_year: includeFiveYear,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Exam Type */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Exam Type
          </label>
          <select
            value={examType}
            onChange={(e) => setExamType(e.target.value as ExamType)}
            className="w-full px-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all font-medium text-slate-800"
            disabled={isLoading}
          >
            <option value="JEE_MAIN">JEE Main (NIT/IIIT/GFTI)</option>
            <option value="JEE_ADVANCED">JEE Advanced (IIT)</option>
          </select>
        </div>

        {/* Rank Input */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Category Rank (Or CRL if OPEN)
          </label>
          <input
            type="number"
            min="1"
            value={rank}
            onChange={(e) => setRank(e.target.value ? Number(e.target.value) : "")}
            className="w-full px-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all placeholder:text-slate-400 font-medium"
            placeholder="e.g. 5000"
            required
            disabled={isLoading}
          />
        </div>

        {/* Category */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Category
          </label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value as Category)}
            className="w-full px-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all font-medium text-slate-800"
            disabled={isLoading}
          >
            <option value="OPEN">OPEN (General)</option>
            <option value="OBC-NCL">OBC-NCL</option>
            <option value="SC">SC</option>
            <option value="ST">ST</option>
            <option value="EWS">Gen-EWS</option>
          </select>
        </div>

        {/* Gender */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Gender Pool
          </label>
          <select
            value={gender}
            onChange={(e) => setGender(e.target.value as Gender)}
            className="w-full px-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all font-medium text-slate-800"
            disabled={isLoading}
          >
            <option value="Gender-Neutral">Gender-Neutral</option>
            <option value="Female-only">Female-Only (including Supernumerary)</option>
          </select>
        </div>

        {/* College Type */}
        {examType === "JEE_MAIN" && (
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Target Institutes
            </label>
            <select
              value={collegeType}
              onChange={(e) => setCollegeType(e.target.value as CollegeType)}
              className="w-full px-4 py-2 bg-slate-50 border border-slate-300 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all font-medium text-slate-800"
              disabled={isLoading}
            >
              <option value="ALL">All Institutes (NIT, IIIT, GFTI)</option>
              <option value="NIT">NITs Only</option>
              <option value="IIIT">IIITs Only</option>
              <option value="GFTI">GFTIs Only</option>
            </select>
          </div>
        )}

        {/* Home State (Conditional) */}
        {showHomeState && examType === "JEE_MAIN" ? (
          <div className="animate-in fade-in slide-in-from-top-2 duration-300">
            <label className="block text-sm font-medium text-slate-700 mb-2 text-blue-700">
              Home State (For NIT/GFTI Quotas)
            </label>
            <select
              value={homeState}
              onChange={(e) => setHomeState(e.target.value)}
              className="w-full px-4 py-2 bg-blue-50 border border-blue-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all font-medium text-blue-900"
              disabled={isLoading}
              required={collegeType === "NIT" || collegeType === "GFTI"}
            >
              <option value="">Select Home State...</option>
              {INDIAN_STATES.map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>
          </div>
        ) : (
          <div className="hidden lg:block"></div>
        )}
      </div>

      <div className="mt-8 pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-6">
        
        {/* Toggle 5-year */}
        <label className="flex items-center space-x-3 cursor-pointer group">
          <div className="relative">
            <input
              type="checkbox"
              className="sr-only"
              checked={includeFiveYear}
              onChange={(e) => setIncludeFiveYear(e.target.checked)}
              disabled={isLoading}
            />
            <div className={`block w-11 h-6 rounded-full transition-colors duration-300 ${includeFiveYear ? 'bg-blue-600' : 'bg-slate-300'}`}></div>
            <div className={`absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform duration-300 ${includeFiveYear ? 'translate-x-5' : 'translate-x-0'}`}></div>
          </div>
          <span className="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">
            Include 5-Year Integrated Programs
          </span>
        </label>

        {/* Submit */}
        <button
          type="submit"
          disabled={isLoading || !rank || (showHomeState && !homeState)}
          className="w-full sm:w-auto px-8 py-3 bg-slate-900 text-white font-medium rounded-xl hover:bg-slate-800 hover:shadow-lg hover:-translate-y-0.5 focus:ring-4 focus:ring-slate-900/20 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none transition-all"
        >
          {isLoading ? (
            <div className="flex items-center justify-center space-x-2">
              <span className="animate-spin h-4 w-4 border-2 border-white/30 border-t-white rounded-full"></span>
              <span>Searching...</span>
            </div>
          ) : (
            "Find Colleges"
          )}
        </button>
      </div>
    </form>
  );
}
