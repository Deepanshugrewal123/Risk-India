import React, { useEffect, useRef } from 'react';
import { useCrisis } from '../../context/CrisisContext';

interface Particle {
  x: number;
  y: number;
  originX: number;
  originY: number;
  vx: number;
  vy: number;
  baseRadius: number;
  colorType: 'orange' | 'green' | 'slate' | 'light' | 'cross' | 'coord';
  label?: string;
  mass: number;
  layer: 1 | 2 | 3 | 4; // Parallax depth layer
}

interface ParticleFieldCanvasProps {
  className?: string;
  particleCount?: number;
  isHero?: boolean;
}

export const ParticleFieldCanvas: React.FC<ParticleFieldCanvasProps> = ({
  className = '',
  particleCount = 56,
  isHero = false,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const { isCrisisMode } = useCrisis();

  useEffect(() => {
    // If in crisis mode, completely suppress canvas rendering & animation frame loops
    if (isCrisisMode) return;

    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Check motion preference dynamically
    const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    let prefersReducedMotion = motionQuery.matches;

    const handleMotionChange = (e: MediaQueryListEvent) => {
      prefersReducedMotion = e.matches;
    };
    motionQuery.addEventListener?.('change', handleMotionChange);

    let animationFrameId: number;
    let width = (canvas.width = canvas.parentElement?.clientWidth || window.innerWidth);
    let height = (canvas.height = canvas.parentElement?.clientHeight || window.innerHeight);

    // Mouse tracking with smooth lerping
    const mouse = {
      x: -1000,
      y: -1000,
      targetX: -1000,
      targetY: -1000,
      vx: 0,
      vy: 0,
      radius: isHero ? 240 : 200,
      strength: isHero ? 6.2 : 4.5,
    };

    // Parallax camera offset
    const camera = {
      x: 0,
      y: 0,
      targetX: 0,
      targetY: 0,
    };

    // Real Indian coordinates and geospatial markers for subtle identity
    const geoCoordinates = [
      '26.1°N 91.7°E', // Guwahati / Assam
      '31.7°N 76.9°E', // Mandi / HP
      '19.8°N 85.8°E', // Puri / Odisha
      '11.6°N 76.1°E', // Wayanad / Kerala
      '26.1°N 86.6°E', // Supaul / Bihar
      '30.5°N 79.5°E', // Chamoli / UK
      '28.6°N 77.2°E', // New Delhi
      '19.0°N 72.8°E', // Mumbai
      '23.2°N 77.4°E', // Central Plateau
      '+',
      '×',
      '○',
      '▲',
    ];

    // Colors: Clearly visible, warm burnt orange, deep muted sage green, charcoal slate, light neutral
    const colorStyles = {
      orange: {
        fill: 'rgba(217, 95, 28, 0.72)', // Rich burnt orange
        stroke: 'rgba(234, 88, 12, 0.85)',
        highlight: 'rgba(217, 95, 28, 0.95)',
      },
      green: {
        fill: 'rgba(24, 138, 86, 0.68)', // Deep muted forest sage
        stroke: 'rgba(16, 185, 129, 0.82)',
        highlight: 'rgba(24, 138, 86, 0.92)',
      },
      slate: {
        fill: 'rgba(40, 44, 52, 0.42)', // Crisp charcoal/slate
        stroke: 'rgba(25, 28, 34, 0.55)',
        highlight: 'rgba(20, 22, 28, 0.75)',
      },
      light: {
        fill: 'rgba(180, 182, 175, 0.65)', // Off-white / paper stone
        stroke: 'rgba(160, 162, 155, 0.80)',
        highlight: 'rgba(120, 122, 115, 0.90)',
      },
    };

    const particles: Particle[] = [];
    const count = Math.min(particleCount, width < 768 ? 24 : particleCount);

    for (let i = 0; i < count; i++) {
      const x = Math.random() * width;
      const y = Math.random() * height;

      // Distribution: 30% Orange, 25% Green, 25% Slate, 20% Coordinate/Cross
      const rand = Math.random();
      let colorType: Particle['colorType'] = 'slate';
      let layer: Particle['layer'] = 2;
      let label: string | undefined = undefined;
      let baseRadius = Math.random() * 2.5 + 2.5;

      if (rand < 0.28) {
        colorType = 'orange';
        layer = 3;
        baseRadius = Math.random() * 2.8 + 3.0; // Noticeable accent node
      } else if (rand < 0.52) {
        colorType = 'green';
        layer = 3;
        baseRadius = Math.random() * 2.6 + 2.8; // Secondary accent node
      } else if (rand < 0.76) {
        colorType = 'slate';
        layer = 2;
        baseRadius = Math.random() * 2.0 + 2.2;
      } else {
        colorType = rand < 0.88 ? 'coord' : 'cross';
        layer = 4;
        label = geoCoordinates[Math.floor(Math.random() * geoCoordinates.length)];
        baseRadius = 3;
      }

      particles.push({
        x,
        y,
        originX: x,
        originY: y,
        vx: (Math.random() - 0.5) * 0.45,
        vy: (Math.random() - 0.5) * 0.45,
        baseRadius,
        colorType,
        label,
        mass: Math.random() * 1.5 + 0.8,
        layer,
      });
    }

    // Resize handling with proportional particle redistribution
    const handleResize = () => {
      if (!canvas || !canvas.parentElement) return;
      const newWidth = canvas.parentElement.clientWidth || window.innerWidth;
      const newHeight = canvas.parentElement.clientHeight || window.innerHeight;
      if (newWidth <= 0 || newHeight <= 0) return;
      if (newWidth === width && newHeight === height) return;

      const scaleX = width > 0 ? newWidth / width : 1;
      const scaleY = height > 0 ? newHeight / height : 1;

      width = canvas.width = newWidth;
      height = canvas.height = newHeight;

      particles.forEach((p) => {
        p.originX = Math.max(15, Math.min(width - 15, p.originX * scaleX));
        p.originY = Math.max(15, Math.min(height - 15, p.originY * scaleY));
        p.x = Math.max(15, Math.min(width - 15, p.x * scaleX));
        p.y = Math.max(15, Math.min(height - 15, p.y * scaleY));
      });
    };

    // Smooth pointer/mouse position tracking with canvas bounding check
    const updatePointer = (clientX: number, clientY: number) => {
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      const isInside =
        clientX >= rect.left - 60 &&
        clientX <= rect.right + 60 &&
        clientY >= rect.top - 60 &&
        clientY <= rect.bottom + 60;

      if (isInside) {
        mouse.targetX = clientX - rect.left;
        mouse.targetY = clientY - rect.top;

        const centerX = width / 2;
        const centerY = height / 2;
        camera.targetX = ((clientX - centerX) / (centerX || 1)) * (isHero ? 28 : 16);
        camera.targetY = ((clientY - centerY) / (centerY || 1)) * (isHero ? 24 : 14);
      } else {
        mouse.targetX = -1000;
        mouse.targetY = -1000;
        camera.targetX = 0;
        camera.targetY = 0;
      }
    };

    const handlePointerMove = (e: PointerEvent) => {
      updatePointer(e.clientX, e.clientY);
    };

    const handleMouseMove = (e: MouseEvent) => {
      updatePointer(e.clientX, e.clientY);
    };

    const handlePointerLeave = () => {
      mouse.targetX = -1000;
      mouse.targetY = -1000;
      camera.targetX = 0;
      camera.targetY = 0;
    };

    window.addEventListener('resize', handleResize);
    window.addEventListener('pointermove', handlePointerMove, { passive: true });
    window.addEventListener('mousemove', handleMouseMove, { passive: true });
    window.addEventListener('pointerleave', handlePointerLeave);
    window.addEventListener('pointercancel', handlePointerLeave);
    window.addEventListener('pointerup', handlePointerLeave);
    window.addEventListener('touchend', handlePointerLeave, { passive: true });
    window.addEventListener('touchcancel', handlePointerLeave, { passive: true });
    window.addEventListener('blur', handlePointerLeave);
    document.addEventListener('mouseleave', handlePointerLeave);

    const parentEl = canvas.parentElement;
    let resizeObserver: ResizeObserver | null = null;
    if (typeof ResizeObserver !== 'undefined' && parentEl) {
      resizeObserver = new ResizeObserver(() => {
        handleResize();
      });
      resizeObserver.observe(parentEl);
    }

    // Subtle background contour geometry (Layer 1)
    const drawBackgroundContours = (camX: number, camY: number) => {
      ctx.save();
      ctx.strokeStyle = 'rgba(18, 19, 22, 0.055)';
      ctx.lineWidth = 1;

      // Subtle India-inspired latitude/longitude arcs
      const offsetL1X = camX * 0.25;
      const offsetL1Y = camY * 0.25;

      ctx.beginPath();
      // Wave contour 1
      ctx.moveTo(0, height * 0.35 + offsetL1Y);
      ctx.bezierCurveTo(
        width * 0.35 + offsetL1X,
        height * 0.25 + offsetL1Y,
        width * 0.65 - offsetL1X,
        height * 0.48 + offsetL1Y,
        width,
        height * 0.38 + offsetL1Y
      );
      ctx.stroke();

      // Wave contour 2
      ctx.beginPath();
      ctx.moveTo(0, height * 0.68 + offsetL1Y);
      ctx.bezierCurveTo(
        width * 0.28 - offsetL1X,
        height * 0.78 + offsetL1Y,
        width * 0.72 + offsetL1X,
        height * 0.58 + offsetL1Y,
        width,
        height * 0.72 + offsetL1Y
      );
      ctx.stroke();

      // Faint central India coordinate axis marker
      if (isHero) {
        ctx.strokeStyle = 'rgba(18, 19, 22, 0.07)';
        ctx.beginPath();
        const axX = width * 0.5 + offsetL1X;
        const axY = height * 0.45 + offsetL1Y;
        ctx.moveTo(axX - 18, axY);
        ctx.lineTo(axX + 18, axY);
        ctx.moveTo(axX, axY - 18);
        ctx.lineTo(axX, axY + 18);
        ctx.stroke();
      }

      ctx.restore();
    };

    // Render loop
    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Lerp mouse cursor position smoothly
      mouse.x += (mouse.targetX - mouse.x) * 0.14;
      mouse.y += (mouse.targetY - mouse.y) * 0.14;

      // Lerp camera parallax
      camera.x += (camera.targetX - camera.x) * 0.08;
      camera.y += (camera.targetY - camera.y) * 0.08;

      // Draw Layer 1: Geospatial contour curves
      drawBackgroundContours(camera.x, camera.y);

      // Connecting lines between nearby nodes with cursor proximity illumination
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const pi = particles[i];
          const pj = particles[j];
          const dx = pi.x - pj.x;
          const dy = pi.y - pj.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 130) {
            // Check distance of line midpoint to mouse cursor
            const midX = (pi.x + pj.x) / 2;
            const midY = (pi.y + pj.y) / 2;
            const distToMouse = Math.sqrt((mouse.x - midX) ** 2 + (mouse.y - midY) ** 2);

            let alpha = (1 - dist / 130) * 0.12;
            // Noticeable proximity illumination when cursor approaches
            if (distToMouse < mouse.radius && !prefersReducedMotion) {
              const mouseFactor = (mouse.radius - distToMouse) / mouse.radius;
              alpha += mouseFactor * 0.32; // Significantly brighter near cursor!
            }

            ctx.beginPath();
            ctx.strokeStyle = `rgba(28, 30, 36, ${alpha})`;
            ctx.lineWidth = alpha > 0.2 ? 1.2 : 0.8;
            ctx.moveTo(pi.x, pi.y);
            ctx.lineTo(pj.x, pj.y);
            ctx.stroke();
          }
        }
      }

      // Update & render particles
      particles.forEach((p) => {
        // Natural harmonic float
        p.x += p.vx;
        p.y += p.vy;

        // Bounce gently off boundaries
        if (p.x < 15 || p.x > width - 15) p.vx *= -1;
        if (p.y < 15 || p.y > height - 15) p.vy *= -1;

        // Parallax offset per layer
        const layerMultiplier = p.layer === 4 ? 0.85 : p.layer === 3 ? 0.60 : 0.35;
        const targetHomeX = p.originX + camera.x * layerMultiplier;
        const targetHomeY = p.originY + camera.y * layerMultiplier;

        // Cursor proximity physics
        const dx = mouse.x - p.x;
        const dy = mouse.y - p.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        let currentScale = 1.0;
        let isHovered = false;

        if (distance < mouse.radius && distance > 0 && !prefersReducedMotion) {
          isHovered = true;
          const proximity = (mouse.radius - distance) / mouse.radius;
          const angle = Math.atan2(dy, dx);

          // Noticeable organic displacement (repulsion force)
          const pushForce = proximity * mouse.strength * (1.2 / p.mass);
          p.x -= Math.cos(angle) * pushForce;
          p.y -= Math.sin(angle) * pushForce;

          // Scale node up noticeably near cursor (1.0 -> 1.42x)
          currentScale = 1.0 + proximity * 0.42;
        } else {
          // Smooth return spring toward home target
          p.x += (targetHomeX - p.x) * 0.008;
          p.y += (targetHomeY - p.y) * 0.008;
        }

        // Render the node
        ctx.save();
        const style =
          p.colorType === 'orange'
            ? colorStyles.orange
            : p.colorType === 'green'
            ? colorStyles.green
            : p.colorType === 'slate'
            ? colorStyles.slate
            : colorStyles.light;

        const effectiveRadius = p.baseRadius * currentScale;

        if (p.colorType === 'coord' && p.label) {
          // Render coordinate / telemetry badge
          ctx.font = '10px "JetBrains Mono", monospace';
          ctx.fillStyle = isHovered ? 'rgba(18, 19, 22, 0.95)' : 'rgba(40, 44, 52, 0.55)';
          ctx.fillText(p.label, p.x + 4, p.y - 4);

          // Small crosshair point
          ctx.fillStyle = isHovered ? colorStyles.orange.fill : 'rgba(18, 19, 22, 0.50)';
          ctx.beginPath();
          ctx.arc(p.x, p.y, 2 * currentScale, 0, Math.PI * 2);
          ctx.fill();
        } else if (p.colorType === 'cross') {
          // Render crosshair marker
          ctx.strokeStyle = isHovered ? colorStyles.orange.stroke : style.stroke;
          ctx.lineWidth = 1.2;
          const s = 4 * currentScale;
          ctx.beginPath();
          ctx.moveTo(p.x - s, p.y);
          ctx.lineTo(p.x + s, p.y);
          ctx.moveTo(p.x, p.y - s);
          ctx.lineTo(p.x, p.y + s);
          ctx.stroke();
        } else {
          // Circular particle node (orange, green, or slate)
          ctx.fillStyle = isHovered ? style.highlight : style.fill;
          ctx.strokeStyle = style.stroke;
          ctx.lineWidth = 1;

          ctx.beginPath();
          ctx.arc(p.x, p.y, effectiveRadius, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();

          // Subtle outer halo ring on hovered or accent nodes
          if (isHovered && (p.colorType === 'orange' || p.colorType === 'green')) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, effectiveRadius * 1.7, 0, Math.PI * 2);
            ctx.strokeStyle = p.colorType === 'orange' ? 'rgba(217, 95, 28, 0.28)' : 'rgba(24, 138, 86, 0.25)';
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }

        ctx.restore();
      });

      animationFrameId = requestAnimationFrame(render);
    };

    animationFrameId = requestAnimationFrame(render);

    return () => {
      cancelAnimationFrame(animationFrameId);
      motionQuery.removeEventListener?.('change', handleMotionChange);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('pointerleave', handlePointerLeave);
      window.removeEventListener('pointercancel', handlePointerLeave);
      window.removeEventListener('pointerup', handlePointerLeave);
      window.removeEventListener('touchend', handlePointerLeave);
      window.removeEventListener('touchcancel', handlePointerLeave);
      window.removeEventListener('blur', handlePointerLeave);
      document.removeEventListener('mouseleave', handlePointerLeave);
      if (resizeObserver) {
        resizeObserver.disconnect();
      }
    };
  }, [particleCount, isHero, isCrisisMode]);

  if (isCrisisMode) {
    return null;
  }

  return (
    <canvas
      ref={canvasRef}
      className={`pointer-events-none absolute inset-0 w-full h-full ${className}`}
      aria-hidden="true"
    />
  );
};
