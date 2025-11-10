/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        nuam: {
          50:  "#FFF3ED",
          100: "#FFE3D6",
          200: "#FFC2AD",
          300: "#FFA184",
          400: "#FF835F",
          500: "#FF6F3D", // principal
          600: "#F05B2A",
          700: "#CC4821",
          800: "#9E391B",
          900: "#7F2F17"
        }
      }
    }
  },
  plugins: [],
};