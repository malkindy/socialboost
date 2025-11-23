/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}", // all files inside app/
    "./pages/**/*.{js,ts,jsx,tsx}", // optional if you have pages folder
    "./components/**/*.{js,ts,jsx,tsx}" // optional if you have components folder
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
