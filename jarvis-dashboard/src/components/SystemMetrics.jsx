import React, { useState, useEffect } from 'react';

const SystemMetrics = () => {
    const [cpu, setCpu] = useState(16);
    const [ram, setRam] = useState(42);
    const [net, setNet] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setCpu(Math.floor(Math.random() * 20) + 10);
            setRam(Math.floor(Math.random() * 10) + 40);
            setNet(Math.floor(Math.random() * 100));
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="flex flex-col h-full justify-between py-2">
            {/* Resource Bars */}
            <div className="space-y-6">
                {/* CPU */}
                <div>
                    <div className="flex justify-between text-xs mb-1 font-bold tracking-wider">
                        <span className="text-cyber-cyan">CPU LOAD</span>
                        <span className="text-cyber-green">{cpu}%</span>
                    </div>
                    <div className="h-2 w-full bg-cyber-dark border border-cyber-cyan/30 rounded-sm overflow-hidden">
                        <div
                            className="h-full bg-cyber-cyan shadow-neon-cyan transition-all duration-500 ease-out"
                            style={{ width: `${cpu}%` }}
                        ></div>
                    </div>
                </div>

                {/* RAM */}
                <div>
                    <div className="flex justify-between text-xs mb-1 font-bold tracking-wider">
                        <span className="text-cyber-cyan">RAM USAGE</span>
                        <span className="text-cyber-green">{ram}%</span>
                    </div>
                    <div className="h-2 w-full bg-cyber-dark border border-cyber-cyan/30 rounded-sm overflow-hidden">
                        <div
                            className="h-full bg-cyber-green shadow-neon-green transition-all duration-500 ease-out"
                            style={{ width: `${ram}%` }}
                        ></div>
                    </div>
                </div>
            </div>

            {/* Circular Graphics / Decor */}
            <div className="grid grid-cols-2 gap-4 mt-4">
                <div className="flex flex-col items-center justify-center p-2 bg-cyber-dark/30 border border-cyber-cyan/10 rounded">
                    <div className="text-[10px] text-cyber-cyan/70 mb-1">NETWORK</div>
                    <div className="text-xl font-bold text-cyber-green">{net} <span className="text-xs text-cyber-cyan/50">mbps</span></div>
                    <div className="text-[9px] text-cyber-red animate-pulse mt-1">UPLINK ACTIVE</div>
                </div>

                <div className="flex items-center justify-center relative">
                    <svg viewBox="0 0 100 100" className="w-20 h-20 animate-[spin_4s_linear_infinite]">
                        <circle cx="50" cy="50" r="40" stroke="#111" strokeWidth="4" fill="none" />
                        <path d="M50 10 A40 40 0 0 1 90 50" stroke="#00f3ff" strokeWidth="4" fill="none" className="drop-shadow-[0_0_5px_rgba(0,243,255,0.8)]" />
                    </svg>
                    <div className="absolute font-bold text-xs text-cyber-cyan">
                        98%
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SystemMetrics;
