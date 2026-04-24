"use client";

import React, { useState, useEffect } from 'react';
import { 
  Cpu, 
  Globe, 
  ShieldCheck, 
  Activity, 
  Wifi, 
  Lock, 
  Zap
} from 'lucide-react';

interface HudHeaderProps {
  status: 'IDLE' | 'EXECUTING' | 'ERROR';
}

export default function HudHeader({ status }: HudHeaderProps) {
  const [time, setTime] = useState('');
  const [latency, setLatency] = useState('24ms');

  // Update Clock
  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      setTime(now.toLocaleTimeString('en-GB', { hour12: false }));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Simulate Network Jitter for Realism
  useEffect(() => {
    const jitter = setInterval(() => {
      const ms = Math.floor(Math.random() * (45 - 18) + 18);
      setLatency(`${ms}ms`);
    }, 3000);
    return () => clearInterval(jitter);
  }, []);

  return (
    <header className="glass-panel flex flex-col md:flex-row items-center justify-between px-8 py-4 z-20 gap-4">
      
      {/* LEFT: CORE IDENTITY */}
      <div className="flex items-center gap-5">
        <div className="relative">
          <div className={`p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 ${status === 'EXECUTING' ? 'animate-pulse' : ''}`}>
            <Cpu className="text-cyan-400" size={28} />
          </div>
          {/* Animated Orbitals */}
          <div className="absolute inset-0 border border-cyan-500/20 rounded-full animate-[ping_3s_linear_infinite]" />
        </div>
        
        <div className="flex flex-col">
          <h1 className="text-2xl font-black tracking-[0.4em] neon-text uppercase italic flex items-center gap-2">
            V.E.R.A. <span className="text-[10px] tracking-widest text-cyan-700 mt-1">v3.0.4_BETA</span>
          </h1>
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1 text-[9px] font-bold text-cyan-600 uppercase tracking-widest">
              <span className={`w-1.5 h-1.5 rounded-full ${status === 'EXECUTING' ? 'bg-yellow-500 shadow-[0_0_8px_#eab308]' : 'bg-green-500 shadow-[0_0_8px_#22c55e]'}`} />
              System_State: {status}
            </span>
            <span className="text-[9px] text-slate-700 px-2 border-l border-slate-800">
              LOC: PRAYAGRAJ_NODE_01
            </span>
          </div>
        </div>
      </div>

      {/* CENTER: LIVE METRICS */}
      <div className="hidden lg:flex items-center gap-10 px-10 border-x border-cyan-900/20">
        <MetricItem icon={<Wifi size={14}/>} label="UPLINK" val={latency} color="text-cyan-400" />
        <MetricItem icon={<Lock size={14}/>} label="AUTH" val="GROQ_RSA" color="text-blue-400" />
        <MetricItem icon={<Zap size={14}/>} label="LPU_LOAD" val={status === 'EXECUTING' ? "88%" : "12%"} color={status === 'EXECUTING' ? "text-yellow-400" : "text-green-500"} />
      </div>

      {/* RIGHT: CHRONO & SECURITY */}
      <div className="flex items-center gap-6">
        <div className="flex flex-col items-end">
          <span className="text-[10px] font-black text-cyan-800 uppercase tracking-tighter flex items-center gap-1">
            <ShieldCheck size={12} className="text-cyan-600" /> Security_Level: 05
          </span>
          <span className="text-lg font-mono font-bold text-cyan-100 tracking-tighter">
            {time || "00:00:00"}
          </span>
        </div>
        
        <div className="h-10 w-[1px] bg-slate-800 hidden md:block" />
        
        <div className="flex items-center gap-3 bg-black/40 px-4 py-2 rounded-lg border border-white/5">
          <Activity size={18} className="text-cyan-500" />
          <div className="flex flex-col">
            <span className="text-[8px] font-bold text-slate-500 uppercase">Heartbeat</span>
            <span className="text-[10px] font-mono text-cyan-400">ACTIVE</span>
          </div>
        </div>
      </div>

    </header>
  );
}

// --- SUB-COMPONENT ---

function MetricItem({ icon, label, val, color }: { icon: React.ReactNode, label: string, val: string, color: string }) {
  return (
    <div className="flex flex-col items-center group cursor-default">
      <div className="flex items-center gap-1 text-[9px] font-black text-slate-500 uppercase tracking-tighter group-hover:text-cyan-600 transition-colors">
        {icon} {label}
      </div>
      <span className={`text-[12px] font-mono font-bold tracking-widest ${color}`}>{val}</span>
    </div>
  );
}
