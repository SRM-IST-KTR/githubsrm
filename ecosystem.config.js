module.exports = {
    apps: [
        {
            name: "GitHubSRM: Django Server",
            interpreter: "python3",
            cwd: "server/githubsrm",
            script: "manage.py",
            args: "runserver",
        },
    ],
};