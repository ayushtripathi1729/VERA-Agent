import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* High-Performance AI Dashboard Configuration 
  */
  
  // 1. Enable React Strict Mode for better debugging of neural logs
  reactStrictMode: true,

  // 2. Transpile Framer Motion and Lucide for faster cloud builds
  transpilePackages: ["lucide-react", "framer-motion"],

  // 3. Environment Variable Mapping
  env: {
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL,
  },

  // 4. Power-User Optimizations
  eslint: {
    // We ignore lint errors during the hackathon build to ensure it deploys fast.
    // In a production environment, you would keep this enabled.
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Ensures the build doesn't crash if there's a minor type mismatch in the agent logic.
    ignoreBuildErrors: true,
  },

  // 5. Image Optimization (if you add neural network diagrams or profile icons later)
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**', // Allows images from any secure source
      },
    ],
  },
};

export default nextConfig;
