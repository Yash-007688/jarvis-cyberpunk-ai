import React from 'react';
import Webcam from 'react-webcam';

const VisualInput = () => {
    return (
        <div className="relative w-full h-full bg-black flex items-center justify-center overflow-hidden">
            {/* Webcam */}
            <Webcam
                audio={false}
                className="absolute inset-0 w-full h-full object-cover opacity-60"
                style={{ filter: 'grayscale(100%) contrast(1.2) brightness(0.8)' }}
            />

            {/* Scanline Overlay */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] z-10 bg-[length:100%_2px,3px_100%] pointer-events-none"></div>

            {/* HUD Elements */}
            <div className="absolute top-2 left-2 text-[10px] text-cyber-cyan z-20 font-bold">
                CAM_01 [REC]
            </div>

            {/* Face Tracking Mock-up Box */}
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32 border border-cyber-green/50 z-20 transition-all duration-300">
                <div className="absolute -top-1 -left-1 w-2 h-2 border-t border-l border-cyber-green"></div>
                <div className="absolute -top-1 -right-1 w-2 h-2 border-t border-r border-cyber-green"></div>
                <div className="absolute -bottom-1 -left-1 w-2 h-2 border-b border-l border-cyber-green"></div>
                <div className="absolute -bottom-1 -right-1 w-2 h-2 border-b border-r border-cyber-green"></div>

                <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 text-[8px] text-cyber-green whitespace-nowrap bg-black/50 px-1">
                    TARGET DETECTED
                </div>
            </div>
        </div>
    );
};

export default VisualInput;
