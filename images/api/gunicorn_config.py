"""gunicorn server configuration."""

threads = 8
workers = 1
timeout = 0
bind = "0.0.0.0:5000"
worker_class = "uvicorn.workers.UvicornWorker"
