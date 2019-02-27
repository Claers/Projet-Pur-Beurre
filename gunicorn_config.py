bind = "127.0.0.1:8887"
log_file = "logs/gunicorn_logs.txt"

# Environment variables
raw_env = [
    "PRODUCTION=true",
]
