FROM oven/bun:1 AS builder

WORKDIR /app

COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

COPY . .

RUN bun run build

FROM oven/bun:1-alpine

WORKDIR /home/bun/app

COPY --from=builder /app/.svelte-kit/output /home/bun/app/

RUN chown -R bun:bun /home/bun/app
USER bun

EXPOSE 3000

CMD ["bun", "run", "start"]