const { HOST_NAME } = process.env;
module.exports = {
  async rewrites() {
    return [
      {
        source: "/:path*",
        destination: "/:path*",
      },
      {
        source: "/portal",
        destination: `${HOST_NAME}/portal`,
      },
      {
        source: "/portal/:path*",
        destination: `${HOST_NAME}/portal/:path*`,
      },
    ];
  },
};
