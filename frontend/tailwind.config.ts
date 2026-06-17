import type { Config } from "tailwindcss";

export default {
  darkMode: "class",
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#6366f1",
          light: "#a5b4fc",
          dark: "#4338ca"
        }
      }
    }
  },
  plugins: []
} satisfies Config;
