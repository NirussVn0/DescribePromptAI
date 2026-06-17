"use client";

import { useState } from "react";
import { FiUploadCloud } from "react-icons/fi";

import { useImageAnalysis } from "../../hooks/useImageAnalysis";

export default function ImageUpload() {
  const [fileName, setFileName] = useState<string>("");
  const { uploadImage, isUploading } = useImageAnalysis();

  const helperText = isUploading
    ? "Uploading & analyzing..."
    : fileName
      ? `Ready to analyze: ${fileName}`
      : "Drag & drop or browse an image";

  return (
    <div className="rounded-3xl border border-slate-200/70 bg-gradient-to-br from-white via-white to-slate-100/60 p-6 shadow-lg dark:border-slate-800/70 dark:from-slate-900 dark:via-slate-900 dark:to-slate-950/80">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-900 dark:text-white">Upload reference image</h2>
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            Supports JPG, PNG, WEBP up to 50&nbsp;MB. Your assets stay private during local analysis.
          </p>
        </div>
      </div>

      <label
        className="mt-5 flex cursor-pointer flex-col items-center gap-4 rounded-2xl border border-dashed border-slate-300 bg-slate-100/70 p-6 text-center transition hover:border-brand hover:bg-white dark:border-slate-700 dark:bg-slate-900/60 dark:hover:border-brand-light"
        aria-disabled={isUploading}
      >
        <span className="flex h-14 w-14 items-center justify-center rounded-full bg-brand/15 text-brand dark:bg-brand/25 dark:text-brand-light">
          <FiUploadCloud className="text-2xl" />
        </span>
        <div>
          <p className="text-sm font-medium text-slate-900 dark:text-white">Choose file or drop it here</p>
          <p className="text-xs text-slate-500 dark:text-slate-400">{helperText}</p>
        </div>
        <input
          className="hidden"
          type="file"
          accept="image/*"
          disabled={isUploading}
          onChange={async (event) => {
            const file = event.target.files?.[0];
            if (!file) return;
            setFileName(file.name);
            await uploadImage(file);
          }}
        />
      </label>
    </div>
  );
}
