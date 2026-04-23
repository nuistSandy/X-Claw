import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { vitePatchable } from "./vite-plugin-patchable";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const apiBaseUrl = env.VITE_API_BASE_URL ?? "";

  return {
    define: {
      VITE_API_BASE_URL: JSON.stringify(apiBaseUrl),
      TOKEN: JSON.stringify(env.TOKEN || ""),
      MOBILE: false,
    },
    plugins: [
      react(),
      vitePatchable({
        include: ["src/pages"],
        registryOutput: "src/plugins/generated/registerHostModules.ts",
        registryImport: "../moduleRegistry",
        requireMarker: false,
        verbose: true,
      }),
    ],
    css: {
      modules: {
        localsConvention: "camelCase",
        generateScopedName: "[name]__[local]__[hash:base64:5]",
      },
      preprocessorOptions: {
        less: {
          javascriptEnabled: true,
        },
      },
    },
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    // ✅ 已配置好代理
    server: {
      host: "0.0.0.0",
      port: 5173,
      proxy: {
        "/api": {
          target: "http://127.0.0.1:8088",
          changeOrigin: true,
          ws: true,
          rewrite: (path) => path.replace(/^\/api/, "")
        },
        "/channels": {
          target: "http://127.0.0.1:8088",
          changeOrigin: true,
          ws: true
        }
      }
    },
    optimizeDeps: {
      include: ["diff"],
    },
    build: {
      cssCodeSplit: true,
      sourcemap: mode !== "production",
      chunkSizeWarningLimit: 1000,
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (
              id.includes("node_modules/react/") ||
              id.includes("node_modules/react-dom/") ||
              id.includes("node_modules/react-router-dom/") ||
              id.includes("node_modules/scheduler/")
            ) {
              return "react-vendor";
            }
            if (
              id.includes("node_modules/antd/") ||
              id.includes("node_modules/antd-style/") ||
              id.includes("node_modules/@ant-design/") ||
              id.includes("node_modules/@agentscope-ai/")
            ) {
              return "ui-vendor";
            }
            if (
              id.includes("node_modules/i18next/") ||
              id.includes("node_modules/react-i18next/")
            ) {
              return "i18n-vendor";
            }
            if (
              id.includes("node_modules/react-markdown/") ||
              id.includes("node_modules/remark-gfm/") ||
              id.includes("node_modules/rehype") ||
              id.includes("node_modules/remark") ||
              id.includes("node_modules/unified/") ||
              id.includes("node_modules/mdast") ||
              id.includes("node_modules/hast") ||
              id.includes("node_modules/micromark")
            ) {
              return "markdown-vendor";
            }
            if (id.includes("node_modules/@dnd-kit/")) {
              return "dnd-vendor";
            }
            if (
              id.includes("node_modules/dayjs/") ||
              id.includes("node_modules/zustand/") ||
              id.includes("node_modules/ahooks/") ||
              id.includes("node_modules/@vvo/tzdb/")
            ) {
              return "utils-vendor";
            }
          },
        },
      },
    },
  };
});