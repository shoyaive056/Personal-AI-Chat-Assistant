/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        ink: "rgb(var(--color-ink) / <alpha-value>)",
        paper: "rgb(var(--color-paper) / <alpha-value>)",
        surface: "rgb(var(--color-surface) / <alpha-value>)",
        border: "rgb(var(--color-border) / <alpha-value>)",
        slate: "rgb(var(--color-slate) / <alpha-value>)",
        moss: {
          DEFAULT: "rgb(var(--color-moss) / <alpha-value>)",
          dark: "rgb(var(--color-moss-dark) / <alpha-value>)",
          light: "rgb(var(--color-moss-light) / <alpha-value>)",
        },
        rust: {
          DEFAULT: "rgb(var(--color-rust) / <alpha-value>)",
          bg: "rgb(var(--color-rust-bg) / <alpha-value>)",
          border: "rgb(var(--color-rust-border) / <alpha-value>)",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        serif: ["Fraunces", "Georgia", "serif"],
      },
    },
  },
  plugins: [],
};