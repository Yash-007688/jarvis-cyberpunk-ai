import React from 'react';

const CyberContainer = ({ children, title, className = '' }) => {
    return (
        <div className={`relative bg-cyber-panel border border-cyber-cyan/30 rounded-lg overflow-hidden flex flex-col backdrop-blur-md ${className}`}>
            {/* Corner Accents */}
            <div className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-cyber-cyan"></div>
            <div className="absolute top-0 right-0 w-2 h-2 border-t-2 border-r-2 border-cyber-cyan"></div>
            <div className="absolute bottom-0 left-0 w-2 h-2 border-b-2 border-l-2 border-cyber-cyan"></div>
            <div className="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-cyber-cyan"></div>

            {/* Header Line */}
            {title && (
                <div className="flex items-center px-4 py-2 border-b border-cyber-cyan/20 bg-cyber-dark/50">
                    <div className="w-2 h-2 bg-cyber-cyan rounded-full mr-2 animate-pulse"></div>
                    <h3 className="text-cyber-cyan font-display uppercase tracking-widest text-sm font-bold text-glow">
                        {title}
                    </h3>
                    <div className="flex-1 ml-4 h-px bg-gradient-to-r from-cyber-cyan/50 to-transparent"></div>
                </div>
            )}

            {/* Content */}
            <div className="flex-1 p-4 relative">
                {/* Scanline Effect Overlay (Optional, subtle) */}
                <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.1)_50%),linear-gradient(90deg,rgba(255,0,0,0.03),rgba(0,255,0,0.01),rgba(0,0,255,0.03))] z-0 bg-[length:100%_2px,3px_100%]"></div>
                <div className="relative z-10 w-full h-full">
                    {children}
                </div>
            </div>
        </div>
    );
};

export default CyberContainer;
