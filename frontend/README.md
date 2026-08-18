# UniHAP HITL Frontend

Next.js 15 (App Router) review UI for the UniHAP product-intelligence pipeline. Curators
browse the catalog, inspect evidence-backed attributes, and approve or reject records here.

## Prerequisites

- Node 20+
- The UniHAP backend running locally (`uv run unihap api`, from the repo root) — this
  frontend talks to it directly, there's no bundled mock

## Setup

```bash
cp .env.local.example .env.local
npm install
npm run dev
```

The backend must run on `http://localhost:8000` (its CORS config only allows requests
from `http://localhost:3000`/`http://127.0.0.1:3000`, so keep the frontend dev server on
the default port). Open [http://localhost:3000](http://localhost:3000).

## Scripts

```bash
npm run dev         # start the dev server
npm run build        # production build
npm run start        # serve the production build
npm run lint          # eslint
npm run typecheck  # tsc --noEmit
```

## Structure

- `src/app` — routes (`/`, `/catalog`, `/catalog/[id]`, `/settings`) and SEO routes
  (`sitemap.ts`, `robots.ts`, `opengraph-image.tsx`)
- `src/components/ui` — unstyled-ish primitives (button, card, tabs, disclosure, ...)
- `src/components/{catalog,product,landing,settings,layout,common}` — feature components
- `src/hooks` — TanStack Query hooks and local-storage-backed settings hooks
- `src/lib` — API client, design tokens' JS-side counterparts, formatting, animation
  variants
- `src/types` — mirrors the backend's Pydantic schemas field-for-field

## Environment variables

| Variable | Purpose | Default |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | Backend base URL | `http://localhost:8000` |
| `NEXT_PUBLIC_SITE_URL` | This app's own public URL, used in SEO metadata/sitemap/robots | `http://localhost:3000` |
