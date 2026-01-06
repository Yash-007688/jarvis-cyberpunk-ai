import React from 'react';
import CyberContainer from './components/CyberContainer';
import CoreSystem from './components/CoreSystem';
import VisualInput from './components/VisualInput';
import SystemMetrics from './components/SystemMetrics';
import Transcript from './components/Transcript';

function App() {
  return (
    <div className="min-h-screen bg-cyber-black text-cyber-cyan p-4 font-mono bg-[radial-gradient(circle_at_center,_#111111_0%,_#050505_100%)] overflow-hidden">
      {/* Background Matrix/Grid Effect (Optional) */}
      <div className="fixed inset-0 pointer-events-none bg-grid-pattern opacity-10"></div>

      {/* Main Grid Container */}
      <div className="relative z-10 grid grid-cols-12 grid-rows-12 gap-4 h-[calc(100vh-2rem)]">

        {/* HEADER */}
        <header className="col-span-12 row-span-1 flex items-center justify-between px-6 border-b border-cyber-cyan/30 bg-cyber-dark/80 backdrop-blur-md rounded-lg">
          <div className="flex items-center space-x-6">
            <div className="text-3xl font-display font-bold text-cyber-cyan text-glow tracking-tighter">JARVIS</div>
            <div className="h-6 w-px bg-cyber-cyan/50"></div>
            <div className="text-xs text-cyber-cyan/70 tracking-widest">SYSTEM_READY // ONLINE</div>
          </div>
          <div className="flex space-x-8 text-xs font-bold tracking-widest uppercase">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-cyber-green rounded-full shadow-neon-green animate-pulse"></span>
              <span className="text-cyber-green">Connected to Mainframe</span>
            </div>
            <div className="text-cyber-cyan/60">
              Lat: 28.6139° N
            </div>
          </div>
        </header>

        {/* LEFT COLUMN: Visual Input & Metrics */}
        <div className="col-span-3 row-span-11 flex flex-col gap-4">
          {/* Visual Input */}
          <CyberContainer title="VISUAL INPUT" className="h-2/5">
            <VisualInput />
          </CyberContainer>

          {/* System Metrics */}
          <CyberContainer title="SYSTEM METRICS" className="flex-1">
            <SystemMetrics />
          </CyberContainer>
        </div>

        {/* CENTER COLUMN: Core System */}
        <div className="col-span-6 row-span-11">
          <CyberContainer title="CORE SYSTEM" className="h-full">
            <CoreSystem />
          </CyberContainer>
        </div>

        {/* RIGHT COLUMN: Transcript/Chat */}
        <div className="col-span-3 row-span-11">
          <CyberContainer title="TRANSCRIPT" className="h-full">
            <Transcript />
          </CyberContainer>
        </div>

      </div>
    </div>
  );
}

export default App;
