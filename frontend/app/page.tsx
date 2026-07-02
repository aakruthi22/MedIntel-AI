"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { UploadCloud, Send, FileText, Shield, Brain, LogOut, CheckCircle2 } from "lucide-react";
import axios from "axios";

export default function DashboardPage() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);

  // Security Guard: Ensure user is logged in on page load
  useEffect(() => {
    const token = localStorage.getItem("medintel_token");
    if (!token) {
      router.push("/login");
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("medintel_token");
    router.push("/login");
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);
    
    setUploading(true);
    const token = localStorage.getItem("medintel_token");

    try {
      await axios.post("http://127.0.0.1:8000/api/v1/documents/upload", formData, {
        headers: { 
          "Content-Type": "multipart/form-data",
          "Authorization": `Bearer ${token}` 
        },
      });
      setUploadedFiles((prev) => [...prev, file.name]);
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Failed to upload document. Ensure backend is running and you are authenticated.");
    } finally {
      setUploading(false);
    }
  };

  const handleResearchQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;

    setIsLoading(true);
    setResult(null);
    const token = localStorage.getItem("medintel_token");

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/v1/research/query", 
        { query: query, specialty_filter: "General Informatics" },
        { 
          headers: { 
            "Authorization": `Bearer ${token}` 
          } 
        }
      );
      setResult(response.data);
    } catch (error) {
      console.error("Pipeline failure:", error);
      alert("Error executing query. Check backend connectivity.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white font-sans flex flex-col">
      {/* Navbar */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md px-6 py-4 flex justify-between items-center sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <Brain className="w-8 h-8 text-blue-500" />
          <span className="text-xl font-bold tracking-tight">MEDINTEL <span className="text-blue-500 font-light">AI</span></span>
        </div>
        <button 
          onClick={handleLogout}
          className="flex items-center gap-2 bg-slate-800 hover:bg-red-950/40 border border-slate-700 hover:border-red-900 text-slate-300 hover:text-red-400 px-4 py-2 rounded-xl transition-all text-sm"
        >
          <LogOut className="w-4 h-4" />
          Disconnect Portal
        </button>
      </header>

      {/* Main Container */}
      <div className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Left Control Panel: Uploads & Knowledge Base info */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
            <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
              <UploadCloud className="w-4 h-4 text-blue-500" /> Document Ingestion
            </h2>
            <p className="text-xs text-slate-400">Upload private medical literature or patient records to secure isolated vector space.</p>
            
            <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-slate-800 hover:border-blue-500/50 bg-slate-950 rounded-xl cursor-pointer transition-colors group">
              <div className="flex flex-col items-center justify-center pt-5 pb-6 text-center px-2">
                <UploadCloud className="w-8 h-8 text-slate-500 group-hover:text-blue-500 mb-2 transition-colors" />
                <p className="text-xs text-slate-400 font-medium">{uploading ? "Ingesting PDF..." : "Drop Clinical PDF here"}</p>
              </div>
              <input type="file" accept=".pdf" className="hidden" onChange={handleFileUpload} disabled={uploading} />
            </label>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3 max-h-64 overflow-y-auto">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Indexed Knowledge</h3>
            {uploadedFiles.length === 0 ? (
              <p className="text-xs text-slate-600 italic">No custom assets uploaded yet.</p>
            ) : (
              <div className="space-y-2">
                {uploadedFiles.map((file, idx) => (
                  <div key={idx} className="flex items-center gap-2 bg-slate-950 p-2 rounded-lg border border-slate-800 text-xs">
                    <FileText className="w-3.5 h-3.5 text-blue-500 shrink-0" />
                    <span className="truncate text-slate-300">{file}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Panel: Research Lab Chat Interface */}
        <div className="lg:col-span-3 flex flex-col space-y-6">
          
          {/* Query Bar */}
          <form onSubmit={handleResearchQuery} className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex gap-3 shadow-xl">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Query deep medical knowledge or private documents (e.g., 'Identify symptoms of metabolic syndrome')"
              className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500 placeholder-slate-600 text-white"
            />
            <button
              type="submit"
              disabled={isLoading || !query}
              className="bg-blue-600 hover:bg-blue-500 text-white p-3 rounded-xl transition-all disabled:opacity-50 disabled:hover:bg-blue-600"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>

          {/* Core Response Window */}
          <div className="flex-1 bg-slate-900 border border-slate-800 rounded-2xl p-6 min-h-[400px] flex flex-col shadow-inner relative overflow-hidden">
            
            {/* Loading Indicator */}
            {isLoading && (
              <div className="absolute inset-0 bg-slate-900/80 backdrop-blur-sm flex flex-col items-center justify-center space-y-4">
                <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
                <p className="text-sm text-slate-400 animate-pulse font-medium">Orchestrating Agents & Synthesizing Grounded Insight...</p>
              </div>
            )}

            {/* Empty State */}
            {!result && !isLoading && (
              <div className="flex-1 flex flex-col items-center justify-center text-center max-w-md mx-auto space-y-4">
                <Shield className="w-12 h-12 text-slate-700" />
                <h3 className="text-base font-semibold text-slate-300">Isolated Lab Sandbox Ready</h3>
                <p className="text-xs text-slate-500">Submit an inquiry above. LangGraph agents will verify security restrictions, retrieve matching vector data, and validate medical responses.</p>
              </div>
            )}

            {/* Result & Evidence Mapping View */}
            {result && (
              <div className="space-y-6 flex-1 overflow-y-auto">
                <div className="space-y-2">
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-blue-400 flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-green-500" /> Clinical Synthesis Result
                  </h3>
                  <div className="bg-slate-950 p-5 rounded-xl border border-slate-800/80 text-sm leading-relaxed text-slate-200 shadow-inner">
                    {result.draft_answer || result.answer || JSON.stringify(result)}
                  </div>
                </div>

                {/* Evidence Citations */}
                {result.citations && result.citations.length > 0 && (
                  <div className="space-y-3 pt-2">
                    <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Verified Evidence Citations</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {result.citations.map((citation: any, idx: number) => (
                        <div key={idx} className="bg-slate-950/60 border border-slate-800 p-4 rounded-xl flex flex-col space-y-2 hover:border-slate-700 transition-colors">
                          <div className="flex justify-between items-center text-xs">
                            <span className="font-medium text-blue-400 flex items-center gap-1">
                              <FileText className="w-3 h-3" /> {citation.source_name || "Literature Asset"}
                            </span>
                            <span className="text-slate-500 bg-slate-900 px-2 py-0.5 rounded-md text-[10px]">
                              Match: {Math.round(citation.confidence_score * 100)}%
                            </span>
                          </div>
                          <p className="text-xs text-slate-400 line-clamp-3 italic">"{citation.chunk_content}"</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}