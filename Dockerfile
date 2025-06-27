# Stage 1: Build the SvelteKit application
FROM oven/bun:1 AS builder # Gunakan tag versi spesifik (misal: 1.1.18) atau 'latest'

WORKDIR /app

# Copy package.json and bun.lockb first to leverage Docker's build cache
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile # Gunakan --frozen-lockfile untuk build produksi

# Copy the rest of your application code
COPY . .

# Build the SvelteKit application
# This command generates the production build in .svelte-kit/output
RUN bun run build

# Stage 2: Create the final production image
FROM oven/bun:1-alpine # Gunakan base image yang lebih kecil dan stabil untuk produksi (misal: 1.1.18-alpine)

# Set the working directory for your application in the final image
WORKDIR /home/bun/app

# Copy the entire SvelteKit build output from the builder stage
# This includes the 'server', 'client', and importantly, the 'static' folder
# So, /home/bun/app/static/jkt48_members.json will be available
COPY --from=builder /app/.svelte-kit/output /home/bun/app/

# Optional: Set correct permissions (good practice)
RUN chown -R bun:bun /home/bun/app
USER bun

# Expose the port your SvelteKit app listens on (default is 3000)
EXPOSE 3000

# Command to start your SvelteKit application
CMD ["bun", "run", "start"]