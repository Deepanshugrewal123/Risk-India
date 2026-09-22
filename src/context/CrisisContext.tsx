import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface CrisisContextType {
  isCrisisMode: boolean;
  toggleCrisisMode: () => void;
  setCrisisMode: (active: boolean) => void;
}

const CrisisContext = createContext<CrisisContextType | undefined>(undefined);

const CRISIS_STORAGE_KEY = 'risk_india_crisis_mode';

export const CrisisProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isCrisisMode, setIsCrisisModeState] = useState<boolean>(() => {
    if (typeof window === 'undefined') return false;
    try {
      // Check URL query parameter: ?crisis=true or ?crisis=1
      const params = new URLSearchParams(window.location.search);
      if (params.get('crisis') === 'true' || params.get('crisis') === '1') {
        return true;
      }
      // Check stored preference
      const stored = localStorage.getItem(CRISIS_STORAGE_KEY);
      return stored === 'true';
    } catch {
      return false;
    }
  });

  const setCrisisMode = (active: boolean) => {
    setIsCrisisModeState(active);
    try {
      localStorage.setItem(CRISIS_STORAGE_KEY, String(active));
      // Update URL query parameter without full reload
      const url = new URL(window.location.href);
      if (active) {
        url.searchParams.set('crisis', 'true');
      } else {
        url.searchParams.delete('crisis');
      }
      window.history.replaceState(null, '', url.toString());
    } catch {
      // Ignore storage errors in restricted contexts
    }
  };

  const toggleCrisisMode = () => {
    setCrisisMode(!isCrisisMode);
  };

  // Keep body class and reduced-motion styling synced
  useEffect(() => {
    if (typeof document !== 'undefined') {
      if (isCrisisMode) {
        document.documentElement.classList.add('crisis-mode');
      } else {
        document.documentElement.classList.remove('crisis-mode');
      }
    }
  }, [isCrisisMode]);

  return (
    <CrisisContext.Provider value={{ isCrisisMode, toggleCrisisMode, setCrisisMode }}>
      {children}
    </CrisisContext.Provider>
  );
};

export const useCrisis = (): CrisisContextType => {
  const context = useContext(CrisisContext);
  if (!context) {
    const isDocCrisis = typeof document !== 'undefined' && document.documentElement.classList.contains('crisis-mode');
    return {
      isCrisisMode: isDocCrisis,
      toggleCrisisMode: () => {},
      setCrisisMode: () => {},
    };
  }
  return context;
};
