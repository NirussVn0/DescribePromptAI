"use client";

import { create } from "zustand";
import { apiClient } from "../services/apiClient";
import type { PromptGenerationResponse } from "../types";

interface PromptState {
  prompts: PromptGenerationResponse["prompts"];
  generatePrompts: (imageId: string) => Promise<PromptGenerationResponse>;
}

export const promptStore = create<PromptState>((set) => ({
  prompts: [],
  generatePrompts: async (imageId: string) => {
    const response = await apiClient.post<PromptGenerationResponse>("/prompts/generate", {
      image_id: imageId,
      target_platforms: ["sora", "runway", "pika", "luma"]
    });
    set({ prompts: response.prompts });
    return response;
  }
}));
