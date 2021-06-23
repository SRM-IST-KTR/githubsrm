module.exports = {
  purge: ["./pages/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        "base-black": "#353535",
        "base-green": "#79BA6E",
        "base-smoke": "#D9D9D9",
        "base-blue": "#284B63",
        "base-teal": "#6CAEB2",
      },
      fontFamily: {
        montserrat: ["Montserrat", "sans-serif"],
      },
      zIndex: {
        1: 1,
        "-10": "-10",
      },
      "border-b": ["hover"],
    },
    keyframes: {
      fill: {
        "0%": { width: "0%", height: "1px" },
        "50%": { width: "100%", height: "1px" },
        "100%": { width: "100%", height: "100%", background: "#FFFFFF" },
      },
    },
    animation: {
      fill: "fill 1s forwards",
    },
  },
  variants: {
    extend: {
      zIndex: ["hover"],
    },
  },
  plugins: [],
};
