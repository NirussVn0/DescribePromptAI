"use client";

import { useState } from "react";
import toast from "react-hot-toast";

import { apiClient } from "../services/apiClient";
import { analysisStore } from "../store/analysisStore";
import { getErrorMessage } from "../utils/errors";

const fileToBase64 = (file: File) =>
  new Promise<string>((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result;
      if (typeof result === "string") {
        resolve(result.split(",").pop() ?? "");
      } else {
        reject(new Error("Failed to read file data."));
      }
    };
    reader.onerror = () => reject(new Error("Unable to read the selected file."));
    reader.readAsDataURL(file);
  });

export function useImageAnalysis() {
  const [isUploading, setIsUploading] = useState(false);
  const { setImageId, runAnalysis } = analysisStore();

  const uploadImage = async (file: File) => {
    setIsUploading(true);
    try {
      const base64 = await fileToBase64(file);
      const response = await apiClient.post<{ image_id: string; size_bytes: number }>("/images/upload", {
        filename: file.name,
        content_type: file.type || "image/*",
        data_base64: base64
      });

      setImageId(response.image_id);
      await runAnalysis(response.image_id);
      toast.success("Image analyzed successfully.");
    } catch (error) {
      toast.error(getErrorMessage(error, "Failed to analyze the provided image."));
    } finally {
      setIsUploading(false);
    }
  };

  return { uploadImage, isUploading };
}
