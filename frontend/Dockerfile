# Dockerfile para SIGOT Frontend (Vue + Nginx)
# Multi-stage build

# Stage 1: Build Vue app
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build for production
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config template
COPY nginx.conf /etc/nginx/nginx.conf.template

# Copy built Vue app
COPY --from=builder /app/dist /usr/share/nginx/html

# Default environment variables
ENV PORT=80
ENV BACKEND_URL=http://backend:8000

# Expose port
EXPOSE 80

# Use envsubst to replace env vars and start nginx
CMD ["/bin/sh", "-c", "envsubst '${PORT} ${BACKEND_URL}' < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]

