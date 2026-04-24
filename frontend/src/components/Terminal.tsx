"use client";

import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRight, ShieldAlert, CheckCircle2, Info, AlertTriangle } from 'lucide-react';

interface LogEntry {
  message: string;
  status: 'SYSTEM' | 'SUCCESS' | 'ERROR' | 'INFO';
  timestamp: string;
}

interface TerminalProps {
  logs: LogEntry[];
}

export default function Terminal({ logs }: TerminalProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll logic for the "Neural Stream"
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [logs]);

  return (
    <div className="flex-1 flex flex-col min-h-0 bg-black/80 rounded-xl border border-cyan-900/30 overflow-hidden relative group">
      
      {/* 1. TERMINAL HEADER */}
      <div className="flex items-center justify-between px-5 py-2.5 bg-cyan-950/20 border-b border-cyan-900/30">
        <div className="flex items-center gap-3">
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-red-500/20 border border-red-500/40" />
            <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/20 border border-yellow-500/40" />
            <div className="w-2.5 h-2.5 rounded-full bg-green-500/20 border border-green-500/40" />
          </div>
          <span className="text-[10px] font-black text-cyan-700 tracking-[0.2em] uppercase italic">
            Neural_Execution_Stream // v3.0
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className="h-1 w-12 bg-cyan-900/30 rounded-full overflow-hidden">
            <motion.div 
              className="h-full bg-cyan-500" 
              animate={{ x: [-48, 48] }} 
              transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
            />
          </div>
        </div>
      </div>

      {/* 2. LOG VIEWPORT */}
      <div 
        ref={scrollRef}
        className="flex-1 p-6 overflow-y-auto custom-scrollbar font-mono relative"
      >
        {/* Subtle Scanline Overlay */}
        <div className="scanline pointer-events-none" />
        
        <AnimatePresence mode="popLayout">
          {logs.length === 0 ? (
            <motion.div 
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }}
              className="flex items-center gap-3 text-cyan-900/40 text-xs italic"
            >
              <ChevronRight size={14} className="animate-pulse" />
              <span>Kernel initialized. Awaiting neural injection...</span>
            </motion.div>
          ) : (
            logs.map((log, index) => (
              <motion.div 
                key={`${index}-${log.timestamp}`}
                initial={{ opacity: 0, x: -5, filter: 'blur(4px)' }}
                animate={{ opacity: 1, x: 0, filter: 'blur(0px)' }}
                transition={{ duration: 0.3, delay: 0.05 }}
                className="group flex gap-4 text-[13px] leading-relaxed border-l border-cyan-900/10 pl-4 mb-3 hover:bg-cyan-500/5 transition-colors rounded-r-lg"
              >
                {/* Timestamp */}
                <span className="text-[10px] text-cyan-900 font-bold min-w-[55px] mt-1 shrink-0">
                  {log.timestamp}
                </span>

                {/* Status Indicator */}
                <div className="mt-1 shrink-0">
                  <StatusIcon status={log.status} />
                </div>

                {/* Message Body */}
                <div className="flex flex-col flex-1 min-w-0">
                  <span className={`text-[10px] font-black uppercase tracking-tighter mb-0.5 ${getStatusColor(log.status)}`}>
                    {log.status}
                  </span>
                  <p className="text-cyan-100/90 break-words selection:bg-cyan-500/40">
                    {log.message}
                  </p>
                </div>
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>

      {/* 3. FOOTER DECORATION */}
      <div className="px-5 py-2 border-t border-cyan-900/10 flex justify-between items-center opacity-40">
        <span className="text-[8px] text-cyan-800 uppercase tracking-[0.3em]">Buffer_Type: Circular_FIFO</span>
        <span className="text-[8px] text-cyan-800 uppercase tracking-[0.3em]">Mode: Read_Write_Encrypted</span>
      </div>
    </div>
  );
}

// --- HELPERS ---

function StatusIcon({ status }: { status: LogEntry['status'] }) {
  switch (status) {
    case 'ERROR': return <ShieldAlert size={14} className="text-red-500" />;
    case 'SUCCESS': return <CheckCircle2 size={14} className="text-green-500" />;
    case 'SYSTEM': return <AlertTriangle size={14} className="text-yellow-500 shadow-yellow-500/20" />;
    default: return <Info size={14} className="text-cyan-600" />;
  }
}

function getStatusColor(status: LogEntry['status']) {
  switch (status) {
    case 'ERROR': return 'text-red-500';
    case 'SUCCESS': return 'text-green-400';
    case 'SYSTEM': return 'text-yellow-500';
    default: return 'text-cyan-600';
  }
}
