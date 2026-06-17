export interface FaceAttributes {
  embedding_id: string;
  embedding_vector?: number[];
  age_range?: string | null;
  gender?: string | null;
  emotions?: string[];
  accessories?: string[];
}

export interface ContextAttributes {
  scene?: string[];
  lighting?: string | null;
  style_tags?: string[];
  detected_objects?: string[];
}

export interface AnalysisResult {
  image_id: string;
  face?: FaceAttributes | null;
  context?: ContextAttributes | null;
}

export interface PromptPayload {
  platform: string;
  prompt: Record<string, unknown>;
  metadata: Record<string, unknown>;
}

export interface PromptGenerationResponse {
  image_id: string;
  prompts: PromptPayload[];
}

export interface VideoVisualCue {
  title: string;
  content: string;
  weight: number;
}

export interface VideoPromptPayload {
  reference_id: string;
  narrative: string;
  motion: string;
  persona?: string | null;
  visual_cues: VideoVisualCue[];
  technical: Record<string, string>;
}

export interface VideoExtensionResponse {
  image_id: string;
  video_prompt: VideoPromptPayload;
  duration_seconds: number;
}
