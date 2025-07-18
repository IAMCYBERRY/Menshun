# =============================================================================
# Menshun Frontend - Multi-stage Docker Build
# =============================================================================

# Build stage
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache git

# Copy package files
COPY package*.json ./

# Install dependencies (including dev dependencies for build)
RUN npm install && npm cache clean --force

# Copy source code
COPY . .

# Build arguments for environment variables
ARG VITE_AZURE_CLIENT_ID
ARG VITE_AZURE_TENANT_ID
ARG VITE_AZURE_REDIRECT_URI
ARG VITE_API_BASE_URL
ARG VITE_APP_VERSION
ARG VITE_APP_ENVIRONMENT

# Set environment variables
ENV VITE_AZURE_CLIENT_ID=$VITE_AZURE_CLIENT_ID
ENV VITE_AZURE_TENANT_ID=$VITE_AZURE_TENANT_ID
ENV VITE_AZURE_REDIRECT_URI=$VITE_AZURE_REDIRECT_URI
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_APP_VERSION=$VITE_APP_VERSION
ENV VITE_APP_ENVIRONMENT=$VITE_APP_ENVIRONMENT

# Build application
RUN npm run build

# Production stage
FROM nginx:1.25-alpine as production

# Install security updates
RUN apk upgrade --no-cache

# Copy custom nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/default.conf /etc/nginx/conf.d/default.conf

# Copy built application
COPY --from=build /app/dist /usr/share/nginx/html

# Copy environment configuration script
COPY docker/configure-env.sh /docker-entrypoint.d/

# Make the script executable
RUN chmod +x /docker-entrypoint.d/configure-env.sh

# Create non-root user
RUN addgroup -g 1001 -S menshun && \
    adduser -S menshun -u 1001 -G menshun

# Set ownership
RUN chown -R menshun:menshun /usr/share/nginx/html
RUN chown -R menshun:menshun /var/cache/nginx
RUN chown -R menshun:menshun /var/log/nginx

# Create nginx directories with proper permissions
RUN mkdir -p /var/run/nginx && \
    chown -R menshun:menshun /var/run/nginx

# Switch to non-root user
USER menshun

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose port
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

# =============================================================================
# Development stage (for development use)
# =============================================================================
FROM node:18-alpine as development

WORKDIR /app

# Install development dependencies
RUN apk add --no-cache git curl

# Copy package files
COPY package*.json ./

# Install all dependencies (including dev)
RUN npm install

# Copy source code
COPY . .

# Expose development port
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# =============================================================================
# Test stage (for running tests)
# =============================================================================
FROM node:18-alpine as test

WORKDIR /app

# Install dependencies and testing tools
RUN apk add --no-cache git

# Copy package files
COPY package*.json ./

# Install all dependencies
RUN npm ci

# Copy source code
COPY . .

# Run tests
CMD ["npm", "run", "test:ci"]