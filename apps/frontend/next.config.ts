import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Required for the Docker multi-stage build (copies only what's needed).
  output: "standalone",

  // API proxy: forward /api/* calls to the FastAPI backend during development.
  // In production, configure your reverse proxy (nginx / ALB) instead.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/:path*`,
      },
    ];
  },
};

export default nextConfig;
