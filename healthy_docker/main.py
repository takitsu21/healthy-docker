import requests
import logging
import time
import traceback
import docker
import os

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

URL_HEALTHCHECK = os.getenv("URL")
HEALTHCHECK_INTERVAL = int(os.getenv("HEALTHCHECK_INTERVAL", 60))


def restart_docker(client: docker.DockerClient, container_name: str):
    container = client.containers.get(container_name)
    container.restart()
    logger.info("Docker container restarted")


def main():
    docker_client = docker.DockerClient(base_url="unix://var/run/docker.sock")
    container_name = os.getenv("CONTAINER_NAME", "qbittorrent")
    while True:
        try:
            response = requests.get(URL_HEALTHCHECK, timeout=10)
            if not response.ok:
                logger.info("Restarting docker...")
                restart_docker(client=docker_client, container_name=container_name)
            else:
                logger.info("Docker container is runnin")
            time.sleep(HEALTHCHECK_INTERVAL)
        except Exception:
            logger.error(f"Error => {traceback.format_exc()}")


if __name__ == "__main__":
    main()
