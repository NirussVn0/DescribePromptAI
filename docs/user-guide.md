# DescribePromptAI User Guide

This guide walks through the end-to-end workflow for transforming an image into platform-specific video prompts.

## 1. Launch the stack

```bash
# Terminal 1
cd backend
uvicorn app.main:app --reload

# Terminal 2
cd frontend
npm install
npm run dev
```

Or run everything via Docker:

```bash
docker compose up --build
```

The frontend is available at `http://localhost:3000` and the backend at `http://localhost:8000`.

## 2. Upload an Image

1. Click **Upload Image** and select a JPG/PNG/WEBP file (≤ 50 MB).
2. The app streams the file to the backend, which stores it in S3 (or in-memory when running locally).
3. The image ID appears in the toast confirmation and enables analysis.

## 3. Configure Analysis Modes

- Use the **Toggle analysis modes** control to enable *Face* and *Context* extraction.
- Toggling a mode automatically re-runs analysis (if an image is already selected).
- Face mode computes a 512-dim InsightFace embedding that is cached in Redis and persisted in Postgres for reuse.

## 4. Review Analysis

The **Analysis Results** panel surfaces:
- Face embedding metadata (ID + vector length), detected emotions, accessories.
- Contextual scene descriptors including lighting, objects, and style tags.

## 5. Generate Prompts

Click **Generate Platform Prompts** to build optimised payloads for Sora, Runway, Pika, and Luma. Results appear in the **Prompt Preview** panel with syntax highlighting.

Each platform output includes:
- Tailored structure (e.g., Sora's five-pillar layout, Runway identity control block).
- Embedded face vectors for likeness preservation.
- Shared metadata (reference ID, aspect ratio, lighting, style tags).

## 6. Extend to Video

Fill in motion guidance and duration within **Video Extension**:
- Describe camera moves, subject actions, or timing cues.
- Submit to enrich the base prompt with video-specific instructions.
- The resulting payload is shown beneath the form for easy copy/paste.

## 7. Export

Use the **Export** panel to retrieve prompts:
- Download JSON or CSV snapshots.
- Copy the payload directly to the clipboard.

## Tips

- If Claude Vision or InsightFace credentials are not configured, the system falls back to deterministic mock outputs so the workflow remains testable.
- Redis caches can be cleared (e.g., with `redis-cli FLUSHALL`) to force a full re-analysis.
- Swagger docs live at `http://localhost:8000/docs` for quick request inspection.

Happy prompt crafting!
