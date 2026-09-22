import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { useCrisis } from '../../context/CrisisContext';

interface TiltCardProps {
  children: React.ReactNode;
  className?: string;
  maxTilt?: number; // default 1.5 degrees
  onClick?: () => void;
}

export const TiltCard: React.FC<TiltCardProps> = ({
  children,
  className = '',
  maxTilt = 1.5,
  onClick,
}) => {
  const { isCrisisMode } = useCrisis();
  const cardRef = useRef<HTMLDivElement | null>(null);
  const [rotateX, setRotateX] = useState(0);
  const [rotateY, setRotateY] = useState(0);

  // If in crisis mode, bypass motion physics entirely to save battery and GPU cycles
  if (isCrisisMode) {
    return (
      <div
        ref={cardRef}
        onClick={onClick}
        className={className}
      >
        {children}
      </div>
    );
  }

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    const mouseX = e.clientX - centerX;
    const mouseY = e.clientY - centerY;

    // Normalize: -1 to 1
    const normX = mouseX / (rect.width / 2);
    const normY = mouseY / (rect.height / 2);

    // Subtle 1-2 degrees maximum
    setRotateX(-normY * maxTilt);
    setRotateY(normX * maxTilt);
  };

  const handleMouseLeave = () => {
    setRotateX(0);
    setRotateY(0);
  };

  return (
    <motion.div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onClick={onClick}
      animate={{
        rotateX,
        rotateY,
      }}
      transition={{
        type: 'spring',
        stiffness: 280,
        damping: 24,
        mass: 0.6,
      }}
      style={{
        transformStyle: 'preserve-3d',
        perspective: 1000,
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
};
