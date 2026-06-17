"use client";

import { useCallback, useState } from "react";

import { apiClient } from "../services/apiClient";
import { analysisStore } from "../store/analysisStore";
import type { VideoExtensionResponse } from "../types";

interface ExtendInput {
  motion: string;
  durationSeconds?: number;
}

export function useVideoExtension() {
  const [videoPrompt, setVideoPrompt] = useState<VideoExtensionResponse["video_prompt"] | null>(null);
  const [isExtending, setIsExtending] = useState(false);
  const imageId = analysisStore((state) => state.imageId);

  const extendPrompt = async ({ motion, durationSeconds }: ExtendInput) => {
    if (!imageId) {
      throw new Error("Upload and analyze an image before extending to video.");
    }
    setIsExtending(true);
    try {
      const result = await apiClient.post<VideoExtensionResponse>("/video/extend", {
        image_id: imageId,
        motion_description: motion,
        duration_seconds: durationSeconds
      });
      setVideoPrompt(result.video_prompt);
      return result;
    } finally {
      setIsExtending(false);
    }
  };

  const resetPrompt = useCallback(() => setVideoPrompt(null), []);

  return {
    imageId,
    extendPrompt,
    isExtending,
    videoPrompt,
    resetPrompt
  };
}
