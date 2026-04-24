"use client";

import React from 'react';
import { 
  ShieldCheck, 
  Settings, 
  HardDrive, 
  FileText, 
  Lock, 
  RefreshCw,
  TrendingUp,
  Fingerprint
} from 'lucide-react';

interface ControlPanelProps {
  isProcessing: boolean;
  onReset: () => void;
}

export default function ControlPanel({ isProcessing, onReset }: ControlPanelProps) {
  return (
    <div className="space-y-6">
      
      {/* 1. SYSTEM INTEGRITY CARD */}
      <section className="glass-panel p-5 relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-2 opacity-10 group-hover:opacity-20 transition-opacity">
          <Fingerprint size={40} className="text-cyan-400" />
        </div>
        
        <h3 className="text-[10px] font-black text-cyan-700 uppercase tracking-[0.3em] mb-4 flex items-center gap-2">
          <ShieldCheck size={14} className="text-cyan-500" />
          Integrity_Protocol
        </h3>

        <div className="space-y-3">
          <StatusRow label="Neural_Link" status="Stable" color="text-green-400" />
          <StatusRow label="Encryption" status="AES-256" color="text-blue-400" />
          <StatusRow label="Groq_LPU" status={isProcessing ? "High_Load" : "Optimal"} color={isProcessing ? "text-yellow-400" : "text-green-400"} />
        </div>

        <button 
          onClick={onReset}
          className="w-full mt-4 py-2 border border-cyan-900/50 rounded-lg text-[10px] font-bold uppercase tracking-widest text-cyan-600 hover:bg-cyan-500/10 hover:text-cyan-400 transition-all flex items-center justify-center gap-2"
        >
          <RefreshCw size={12} className={isProcessing ? "animate-spin" : ""} />
          Purge_Memory_Buffer
        </button>
      </section>

      {/* 2. ASSET VAULT (For generated reports/PDFs) */}
      <section className="glass-panel p-5">
        <h3 className="text-[10px] font-black text-cyan-700 uppercase tracking-[0.3em] mb-4 flex items-center gap-2">
          <HardDrive size={14} className="text-cyan-500" />
          Asset_Vault
        </h3>
        
        <div className="space-y-2">
          <AssetItem name="last_audit_report.pdf" type="Report" size="1.2MB" />
          <AssetItem name="market_analysis.json" type="Data" size="44KB" />
          <div className="p-3 border border-dashed border-cyan-900/30 rounded-lg flex flex-col items-center justify-center opacity-40">
            <Lock size={16} className="text-cyan-900 mb-1" />
            <span className="text-[8px] uppercase tracking-tighter">Encrypted Segment</span>
          </div>
        </div>
      </section>

      {/* 3. PERFORMANCE MONITOR */}
      <section className="glass-panel p-5 bg-gradient-to-br from-slate-900/40 to-cyan-900/10">
        <div className="flex justify-between items-center mb-2">
          <span className="text-[10px] font-bold text-cyan-800 uppercase tracking-widest flex items-center gap-1">
            <TrendingUp size={12} /> Resource_Load
          </span>
          <span className="text-[10px] font-mono text-cyan-400">42%</span>
        </div>
        <div className="w-full bg-black/50 h-1 rounded-full overflow-hidden">
          <div 
            className="bg-cyan-500 h-full transition-all duration-1000" 
            style={{ width: isProcessing ? '85%' : '42%' }}
          />
        </div>
      </section>

    </div>
  );
}

// --- SUB-COMPONENTS ---

function StatusRow({ label, status, color }: { label: string, status: string, color: string }) {
  return (
    <div className="flex justify-between items-center text-[11px] font-mono">
      <span className="text-slate-500 uppercase">{label}:</span>
      <span className={`${color} font-bold uppercase tracking-tighter`}>{status}</span>
    </div>
  );
}

function AssetItem({ name, type, size }: { name: string, type: string, size: string }) {
  return (
    <div className="group flex items-center justify-between p-2 bg-black/20 border border-white/5 rounded-lg hover:border-cyan-500/30 transition-all cursor-pointer">
      <div className="flex items-center gap-3">
        <FileText size={14} className="text-cyan-700 group-hover:text-cyan-400" />
        <div className="flex flex-col">
          <span className="text-[10px] text-cyan-100 font-medium truncate w-32">{name}</span>
          <span className="text-[8px] text-slate-500 uppercase">{type} • {size}</span>
        </div>
      </div>
      <Settings size={12} className="text-slate-700 group-hover:text-cyan-500" />
    </div>
  );
}
