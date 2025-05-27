/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'syne': ['Syne', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
      },
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        sage: {
          50: '#f6f7f6',
          100: '#e4e7e4',
          500: '#6b7b6b',
          600: '#5a6b5a',
          700: '#4a5a4a',
        }
      }
    },
  },
  plugins: [],
}