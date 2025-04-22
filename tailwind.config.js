/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './vue-ysj/src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#fa964b',
      },
    },
  },
  plugins: [],
}; 