# 🚀 DescribePromptAI &nbsp;

![Build](https://img.shields.io/badge/build-passing-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.11-blue?logo=python) ![NextJS](https://img.shields.io/badge/next.js-14-black?logo=next.js) ![Docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker)

> **DescribePromptAI**  
> Full-stack image-to-video prompt engineering  
> **Backend:** FastAPI (Claude Vision, InsightFace, PostgreSQL, Redis, S3)  
> **Frontend:** Next.js 14, Zustand, theme toggle, export tools  
> **Infra:** Docker Compose, Vercel/Render/Railway ready  
> **Demo:** [depromptai.sabicoder.xyz](https://depromptai.sabicoder.xyz/)

---

## 🧩 Architecture

```
.
├── backend
│   ├── app
│   │   ├── core
│   │   ├── models
│   │   ├── routers
│   │   ├── services
│   │   └── utils
│   └── tests
├── frontend
│   ├── public
│   └── src
│       ├── app
│       ├── components
│       ├── hooks
│       ├── services
│       ├── store
│       ├── types
│       └── utils
└── docker-compose.yml
```

| Backend                             |Frontend                              |
|----------------------------------------|------------------------------------------|
| FastAPI (Python 3.11)                  | Next.js 14 (TypeScript, Tailwind)        |
| Claude Vision, InsightFace Embeddings   | Zustand, ThemeToggle, Prompt Export      |
| PostgreSQL, Redis, S3                  | Responsive dark/light UI                 |

---

## ✨ Features

- 🖼️ Image upload and smart multimodal analysis
- 🔍 AI prompt (Claude Vision + InsightFace) generation
- 🎥 Export platform-optimized prompts for Sora, Runway, Pika, Luma
- 🌗 Theme toggle (dark/light)
- 🍃 Dockerized stack for instant dev/prod deployment

---

## Getting Started

```
# 1. Install dependencies
cd backend     &&    pip install -r requirements.txt
cd ../frontend &&    pnpm install

# 2. Start services
docker-compose up --build

# 3. Open:
#    - Frontend:   http://localhost:3000
#    - API Docs:   http://localhost:8000/docs
#    - Production: https://depromptai.sabicoder.xyz
```

---

## 📚 Documentation

- [API Reference](docs/api.md)
- [User Guide](docs/user-guide.md)
- [Architecture Overview](docs/architecture.md)

> Sample configs: [`backend/.env.example`](backend/.env.example), [`frontend/.env.example`](frontend/.env.example)


## 👨‍💻 Contributer

- **NirusVn0**  
  - [work@sabicoder.xyz](mailto:work@sabicoder.xyz)
  - [sabicoder.xyz](https://sabicoder.xyz/)
  - [GitHub](https://github.com/NirusVn0)
  - [X](https://twitter.com/NirusVn0)

<p align="center">
  <a href="https://sabicoder.xyz">
    <img src="https://skillicons.dev/icons?i=python,fastapi,nextjs,docker,redis,postgresjs" height="32px" />
  </a>
</p>

---