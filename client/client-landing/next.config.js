const { API_HOSTNAME } = process.env;
module.exports = {
  async rewrites() {
    return [
      {
        source: "/:path*",
        destination: "/:path*",
      },
      {
        source: "/api",
        destination: `${API_HOSTNAME}/api`,
      },
      {
        source: "/api/:path*",
        destination: `${API_HOSTNAME}/api/:path*`,
      },
    ];
  },
};
