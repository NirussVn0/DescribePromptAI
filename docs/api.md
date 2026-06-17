# DescribePromptAI API Reference

The DescribePromptAI backend exposes a FastAPI service with the following primary endpoints. All responses are JSON. Authentication is not yet required for the local development stack.

Base URL (local): `http://localhost:8000`

## Health & Documentation

- `GET /docs` – Interactive Swagger UI.
- `GET /openapi.json` – Machine-readable OpenAPI schema.

## Images

### `POST /images/upload`
Upload a base64-encoded image. The service validates the file extension and size, then stores the payload in the configured storage backend (S3 when `STORAGE_BACKEND=hybrid`).

**Request Body**
```json
{
  "filename": "portrait.png",
  "content_type": "image/png",
  "data_base64": "<base64 data>"
}
```

**Response**
```json
{
  "image_id": "9272af64-...",
  "size_bytes": 48321
}
```

## Analysis

### `POST /analysis/full`
Triggers multimodal analysis for the provided `image_id`. Claude Vision handles vision-language extraction and InsightFace produces a 512-dim face embedding (or a deterministic fallback when the model is unavailable). Analysis results are cached in Redis and persisted to Postgres when `STORAGE_BACKEND=hybrid`.

**Request Body**
```json
{
  "image_id": "9272af64-...",
  "modes": ["face", "context"],
  "refresh_cache": false
}
```

**Response**
```json
{
  "image_id": "9272af64-...",
  "face": {
    "embedding_id": "9272af64-...-embedding",
    "embedding_vector": [...512 floats...],
    "emotions": ["confident"],
    "accessories": [],
    "age_range": "25-35",
    "gender": "unspecified"
  },
  "context": {
    "scene": ["indoor studio"],
    "lighting": "soft key lighting",
    "style_tags": ["cinematic"],
    "detected_objects": ["subject"]
  },
  "confidence": {
    "claude": 0.82
  }
}
```

## Prompt Generation

### `POST /prompts/generate`
Composes platform-optimised prompts using the normalized analysis result. Results are written to Redis for quick retrieval and Postgres for history.

**Request Body**
```json
{
  "image_id": "9272af64-...",
  "target_platforms": ["sora", "runway", "pika", "luma"]
}
```

**Response (excerpt)**
```json
{
  "image_id": "9272af64-...",
  "prompts": [
    {
      "platform": "runway",
      "prompt": {
        "prompt": "Scene: indoor studio ...",
        "camera": {
          "type": "medium close-up",
          "angle": "eye-level",
          "movement": "static hold"
        },
        "identity_control": {
          "mode": "embedding_conditioning",
          "face_embedding": [...512 floats...],
          "preserve_likeness": true
        },
        "duration": 10
      },
      "metadata": {
        "reference_id": "9272af64-...",
        "face_embedding_id": "9272af64-...-embedding",
        "aspect_ratio": "16:9"
      }
    }
  ]
}
```

## Video Extension

### `POST /video/extend`
Combines the normalized prompt with user-provided motion notes to create a platform-agnostic video brief.

**Request Body**
```json
{
  "image_id": "9272af64-...",
  "motion_description": "Camera pans slowly around the subject.",
  "duration_seconds": 8
}
```

**Response**
```json
{
  "image_id": "9272af64-...",
  "video_prompt": {
    "reference_id": "9272af64-...",
    "narrative": "Scene: indoor studio ...",
    "motion": "Camera pans slowly around the subject.",
    "visual_cues": [...],
    "technical": {
      "camera": "35mm prime lens",
      "lighting": "soft key lighting",
      "duration_seconds": "8"
    }
  },
  "duration_seconds": 8
}
```

## Error Handling

Errors are normalized to the format:
```json
{
  "error": "validation_error",
  "detail": "Invalid base64 payload."
}
```

The `error` field is one of `validation_error`, `not_found`, `analysis_error`, `prompt_error`, or `configuration_error`.

---

For schema-level detail, consult `/openapi.json` or introspect the `app/models` package.
