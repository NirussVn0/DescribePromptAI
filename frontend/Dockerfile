FROM node:20-alpine

WORKDIR /app

COPY package.json pnpm-lock.yaml ./

# Install pnpm
RUN pnpm install --frozen-lockfile

COPY . .

RUN pnpm run build


EXPOSE 3000

CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0"]
