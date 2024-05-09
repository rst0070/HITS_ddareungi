/** @type {import('next').NextConfig} */
const prefix = process.env.NODE_ENV === 'production' ? 'https://rst0070.github.io/HITS_ddareungi/' : ''

const nextConfig = {
    output: 'export',
    assetPrefix: prefix
};
  
export default nextConfig;
