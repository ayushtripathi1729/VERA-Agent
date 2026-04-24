"use client";

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Terminal as TerminalIcon, 
  Cpu, 
  ShieldAlert, 
  Zap, 
  Send, 
  Activity, 
  Database, 
  ChevronRight,
  Globe
} from 'lucide-react';
import { api } from '@/lib/api';

// --- TYPES ---
interface LogEntry {
  message: string;
  status: 'SYSTEM' | 'SUCCESS' | 'ERROR' | 'INFO';
  timestamp: string;
}

export default function VeraDashboard() {
  const [input, setInput] = useState('');
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [systemStatus, setSystemStatus] = useState('IDLE');
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll terminal to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  const addLog = (message: string, status: LogEntry['status'] = 'INFO') => {
    const newLog: LogEntry = {
      message,
      status,
      timestamp: new Date().toLocaleTimeString([], { hour12: false }),
    };
    setLogs(prev => [...prev, newLog]);
  };

  const handleExecute = async () => {
    if (!input.trim() || isProcessing) return;

    setIsProcessing(true);
    setSystemStatus('EXECUTING');
    addLog(`INITIATING TASK: ${input}`, 'SYSTEM');

    try {
      // Connect to your Render Backend
      const response = await api.post('/run', { instruction: input });
      
      if (response.data.logs) {
        response.data.logs.forEach((log: any) => {
          addLog(log.message, log.status);
        });
      }
      
      addLog("SEQUENCE COMPLETE. RESULTS STORED IN MEMORY.", "SUCCESS");
    } catch (error) {
      addLog("CRITICAL FAILURE: NEURAL LINK INTERRUPTED.", "ERROR");
    } finally {
      setIsProcessing(false);
      setSystemStatus('IDLE');
      setInput('');
    }
  };

  return (
    <main className="relative flex flex-col w-full h-screen p-4 md:p-8 space-y-6 overflow-hidden">
      
      {/* 1. TOP HUD STATUS BAR */}
      <header className="glass-panel flex items-center justify-between px-8 py-4 z-20">
        <div className="flex items-center gap-4">
          <div className="relative">
            <Cpu className={`text-cyan-400 ${isProcessing ? 'animate-spin' : ''}`} size={32} />
            <div className="absolute inset-0 bg-cyan-400/20 blur-xl rounded-full" />
          </div>
          <div>
            <h1 className="text-xl font-black tracking-[0.3em] neon-text uppercase italic">V.E.R.A. v3.0</h1>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isProcessing ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'}`} />
              <span className="text-[10px] font-bold text-cyan-700 tracking-widest uppercase">
                Node: PRAYAGRAJ_CORE_01 // {systemStatus}
              </span>
            </div>
          </div>
        </div>

        <div className="hidden md:flex gap-8">
          <HudStat icon={<Globe size={14}/>} label="Network" val="Cloud_Sync" color="text-blue-400" />
          <HudStat icon={<ShieldAlert size={14}/>} label="Security" val="Groq_Secured" color="text-cyan-400" />
          <HudStat icon={<Activity size={14}/>} label="Uptime" val="99.9%" color="text-green-400" />
        </div>
      </header>

      {/* 2. MAIN DASHBOARD CONTENT */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-0">
        
        {/* LEFT: COMMAND INTERFACE */}
        <div className="lg:col-span-4 flex flex-col space-y-6">
          <section className="glass-panel p-6 flex-1 flex flex-col">
            <div className="flex items-center gap-2 mb-4">
              <Database className="text-cyan-600" size={18} />
              <h2 className="text-xs font-black uppercase tracking-[0.2em] text-cyan-600">Task_Injection</h2>
            </div>
            
            <textarea 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 w-full bg-black/50 border border-cyan-900/40 rounded-xl p-4 text-sm font-mono text-cyan-100 focus:outline-none focus:border-cyan-500/50 transition-all placeholder:text-cyan-900"
              placeholder="Inject neural instruction (e.g. 'Audit the security of the connected API')..."
            />

            <button 
              onClick={handleExecute}
              disabled={isProcessing}
              className="group relative w-full mt-6 bg-cyan-950 border border-cyan-500/40 py-4 rounded-xl overflow-hidden transition-all hover:bg-cyan-900 disabled:opacity-50"
            >
              <div className="relative z-10 flex items-center justify-center gap-2">
                <span className="font-black uppercase tracking-[0.4em] text-cyan-400 group-hover:text-white transition-colors">
                  {isProcessing ? 'Processing' : 'Deploy_Agent'}
                </span>
                <Send size={16} className="text-cyan-400 group-hover:translate-x-1 transition-transform" />
              </div>
            </button>
          </section>

          {/* SYSTEM QUICK INFO */}
          <section className="glass-panel p-6 h-40">
            <h3 className="text-[10px] font-bold text-cyan-800 uppercase mb-3 tracking-widest">Active_Modules</h3>
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-black/40 p-2 rounded border border-white/5 text-[9px] text-cyan-600 font-mono">NEURAL_PLANNER_V2</div>
              <div className="bg-black/40 p-2 rounded border border-white/5 text-[9px] text-cyan-600 font-mono">TAVILY_SEARCH_ENGINE</div>
              <div className="bg-black/40 p-2 rounded border border-white/5 text-[9px] text-cyan-600 font-mono">SEC_AUDIT_TOOL</div>
              <div className="bg-black/40 p-2 rounded border border-white/5 text-[9px] text-cyan-600 font-mono">PDF_REPORT_GEN</div>
            </div>
          </section>
        </div>

        {/* RIGHT: LIVE TERMINAL OUTPUT */}
        <div className="lg:col-span-8 glass-panel bg-black/80 flex flex-col relative overflow-hidden">
          {/* Scanline from global.css */}
          <div className="scanline" />
          
          <div className="flex items-center justify-between px-6 py-3 border-b border-cyan-900/30">
            <div className="flex items-center gap-2">
              <TerminalIcon size={14} className="text-cyan-600" />
              <span className="text-[10px] font-bold text-cyan-600 tracking-widest uppercase italic">Neural_Output_Stream</span>
            </div>
            <div className="flex gap-2">
              <div className="w-2 h-2 rounded-full bg-red-500/50" />
              <div className="w-2 h-2 rounded-full bg-yellow-500/50" />
              <div className="w-2 h-2 rounded-full bg-green-500/50" />
            </div>
          </div>

          <div 
            ref={scrollRef}
            className="flex-1 p-6 overflow-y-auto custom-scrollbar font-mono space-y-3"
          >
            {logs.length === 0 && (
              <div className="flex items-center gap-2 text-cyan-900/50 text-xs italic">
                <ChevronRight size={14} />
                <span>System operational. Awaiting task sequence...</span>
              </div>
            )}
            
            <AnimatePresence>
              {logs.map((log, index) => (
                <motion.div 
                  key={index}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.2 }}
                  className="flex gap-4 text-[13px] leading-relaxed border-l border-cyan-900/20 pl-4"
                >
                  <span className="text-cyan-800 text-[10px] min-w-[60px]">{log.timestamp}</span>
                  <span className={`uppercase text-[10px] font-black min-w-[70px] ${
                    log.status === 'ERROR' ? 'text-red-500' : 
                    log.status === 'SUCCESS' ? 'text-green-400' : 
                    log.status === 'SYSTEM' ? 'text-yellow-400' : 'text-cyan-600'
                  }`}>
                    [{log.status}]
                  </span>
                  <span className="text-cyan-100/90 whitespace-pre-wrap">{log.message}</span>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </main>
  );
}

function HudStat({ icon, label, val, color }: any) {
  return (
    <div className="flex flex-col items-end">
      <span className="text-[9px] uppercase text-cyan-800 font-black tracking-tighter flex items-center gap-1">
        {icon} {label}
      </span>
      <span className={`text-[11px] font-mono font-bold uppercase ${color}`}>{val}</span>
    </div>
  );
}
