import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import swc from '@vitejs/plugin-react-swc';

export default defineConfig({
  plugins: [
    react(),
    swc(),
  ],
});