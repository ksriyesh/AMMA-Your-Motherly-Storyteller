import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  // Enable static export for GitHub Pages
  output: 'export',
  trailingSlash: true,
  // Configure base path if deploying to a subdirectory
  // basePath: process.env.NODE_ENV === 'production' ? '/repository-name' : '',
  // assetPrefix: process.env.NODE_ENV === 'production' ? '/repository-name/' : '',
  
  // Webpack configuration for proper path resolution
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': __dirname,
    }
    return config
  },
}

export default nextConfig
