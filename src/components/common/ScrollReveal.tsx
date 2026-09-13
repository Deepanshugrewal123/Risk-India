import React, { useEffect, useRef, useState } from 'react';

interface ScrollRevealProps {
  children: React.ReactNode;
  className?: string;
  delay?: number;
  direction?: 'up' | 'none';
}

export const ScrollReveal: React.FC<ScrollRevealProps> = ({
  children,
  className = '',
  delay = 0,
  direction = 'up',
}) => {
  const ref = useRef<HTMLDivElement | null>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    // Respect reduced motion preference
    const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (motionQuery.matches) {
      setIsVisible(true);
      return;
    }

    const handleMotionChange = (e: MediaQueryListEvent) => {
      if (e.matches) {
        setIsVisible(true);
      }
    };
    motionQuery.addEventListener?.('change', handleMotionChange);

    // Fail-safe timeout: ensure content is never permanently hidden if observer fails or stalls
    const failsafeTimer = setTimeout(() => {
      setIsVisible(true);
    }, 10000);

    // Fallback if IntersectionObserver is not supported
    if (typeof IntersectionObserver === 'undefined') {
      setIsVisible(true);
      clearTimeout(failsafeTimer);
      return;
    }

    // Scroll listener fallback in case IntersectionObserver is stalled by mobile browser quirks
    const handleScrollFallback = () => {
      if (!el) return;
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 20) {
        setIsVisible(true);
        clearTimeout(failsafeTimer);
        window.removeEventListener('scroll', handleScrollFallback);
      }
    };
    window.addEventListener('scroll', handleScrollFallback, { passive: true });

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          clearTimeout(failsafeTimer);
          window.removeEventListener('scroll', handleScrollFallback);
          observer.unobserve(el);
        }
      },
      {
        threshold: 0,
        rootMargin: '0px 0px -20px 0px',
      }
    );

    observer.observe(el);

    return () => {
      clearTimeout(failsafeTimer);
      window.removeEventListener('scroll', handleScrollFallback);
      motionQuery.removeEventListener?.('change', handleMotionChange);
      observer.disconnect();
    };
  }, []);

  return (
    <div
      ref={ref}
      style={{
        transitionProperty: 'opacity, transform',
        transitionDuration: '550ms',
        transitionDelay: `${delay}ms`,
        transitionTimingFunction: 'cubic-bezier(0.16, 1, 0.3, 1)',
        willChange: isVisible ? 'auto' : 'opacity, transform',
      }}
      className={`transform-gpu ${
        isVisible
          ? 'opacity-100 translate-y-0'
          : direction === 'up'
          ? 'opacity-0 translate-y-5'
          : 'opacity-0'
      } ${className}`}
    >
      {children}
    </div>
  );
};
