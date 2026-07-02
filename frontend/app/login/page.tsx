"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function LoginPage() {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage("");
    setIsError(false);

    // FastAPI OAuth2PasswordRequestForm expects form-urlencoded data
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    // Ensure we are calling the correct route based on the toggle state
    const endpoint = isRegister ? "/register" : "/token";

    try {
      const response = await axios.post(`http://localhost:8000${endpoint}`, formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      if (isRegister) {
        // Success: Registration
        setMessage("Registration successful! You can now login.");
        setIsError(false);
        setIsRegister(false); // Switch to login view automatically
      } else {
        // Success: Login
        localStorage.setItem("medintel_token", response.data.access_token);
        router.push("/"); // Redirect to dashboard
      }
    } catch (err: any) {
      setIsError(true);
      // Safely handle the error to prevent "undefined" crashes
      if (err.response) {
        // The backend received the request but rejected it (e.g., wrong password, user exists)
        console.error("Backend Error Details:", err.response.data);
        setMessage(err.response.data.detail || "Authentication failed.");
      } else {
        // The backend never received the request (e.g., CORS error, server offline)
        console.error("Network Error:", err);
        setMessage("Network error. Is the FastAPI backend running?");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4 text-white font-sans">
      <div className="bg-slate-900 p-8 rounded-2xl w-full max-w-sm border border-slate-800 shadow-2xl">
        
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-xl font-bold tracking-tight mb-1">
            MEDINTEL <span className="text-blue-500 font-light">AI</span>
          </h1>
          <h2 className="text-lg font-medium text-slate-300">
            {isRegister ? "Create Account" : "Welcome Back"}
          </h2>
        </div>
        
        {/* Status Message */}
        {message && (
          <p className={`mb-6 text-sm text-center p-3 rounded-lg border ${
            isError 
              ? 'bg-red-950/50 border-red-900/50 text-red-400' 
              : 'bg-green-950/50 border-green-900/50 text-green-400'
          }`}>
            {message}
          </p>
        )}
        
        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <input 
              className="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all placeholder-slate-500" 
              placeholder="Username" 
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)} 
            />
          </div>
          <div>
            <input 
              className="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all placeholder-slate-500" 
              type="password" 
              placeholder="Password" 
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)} 
            />
          </div>
          
          <button 
            type="submit" 
            disabled={isLoading || !username || !password}
            className="w-full bg-blue-600 hover:bg-blue-500 text-white p-3 rounded-xl font-medium transition-all disabled:opacity-50 disabled:hover:bg-blue-600 mt-2"
          >
            {isLoading ? "Processing..." : (isRegister ? "Register" : "Login")}
          </button>
        </form>

        {/* Toggle Mode */}
        <div className="text-sm text-center mt-6 text-slate-400">
          {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
          <button 
            type="button"
            className="text-blue-500 hover:text-blue-400 hover:underline font-medium focus:outline-none" 
            onClick={() => {
              setIsRegister(!isRegister);
              setMessage(""); // Clear message when toggling
              setIsError(false);
            }}
          >
            {isRegister ? "Login here" : "Register here"}
          </button>
        </div>

      </div>
    </div>
  );
}