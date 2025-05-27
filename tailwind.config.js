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
        'ascension': {
          'blue': '#0A1F44',
          'white': '#F5F7FA',
        },
        'biotech': {
          'green': '#34C759',
        },
        'signal': {
          'violet': '#6B4EFF',
        },
        'slate': {
          'gray': '#3C3C4E',
        },
        'alert': {
          'red': '#FF3B30',
        },
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#6B4EFF',
          600: '#5B3EDF',
          700: '#4B2EBF',
        },
      }
    },
  },
  plugins: [],
}