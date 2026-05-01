import logging
import os
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("run")

if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    reload_enabled = os.getenv("APP_RELOAD", "true").lower() == "true"

    # Helpful local URLs for quick testing in browser/Postman.
    local_base_url = f"http://127.0.0.1:{port}"
    logger.info("Starting backend server")
    logger.info("Swagger UI: %s/docs", local_base_url)
    logger.info("OpenAPI JSON: %s/openapi.json", local_base_url)
    logger.info("Server bind: http://%s:%s", host, port)

    uvicorn.run("app.main:app", host=host, port=port, reload=reload_enabled)
