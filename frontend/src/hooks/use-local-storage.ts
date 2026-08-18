"use client";

import { useCallback, useEffect, useRef, useState } from "react";

export function useLocalStorageValue<T>(key: string, fallback: T, parse: (raw: string) => T, serialize: (value: T) => string) {
  const [value, setValue] = useState<T>(fallback);
  const parseRef = useRef(parse);
  parseRef.current = parse;
  const fallbackRef = useRef(fallback);
  fallbackRef.current = fallback;

  useEffect(() => {
    const raw = window.localStorage.getItem(key);
    if (raw === null) return;
    try {
      setValue(parseRef.current(raw));
    } catch {
      setValue(fallbackRef.current);
    }
  }, [key]);

  const set = useCallback(
    (next: T) => {
      setValue(next);
      window.localStorage.setItem(key, serialize(next));
    },
    [key, serialize],
  );

  return [value, set] as const;
}

export function useLocalStorageString(key: string, fallback: string) {
  return useLocalStorageValue(key, fallback, (raw) => raw, (v) => v);
}

export function useLocalStorageNumber(key: string, fallback: number) {
  return useLocalStorageValue(
    key,
    fallback,
    (raw) => {
      const parsed = Number(raw);
      return Number.isFinite(parsed) ? parsed : fallback;
    },
    (v) => String(v),
  );
}
