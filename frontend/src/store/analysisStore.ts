"use client";

import { create } from "zustand";
import { apiClient } from "../services/apiClient";
import type { AnalysisResult } from "../types";

interface AnalysisState {
  imageId?: string;
  analysis?: AnalysisResult;
  modes: ("face" | "context")[];
  setImageId: (imageId: string) => void;
  toggleMode: (mode: "face" | "context") => void;
  runAnalysis: (imageId: string) => Promise<AnalysisResult>;
}

export const analysisStore = create<AnalysisState>((set, get) => ({
  modes: ["face", "context"],
  setImageId: (imageId: string) => set({ imageId }),
  toggleMode: (mode: "face" | "context") => {
    const { modes } = get();
    const next = modes.includes(mode)
      ? modes.filter((value) => value !== mode)
      : [...modes, mode];
    set({ modes: next.length ? next : ["face"] });
  },
  runAnalysis: async (imageId: string) => {
    const { modes } = get();
    const result = await apiClient.post<AnalysisResult>("/analysis/full", {
      image_id: imageId,
      modes
    });
    set({ analysis: result });
    return result;
  }
}));
