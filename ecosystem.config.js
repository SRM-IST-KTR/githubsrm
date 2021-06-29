module.exports = {
  apps: [
    {
      name: "GitHubSRM: Django Server",
      cwd: ".",
      interpreter: "bash",
      script: "./run.sh 8000",
    },
  ],
};
