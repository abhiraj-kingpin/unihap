"use client";

import { useLocalStorageNumber, useLocalStorageString } from "@/hooks/use-local-storage";
import { SETTINGS_DEFAULTS, SETTINGS_KEYS } from "@/lib/settings";

export function useCuratorSettings() {
  const [curatorName, setCuratorName] = useLocalStorageString(SETTINGS_KEYS.curatorName, SETTINGS_DEFAULTS.curatorName);
  const [defaultPageSize, setDefaultPageSize] = useLocalStorageNumber(
    SETTINGS_KEYS.defaultPageSize,
    SETTINGS_DEFAULTS.defaultPageSize,
  );

  return { curatorName, setCuratorName, defaultPageSize, setDefaultPageSize };
}
