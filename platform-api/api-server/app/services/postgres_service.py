from app.clients.postgres_client import PostgresClient
from app.core.config import load_clusters

from pathlib import Path
import yaml

CONFIG_FILE = (
    Path(__file__).resolve().parents[1]
    / "config"
    / "postgres_reload_params.yaml"
)


class PostgresService:

    def __init__(self):
        self.clusters = load_clusters()

    def _normalize_cluster_name(
        self,
        cluster_name: str,
    ) -> str:

        return cluster_name.strip().lower()

    def _get_client(self, cluster_name: str) -> PostgresClient:
        
        cluster_name = self._normalize_cluster_name(
            cluster_name
        )

        cluster = self.clusters.get(cluster_name)

        if cluster is None:
            raise ValueError(
                f"Unknown PostgreSQL cluster: {cluster_name}"
            )

        return PostgresClient(
            host=cluster["host"],
            port=cluster.get("port", 5432),
            database=cluster.get("database", "postgres"),
        )

    def get_settings(self, cluster_name: str):

        client = self._get_client(cluster_name)
        return client.get_settings()

    def get_setting(
        self,
        cluster_name: str,
        parameter: str,
    ):

        client = self._get_client(cluster_name)

        setting = client.get_setting(parameter)

        if setting is None:
            raise KeyError(
                f"Unknown PostgreSQL setting: {parameter}"
            )

        return setting

    def reload_config(self, cluster_name: str):

        client = self._get_client(cluster_name)
        return client.reload_config()

    def uptime(self, cluster_name: str):

        client = self._get_client(cluster_name)
        return client.uptime()

    def get_databases(self, cluster_name: str):

        client = self._get_client(cluster_name)
        return client.get_databases()
    
    def checkpoint(
        self,
        cluster_name: str,
    ):
        client = self._get_client(cluster_name)

        return client.checkpoint()

    def get_active_replication_slots(self, cluster_name: str):

        client = self._get_client(cluster_name)
        return client.get_active_replication_slots()

    def analyze_table(
        self,
        cluster_name: str,
        table_name: str,
    ):

        client = self._get_client(cluster_name)

        return client.analyze_table(table_name)

    def vacuum_table(
        self,
        cluster_name: str,
        table_name: str,
    ):

        client = self._get_client(cluster_name)

        return client.vacuum_table(table_name)

    def _load_allowed_reload_parameters(self) -> set[str]:
        with open(CONFIG_FILE, "r") as f:
            data = yaml.safe_load(f)

        return set(
            data["allowed_reload_parameters"].keys()
        )
    
    def postgres_set_parameter(
        self,
        cluster_name: str,
        parameter: str,
        value: str,
    ):
        allowed = self._load_allowed_reload_parameters()

        if parameter not in allowed:
            raise ValueError(
                f"Parameter not allowed for reload: {parameter}"
            )

        client = self._get_client(cluster_name)

        return client.postgres_set_parameter(
            parameter,
            value,
        )

    def check_postgres(
        self,
        cluster_name: str,
        mode: str,
    ):

        cluster_name = self._normalize_cluster_name(
            cluster_name
        )

        cluster = self.clusters.get(cluster_name)

        if not cluster:
            raise ValueError(
                f"Unknown PostgreSQL cluster: {cluster_name}"
            )

        client = self._get_client(cluster_name)

        return client.check_postgres(
            datadir=cluster["datadir"],
            mode=mode,
        )