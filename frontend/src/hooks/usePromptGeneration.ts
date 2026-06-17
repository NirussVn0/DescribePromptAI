"use client";

import { useState } from "react";
import toast from "react-hot-toast";

import { analysisStore } from "../store/analysisStore";
import { promptStore } from "../store/promptStore";
import { getErrorMessage } from "../utils/errors";

export function usePromptGeneration() {
  const [isGenerating, setIsGenerating] = useState(false);
  const generatePrompts = promptStore((state) => state.generatePrompts);
  const imageId = analysisStore((state) => state.imageId);

  const handleGenerate = async () => {
    if (!imageId) {
      toast.error("Upload and analyze an image before generating prompts.");
      return;
    }
    setIsGenerating(true);
    try {
      await generatePrompts(imageId);
      toast.success("Platform prompts generated.");
    } catch (error) {
      toast.error(getErrorMessage(error, "Failed to generate prompts."));
    } finally {
      setIsGenerating(false);
    }
  };

  return {
    handleGenerate,
    isGenerating
  };
}
