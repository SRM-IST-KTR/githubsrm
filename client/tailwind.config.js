module.exports = {
  purge: ["./pages/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        baseBlack: "#353535",
        baseGreen: "#79BA6E",
        baseSmoke: "#D9D9D9",
        baseBlue: "#284B63",
        baseTeal: "#6CAEB2",
      },
      fontFamily: {
        montserrat: ["Montserrat", "sans-serif"],
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
