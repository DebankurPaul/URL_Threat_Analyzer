# ── Stage 1: Build ──────────────────────────────────────────────────────────
# We use Node to compile React → static HTML/JS/CSS files
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first (layer caching — same reason as backend)
COPY package.json package-lock.json ./
RUN npm ci                          # ci = clean install, faster than npm install

# Copy source and build
COPY . .
RUN npm run build
# This creates /app/dist/ with index.html + assets/

# ── Stage 2: Serve ──────────────────────────────────────────────────────────
# We don't need Node in production — just serve the static files with nginx
# nginx image is tiny (~25MB vs ~300MB for Node)
FROM nginx:alpine

# Copy the built files into nginx's serving directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy our custom nginx config (routes /api calls to the backend)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80