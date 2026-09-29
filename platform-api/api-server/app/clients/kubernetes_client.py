import os

from kubernetes import client


class KubernetesClient:

    def __init__(
        self,
        api_server: str,
        ca_cert: str,
    ):
        token = os.environ["K8S_API_TOKEN"]

        configuration = client.Configuration()

        configuration.host = api_server
        configuration.ssl_ca_cert = ca_cert
        configuration.verify_ssl = True

        # Kubernetes Python client expects the complete
        # Authorization header value here.
        configuration.api_key["authorization"] = f"Bearer {token}"

        api_client = client.ApiClient(configuration)

        self.core_api = client.CoreV1Api(api_client)
        self.apps_api = client.AppsV1Api(api_client)

    def get_nodes(self) -> list[dict]:

        result = self.core_api.list_node()

        nodes = []

        for node in result.items:

            ready = False

            for condition in node.status.conditions or []:
                if condition.type == "Ready":
                    ready = condition.status == "True"
                    break

            roles = []

            for label in node.metadata.labels or {}:
                if label.startswith("node-role.kubernetes.io/"):
                    roles.append(
                        label.split("/", 1)[1]
                    )

            if not roles:
                roles.append("worker")

            nodes.append(
                {
                    "name": node.metadata.name,
                    "ready": ready,
                    "roles": roles,
                    "kubernetes_version":
                        node.status.node_info.kubelet_version,
                    "os":
                        node.status.node_info.os_image,
                    "architecture":
                        node.status.node_info.architecture,
                }
            )

        return nodes

    def get_namespaces(self) -> list[dict]:

        result = self.core_api.list_namespace()

        namespaces = []

        for namespace in result.items:
            namespaces.append(
                {
                    "name": namespace.metadata.name,
                    "status": namespace.status.phase,
                    "created_at": namespace.metadata.creation_timestamp,
                }
            )

        return namespaces


    def get_deployments(self) -> list[dict]:

        result = self.apps_api.list_deployment_for_all_namespaces()

        deployments = []

        for deployment in result.items:

            deployments.append(
                {
                    "name": deployment.metadata.name,
                    "namespace": deployment.metadata.namespace,
                    "replicas": deployment.spec.replicas,
                    "ready_replicas":
                        deployment.status.ready_replicas or 0,
                    "available_replicas":
                        deployment.status.available_replicas or 0,
                    "updated_replicas":
                        deployment.status.updated_replicas or 0,
                    "created_at":
                        deployment.metadata.creation_timestamp,
                }
            )

        return deployments


    def get_deployment(
        self,
        namespace: str,
        name: str,
    ) -> dict:

        deployment = self.apps_api.read_namespaced_deployment(
            name=name,
            namespace=namespace,
        )

        containers = []

        for container in deployment.spec.template.spec.containers:
            containers.append(
                {
                    "name": container.name,
                    "image": container.image,
                }
            )

        return {
            "name": deployment.metadata.name,
            "namespace": deployment.metadata.namespace,
            "replicas": deployment.spec.replicas,
            "ready_replicas":
                deployment.status.ready_replicas or 0,
            "available_replicas":
                deployment.status.available_replicas or 0,
            "updated_replicas":
                deployment.status.updated_replicas or 0,
            "containers": containers,
            "created_at":
                deployment.metadata.creation_timestamp,
        }

    def get_statefulsets(self) -> list[dict]:

        result = self.apps_api.list_stateful_set_for_all_namespaces()

        statefulsets = []

        for sts in result.items:

            containers = [
                {
                    "name": container.name,
                    "image": container.image,
                }
                for container in sts.spec.template.spec.containers
            ]

            statefulsets.append(
                {
                    "name": sts.metadata.name,
                    "namespace": sts.metadata.namespace,
                    "replicas": sts.spec.replicas,
                    "ready_replicas": sts.status.ready_replicas or 0,
                    "current_replicas": sts.status.current_replicas or 0,
                    "updated_replicas": sts.status.updated_replicas or 0,
                    "containers": containers,
                    "created_at": sts.metadata.creation_timestamp,
                }
            )

        return statefulsets


    def get_statefulset(
        self,
        namespace: str,
        name: str,
    ) -> dict:

        sts = self.apps_api.read_namespaced_stateful_set(
            name=name,
            namespace=namespace,
        )

        containers = [
            {
                "name": container.name,
                "image": container.image,
            }
            for container in sts.spec.template.spec.containers
        ]

        return {
            "name": sts.metadata.name,
            "namespace": sts.metadata.namespace,
            "replicas": sts.spec.replicas,
            "ready_replicas": sts.status.ready_replicas or 0,
            "current_replicas": sts.status.current_replicas or 0,
            "updated_replicas": sts.status.updated_replicas or 0,
            "service_name": sts.spec.service_name,
            "containers": containers,
            "created_at": sts.metadata.creation_timestamp,
        }