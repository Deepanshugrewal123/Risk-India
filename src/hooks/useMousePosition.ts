import { useState, useEffect } from 'react';

export interface MousePosition {
  x: number;
  y: number;
  normalizedX: number; // -1 to 1
  normalizedY: number; // -1 to 1
  isTouch: boolean;
  prefersReducedMotion: boolean;
}

export const useMousePosition = (): MousePosition => {
  const [position, setPosition] = useState<MousePosition>({
    x: 0,
    y: 0,
    normalizedX: 0,
    normalizedY: 0,
    isTouch: false,
    prefersReducedMotion: false,
  });

  useEffect(() => {
    // Check user preference for reduced motion
    const motionMediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const isReduced = motionMediaQuery.matches;

    // Detect touch device
    const isTouchDevice =
      'ontouchstart' in window || navigator.maxTouchPoints > 0;

    setPosition((prev) => ({
      ...prev,
      isTouch: isTouchDevice,
      prefersReducedMotion: isReduced,
    }));

    if (isTouchDevice || isReduced) {
      return;
    }

    let animationFrameId: number;
    let targetX = window.innerWidth / 2;
    let targetY = window.innerHeight / 2;

    const handleMouseMove = (e: MouseEvent) => {
      targetX = e.clientX;
      targetY = e.clientY;
    };

    const updatePosition = () => {
      const normX = (targetX / window.innerWidth) * 2 - 1;
      const normY = (targetY / window.innerHeight) * 2 - 1;

      setPosition((prev) => ({
        ...prev,
        x: targetX,
        y: targetY,
        normalizedX: normX,
        normalizedY: normY,
      }));

      animationFrameId = requestAnimationFrame(updatePosition);
    };

    window.addEventListener('mousemove', handleMouseMove, { passive: true });
    animationFrameId = requestAnimationFrame(updatePosition);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return position;
};
