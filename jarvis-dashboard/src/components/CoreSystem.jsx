import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere } from '@react-three/drei';
import * as THREE from 'three';

const ParticleSphere = ({ count = 3000 }) => {
    const mesh = useRef();

    // Generate random points on a sphere
    const particles = useMemo(() => {
        const temp = [];
        for (let i = 0; i < count; i++) {
            const phi = Math.acos(-1 + (2 * i) / count);
            const theta = Math.sqrt(count * Math.PI) * phi;

            const x = 3 * Math.cos(theta) * Math.sin(phi);
            const y = 3 * Math.sin(theta) * Math.sin(phi);
            const z = 3 * Math.cos(phi);

            temp.push(x, y, z);
        }
        return new Float32Array(temp);
    }, [count]);

    useFrame((state) => {
        if (mesh.current) {
            mesh.current.rotation.y += 0.002;
            mesh.current.rotation.x += 0.001;
        }
    });

    return (
        <points ref={mesh}>
            <bufferGeometry>
                <bufferAttribute
                    attach="attributes-position"
                    count={particles.length / 3}
                    array={particles}
                    itemSize={3}
                />
            </bufferGeometry>
            <pointsMaterial
                size={0.03}
                color="#00f3ff"
                sizeAttenuation
                transparent
                opacity={0.8}
                blending={THREE.AdditiveBlending}
            />
        </points>
    );
};

const CoreSystem = () => {
    return (
        <div className="w-full h-full relative overflow-hidden">
            {/* Background Grid/Effects */}
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_transparent_0%,_#000_100%)] z-10 pointer-events-none"></div>

            <Canvas camera={{ position: [0, 0, 8], fov: 45 }}>
                <ambientLight intensity={0.5} />
                <ParticleSphere />
                <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.5} />
            </Canvas>

            {/* Overlay Text */}
            <div className="absolute bottom-4 left-0 right-0 text-center z-20">
                <div className="text-cyber-cyan text-xs tracking-[0.3em] font-bold opacity-80 animate-pulse">
                    CORE SYSTEMS ACTIVE
                </div>
                <div className="text-cyber-green text-[10px] mt-1">
                    PROCESSING NEURAL NETWORKS
                </div>
            </div>
        </div>
    );
};

export default CoreSystem;
