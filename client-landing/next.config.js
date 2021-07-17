module.exports = {
  async rewrites() {
    return [
      {
        source: "/:path*",
        destination: "/:path*",
      },
      {
        source: "/portal",
        destination: "http://localhost:8000/portal",
      },
      {
        source: "/portal/:path*",
        destination: "http://localhost:8000/portal/:path*",
      },
    ];
  },
};
