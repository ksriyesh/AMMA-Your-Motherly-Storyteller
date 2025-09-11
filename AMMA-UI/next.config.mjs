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
}

export default nextConfig
