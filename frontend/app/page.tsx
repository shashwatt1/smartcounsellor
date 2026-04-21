"use client";

import { useState } from "react";
import Image from "next/image";
import InputPanel from "@/components/InputPanel";
import ResultsTable from "@/components/ResultsTable";
import LoadingSpinner from "@/components/LoadingSpinner";
import { fetchPredictions, PredictRequest, PredictResponse } from "@/services/api";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<PredictResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async (req: PredictRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchPredictions(req);
      setResponse(data);
    } catch (err) {
      console.error(err);
      setError("Failed to reach the server. Make sure the FastAPI backend is running on http://localhost:8000.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans selection:bg-blue-200 selection:text-blue-900">
      
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm backdrop-blur-md bg-white/90">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between py-3">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => window.scrollTo({top: 0, behavior: 'smooth'})}>
            
            {/* The Company Logo */}
            <div className="relative w-12 h-12 flex-shrink-0">
              <Image 
                src="/Forms_Kart.png" 
                alt="Company Logo" 
                fill
                className="object-contain"
                priority
              />
            </div>

            <div className="hidden sm:flex flex-col">
              <h1 className="text-xl font-black tracking-tight text-slate-800 leading-tight">
                Smart Counsellor
              </h1>
              <span className="text-[11px] font-bold text-blue-600 tracking-wide uppercase">
                Powered by Forms_Kart
              </span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden sm:inline-block text-sm font-semibold text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 shadow-sm animate-pulse-slow">
              ● API Systems Online
            </span>
            <div className="text-sm font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded-full border border-slate-200 shadow-sm">
              JOSAA Model
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Layout */}
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full space-y-10">
        
        {/* Title Section */}
        <section className="text-center max-w-3xl mx-auto py-6 animate-in slide-in-from-bottom-4 duration-700 fade-in">
          <h2 className="text-4xl md:text-5xl font-black text-slate-900 tracking-tight leading-tight mb-4">
            Find Your Dream <br className="hidden sm:block" /> Engineering College
          </h2>
          <p className="text-lg md:text-xl text-slate-500 font-medium">
            Enter your category rank and preferences to predict eligible IITs, NITs, IIITs, and GFTIs based on historical cutoffs.
          </p>
        </section>

        {/* Request Panel */}
        <section className="max-w-5xl mx-auto animate-in slide-in-from-bottom-8 duration-700 delay-150 fade-in fill-mode-both">
          <InputPanel onPredict={handlePredict} isLoading={isLoading} />
        </section>

        {/* Global Error Notice */}
        {error && (
          <div className="max-w-5xl mx-auto p-4 rounded-xl bg-red-50 border-2 border-red-200 text-red-800 font-medium flex items-center gap-3 shadow-sm animate-in zoom-in-95 duration-200">
            <svg className="w-5 h-5 flex-shrink-0 text-red-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {error}
          </div>
        )}

        {/* Results / Empty State */}
        <section className="max-w-6xl mx-auto pb-10">
          {isLoading ? (
            <div className="animate-in fade-in duration-300">
              <LoadingSpinner />
              <p className="text-center text-slate-400 font-medium mt-4 animate-pulse">Running prediction models...</p>
            </div>
          ) : response ? (
            <div className="space-y-4 animate-in slide-in-from-bottom-4 duration-500 fade-in">
              <div className="flex flex-col sm:flex-row items-center justify-between px-2 gap-4">
                <h3 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                  <span className="w-2 h-8 bg-blue-500 rounded-full inline-block"></span>
                  Analyzed {response.total_results} matching programs
                </h3>
                {response.results.length > 0 && (
                  <div className="text-sm font-semibold text-slate-500 bg-white px-4 py-1.5 rounded-full shadow-sm border border-slate-200">
                    Showing top {response.results.length} colleges via {response.category} category
                  </div>
                )}
              </div>
              <ResultsTable results={response.results} userRank={response.rank} />
            </div>
          ) : (
            <div className="py-24 text-center">
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-blue-50 text-blue-500 mb-6 shadow-inner">
                <svg className="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-slate-800 mb-2">Ready to Make Predictions</h3>
              <p className="text-slate-500 font-medium max-w-sm mx-auto">
                Fill out the criteria above and click search. We&apos;ll query historical cutoffs to find your matches.
              </p>
            </div>
          )}
        </section>
        
      </main>

      {/* Footer */}
      <footer className="mt-auto bg-white border-t border-slate-200 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-start items-center">
          <p className="text-sm font-medium text-slate-500">
            Developed by <a href={response?.linkedin || "https://www.linkedin.com/in/shashwatt1/"} target="_blank" rel="noopener noreferrer" className="text-blue-600 font-bold hover:underline hover:text-blue-700 transition-colors">{response?.developed_by || "Shashwat Malviya"}</a>
          </p>
        </div>
      </footer>
    </div>
  );
}
