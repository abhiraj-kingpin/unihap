"use client";

import { createContext, useCallback, useContext, useRef, useState } from "react";

interface LiveAnnouncerContextValue {
  announce: (message: string) => void;
}

const LiveAnnouncerContext = createContext<LiveAnnouncerContextValue | null>(null);

export function LiveRegionProvider({ children }: { children: React.ReactNode }) {
  const [message, setMessage] = useState("");
  const resetTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const announce = useCallback((next: string) => {
    setMessage(next);
    if (resetTimer.current) clearTimeout(resetTimer.current);
    resetTimer.current = setTimeout(() => setMessage(""), 5000);
  }, []);

  return (
    <LiveAnnouncerContext.Provider value={{ announce }}>
      {children}
      <div role="status" aria-live="polite" className="sr-only">
        {message}
      </div>
    </LiveAnnouncerContext.Provider>
  );
}

export function useLiveAnnouncer() {
  const context = useContext(LiveAnnouncerContext);
  if (!context) throw new Error("useLiveAnnouncer must be used within LiveRegionProvider");
  return context.announce;
}
