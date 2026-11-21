import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// En desarrollo, las llamadas a /api se reenvían al Backend (uvicorn en el puerto 8000).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: { '/api': 'http://localhost:8000' },
    // Vitest necesita leer las pruebas de tests/web, que están fuera de esta carpeta.
    fs: { allow: ['.', '../../tests/web'] },
  },
  // Pruebas unitarias (Vitest). Están en tests/web, en la raíz del repositorio.
  test: {
    dir: '../../tests/web',
    environment: 'node',
    coverage: {
      provider: 'v8',
      // Se mide lo que implementa la HU sin interfaz gráfica: Modelos, Controlador y Cliente.
      include: ['src/modelos/**', 'src/controladores/**', 'src/cliente/**'],
      reporter: ['text'],
    },
  },
})
