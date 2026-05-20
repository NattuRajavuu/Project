/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        ink: '#0b0b0f',
        pearl: '#f7f7f5',
        mist: '#e8e8e3',
      },
      boxShadow: {
        glow: '0 24px 80px rgba(0, 0, 0, 0.12)',
        soft: '0 14px 40px rgba(15, 15, 15, 0.08)',
      },
    },
  },
  plugins: [],
};
