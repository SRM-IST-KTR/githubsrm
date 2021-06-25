cd server/githubsrm/
gunicorn core.wsgi:application --bind 0.0.0.0:5000