import os

host = os.getenv("GRAPS_API_HOST", "0.0.0.0")
port = os.getenv("GRAPS_API_PORT", "8080")

# Gunicorn config variables
loglevel = os.getenv("LOG_LEVEL", "info")
workers = 1
bind = f"{host}:{port}"
errorlog = "-"
if os.path.isdir("/dev/shm"):
    worker_tmp_dir = "/dev/shm"
accesslog = "-"
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", "120"))
timeout = int(os.getenv("TIMEOUT", "120"))
keepalive = int(os.getenv("KEEP_ALIVE", "5"))


# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "keepalive": keepalive,
    "errorlog": errorlog,
    "accesslog": accesslog,
}
