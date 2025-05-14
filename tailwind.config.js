module.exports = {
  content: ["./app/templates/**/*.html", "./app/static/js/**/*.js", "./app/static/css/**/*.css"], // Update paths as needed
  safelist: [
    'animate-infinite-scroll',
    'bg-primaryorange',
    'bg-accentpurple',
  ],
  theme: {
    extend: {
      colors: {
        'primaryorange': "#EFB071",
        'accentpurple': "#7F60F9",
        'dark-bg': '#0F172A',
      },
      fontFamily: {
        eurostile: ['EurostileExtendedBlack', 'sans-serif'],
        montserrat: ["'Montserrat'", 'sans-serif'],
        inter: ["'Inter'", 'sans-serif'],
        lexend: ["'Lexend'", 'sans-serif'],
        roboto: ["'Roboto'", 'sans-serif'],
      },
      keyframes: {
        'infinite-scroll': {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
      },
      animation: {
        'infinite-scroll': 'infinite-scroll 25s linear infinite',
      },
    },
  },
  plugins: [],
};
