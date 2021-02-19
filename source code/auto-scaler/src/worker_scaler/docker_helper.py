import docker
import logging
import uuid
import random


class DockerHelper:
    def __init__(self):
        self._client = docker.from_env()
        self._logger = logging.getLogger(__name__)

    def get_list_of_containers(self, image: str):
        running_worker = self._client.containers.list(filters={
            'ancestor': image,
            'status': 'running'
        })

        return running_worker

    def get_service_with_name(self, service_name: str):
        try:
            running_services = self._client.services.list(
                filters={'name': service_name})

            if len(running_services) > 0:
                return running_services[0]
            else:
                self._logger.warn(f'No service of {service_name} is running.')
                return None
        except docker.errors.APIError:
            self._logger.error(
                f'Could not list of services for {service_name}.')
            return None

    def scale_service(self, service_name: str, replicas: int):
        service = self.get_service_with_name(service_name)
        if service is not None:
            if replicas > 0:
                success = service.scale(replicas)
                return success

    def run_container(self, replicas: int, config):
        for _ in range(replicas):
            container_id = str(uuid.uuid4())
            container_name = f'{config.name_prefix}.{container_id}'

            self._logger.info(
                f'Trying to start container with name {container_name}')

            try:
                print(config.volumes)
                self._client.containers.run(config.image,
                                            detach=True,
                                            environment=config.environment,
                                            name=container_name,
                                            network=config.network,
                                            volumes=config.volumes,
                                            runtime=config.runtime)
            except docker.errors.ContainerError as error:
                self._logger.error(f'Couldnt start container. {error}')
                return False
            except docker.errors.ImageNotFound as error:
                self._logger.error(
                    f'Couldnt start container. Image {config.image} not found. {error}'
                )
                return False
            except docker.errors.APIError as error:
                self._logger.error(
                    f'Couldnt start container. API error. {error}')
                return False
            else:
                return True

    def remove_container(self, replicas: int, service_name: str):
        running_worker = list(
            filter(lambda container: container.name.startswith(service_name),
                   self._client.containers.list()))

        if len(running_worker) > 0:
            random_container = random.sample(running_worker, replicas)

            self._logger.info(f'Going to remove {replicas} containers')

            for container in random_container:
                try:
                    self._logger.info(
                        f'Trying to remove container with name {container.name}'
                    )
                    container.remove()
                except docker.errors.APIError as error:
                    self._logger.error(
                        f'Couldnt remove container ({container.name} - {container.short_id}). API error. {error}'
                    )
                    return False
                else:
                    return True
