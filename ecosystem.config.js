module.exports = {
  apps: [
    {
      name: "GitHubSRM: Django Server",
      script: "chmod +x ./run.sh && ./run.sh 8000",
    },
    {
      name: "GitHubSRM: Landing Page",
      cwd: "client",
      script: "yarn start:landing -p 3000",
    },
    {
      name: "GitHubSRM: Portal Page",
      cwd: "client",
      script: "yarn start:portal -p 5000",
    },
  ],
};
