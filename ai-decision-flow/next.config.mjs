/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Transpile heavy canvas/graph libraries if needed for Next.js SSR compatibility
  transpilePackages: ["@xyflow/react"],

  // Server actions configuration
  experimental: {
    serverActions: {
      bodySizeLimit: "2mb",
    },
  },
};

export default nextConfig;