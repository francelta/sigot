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
COPY nginx.conf /tmp/default.conf.template

# Copy built Vue app
COPY --from=builder /app/dist /usr/share/nginx/html

# Create startup script
RUN echo '#!/bin/sh' > /start.sh && \
    echo 'export PORT=${PORT:-80}' >> /start.sh && \
    echo 'envsubst "\$PORT" < /tmp/default.conf.template > /etc/nginx/conf.d/default.conf' >> /start.sh && \
    echo 'echo "Starting nginx on port $PORT"' >> /start.sh && \
    echo 'nginx -g "daemon off;"' >> /start.sh && \
    chmod +x /start.sh

ENTRYPOINT ["/bin/sh", "/start.sh"]
