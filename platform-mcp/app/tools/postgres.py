from app.clients.platform_api import PlatformAPIClient


platform_api = PlatformAPIClient()


def register_postgres_tools(mcp):

    @mcp.tool()
    def postgres_get_setting(
        cluster: str,
        parameter: str,
    ) -> dict:
        """
        Get the current value and metadata of a PostgreSQL
        configuration parameter from a PostgreSQL cluster.

        Args:
            cluster: Platform PostgreSQL cluster name, for example pg01.
            parameter: PostgreSQL setting name, for example wal_level.
        """

        return platform_api.postgres_get_setting(
            cluster,
            parameter,
        )

    @mcp.tool()
    def postgres_get_settings(
        cluster: str,
    ) -> dict:
        """
        Get all PostgreSQL configuration parameters for a cluster.

        Args:
            cluster: Platform PostgreSQL cluster name, for example pg01.
        """

        return platform_api.postgres_get_settings(
            cluster,
        )

    @mcp.tool()
    def postgres_reload(cluster: str) -> dict:
        """
        Reload the PostgreSQL configuration for the specified cluster.

        This calls pg_reload_conf() through the Platform API.
        It does not restart PostgreSQL.
        """
        return platform_api.postgres_reload(cluster)

    @mcp.tool()
    def postgres_uptime(cluster: str) -> dict:
        """
        Uptime of the specified cluster.

        This calls pg_postmaster_start_time and compares with now() 
        through the Platform API.
        """
        return platform_api.postgres_uptime(cluster)

    @mcp.tool()
    def postgres_get_databases(
        cluster: str,
    ) -> dict:
        """
        List all connectable non-template databases
        in the specified PostgreSQL cluster.
        """
        return platform_api.postgres_get_databases(
            cluster,
        )

    @mcp.tool(name="postgres_checkpoint")
    def checkpoint_postgres(
        cluster: str,
    ) -> dict:
        """
        Force a PostgreSQL checkpoint on the specified cluster.
        """
        return platform_api.postgres_checkpoint(
            cluster
        )

    @mcp.tool()
    def postgres_get_active_replication_slots(
        cluster: str,
    ) -> dict:
        """
        List all active replication slots
        in the specified PostgreSQL cluster.
        """
        return platform_api.postgres_get_active_replication_slots(
            cluster,
        )

    @mcp.tool()
    def postgres_analyze_table(
        cluster: str,
        table_name: str,
    ) -> dict:
        """
        Perform Analyze on a table
        in the specified PostgreSQL cluster.
        """
        return platform_api.postgres_analyze_table(
            cluster,
            table_name,
        )

    @mcp.tool()
    def postgres_vacuum_table(
        cluster: str,
        table_name: str,
    ) -> dict:
        """
        Perform Vacuum on a table 
        in the specified PostgreSQL cluster.
        """
        return platform_api.postgres_vacuum_table(
            cluster,
            table_name,
        )

    @mcp.tool()
    def postgres_set_parameter(
        cluster: str,
        parameter: str,
        value: str,
    ) -> dict:
        """
        Change an approved PostgreSQL reloadable parameter
        and reload the PostgreSQL configuration.
        """
        return platform_api.postgres_set_parameter(
            cluster,
            parameter,
            value,
        )

    @mcp.tool()
    def check_postgres(
        cluster: str,
        mode: str,
    ) -> dict:
        """
        Read or execute PostgreSQL SQL files configured for a cluster.

        mode:
        dry-run - return SQL statements without executing them
        run     - execute each SQL statement independently
        """
        return platform_api.check_postgres(
            cluster,
            mode,
        )