import React, { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, Html } from '@react-three/drei';
import * as THREE from 'three';

interface GRNA {
  start: number;
  score: number;
}

interface DNAHelix3DProps {
  geneLength: number;
  grnas: GRNA[];
}

// Generate points for a single helix
function generateHelixPoints(turns: number, pointsPerTurn: number, radius: number, pitch: number, phase: number = 0) {
  const points: [number, number, number][] = [];
  const totalPoints = turns * pointsPerTurn;
  for (let i = 0; i < totalPoints; i++) {
    const t = (i / pointsPerTurn) * 2 * Math.PI;
    const x = radius * Math.cos(t + phase);
    const y = radius * Math.sin(t + phase);
    const z = (pitch * t) / (2 * Math.PI);
    points.push([x, y, z]);
  }
  return points;
}

// Helper to get color for highlighted base pairs
function isHighlighted(idx: number, highlightIndices: number[]) {
  return highlightIndices.includes(idx);
}

// Animated group for slow rotation
const AnimatedGroup: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const group = useRef<THREE.Group>(null);
  useFrame((state, delta) => {
    if (group.current) {
      group.current.rotation.y += delta * 0.2; // slow rotation
    }
  });
  return <group ref={group}>{children}</group>;
};

export const DNAHelix3D: React.FC<DNAHelix3DProps> = ({ geneLength, grnas }) => {
  // Helix parameters
  const turns = 10;
  const pointsPerTurn = 100;
  const radius = 2;
  const pitch = 1.5;

  // Generate double helix points
  const helixA = generateHelixPoints(turns, pointsPerTurn, radius, pitch, 0);
  const helixB = generateHelixPoints(turns, pointsPerTurn, radius, pitch, Math.PI);

  // Map gRNA start positions to helix indices
  const totalPoints = turns * pointsPerTurn;
  const gRNAIndices = grnas.map(g => Math.floor((g.start / geneLength) * (totalPoints - 1)));

  // For each base pair, create a rung (cylinder) between helixA and helixB
  const basePairs = helixA.map((a, i) => {
    const b = helixB[i];
    const isGRNA = isHighlighted(i, gRNAIndices);
    return { a, b, isGRNA };
  });

  // Tooltip state
  const [hoveredIdx, setHoveredIdx] = useState<number | null>(null);

  return (
    <div style={{ width: '100%', height: 400 }}>
      <Canvas camera={{ position: [0, -10, 10], fov: 60 }}>
        <ambientLight intensity={0.7} />
        <directionalLight position={[10, 10, 10]} intensity={0.7} />
        <AnimatedGroup>
          {/* Helix A */}
          <mesh>
            <tubeGeometry
              args={[
                new THREE.CatmullRomCurve3(helixA.map(p => new THREE.Vector3(...p))),
                helixA.length * 2,
                0.13,
                8,
                false,
              ]}
            />
            <meshStandardMaterial color="#1565c0" />
          </mesh>
          {/* Helix B */}
          <mesh>
            <tubeGeometry
              args={[
                new THREE.CatmullRomCurve3(helixB.map(p => new THREE.Vector3(...p))),
                helixB.length * 2,
                0.13,
                8,
                false,
              ]}
            />
            <meshStandardMaterial color="#43a047" />
          </mesh>
          {/* Base pairs (rungs) */}
          {basePairs.map(({ a, b, isGRNA }, i) => (
            <mesh key={i} position={[(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2]}>
              <cylinderGeometry args={[0.06, 0.06, Math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2), 8]} />
              <meshStandardMaterial color={isGRNA ? '#ffd600' : '#bdbdbd'} emissive={isGRNA ? '#ffd600' : '#000'} emissiveIntensity={isGRNA ? 0.7 : 0} />
            </mesh>
          ))}
          {/* gRNA highlights (glowing spheres with tooltip) */}
          {gRNAIndices.map((idx, i) => (
            <Sphere
              key={i}
              args={[0.28, 32, 32]}
              position={helixA[idx]}
              onPointerOver={() => setHoveredIdx(i)}
              onPointerOut={() => setHoveredIdx(null)}
            >
              <meshStandardMaterial color="#ff1744" emissive="#ff1744" emissiveIntensity={0.8} />
              {hoveredIdx === i && (
                <Html distanceFactor={10} style={{ pointerEvents: 'none', background: 'rgba(255,255,255,0.95)', borderRadius: 6, padding: '6px 12px', color: '#222', fontWeight: 500, fontSize: 14, boxShadow: '0 2px 8px #0002' }}>
                  <div>
                    <div>gRNA Rank: {i + 1}</div>
                    <div>Start: {grnas[i].start}</div>
                    <div>Score: {grnas[i].score}</div>
                  </div>
                </Html>
              )}
            </Sphere>
          ))}
        </AnimatedGroup>
        <OrbitControls />
      </Canvas>
    </div>
  );
}; 