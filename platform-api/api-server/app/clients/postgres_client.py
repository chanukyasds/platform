import os

import psycopg
from psycopg.rows import dict_row
from psycopg import sql


class PostgresClient:

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
    ):
        self.connection_params = {
            "host": host,
            "port": port,
            "dbname": database,
            "user": os.environ["POSTGRES_USER"],
            "password": os.environ["POSTGRES_PASSWORD"],
            "connect_timeout": 5,
        }

    def get_settings(self) -> list[dict]:

        query = """
            SELECT
                name,
                setting,
                unit,
                category,
                short_desc,
                context,
                source,
                sourcefile,
                sourceline,
                pending_restart
            FROM pg_settings
            ORDER BY name;
        """

        with psycopg.connect(
            **self.connection_params,
            row_factory=dict_row,
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    def get_setting(self, parameter: str) -> dict | None:

        query = """
            SELECT
                name,
                setting,
                unit,
                category,
                short_desc,
                context,
                source,
                sourcefile,
                sourceline,
                pending_restart
            FROM pg_settings
            WHERE lower(name) = lower(%s);
        """

        with psycopg.connect(
            **self.connection_params,
            row_factory=dict_row,
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute(query, (parameter,))
                return cursor.fetchone()


    def reload_config(self) -> dict:

        query = """
            SELECT
                pg_reload_conf() AS reloaded,
                pg_conf_load_time() AS config_load_time,
                now() AS exact_load_time;
        """

        with psycopg.connect(
            **self.connection_params,
            row_factory=dict_row,
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchone()

    def uptime(self) -> dict:

        query = """
            SELECT
            pg_postmaster_start_time() AS postmaster_start_time,
            (now() - pg_postmaster_start_time())::text AS uptime;
        """

        with psycopg.connect(
            **self.connection_params,
            row_factory=dict_row,
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchone()

    def get_databases(self) -> list[dict]:

        query = """
            SELECT
                datname as database,
                pg_size_pretty(pg_database_size(datname)) AS database_size
            FROM pg_database
            WHERE datistemplate = false
            AND datallowconn = true
            ORDER BY datname;
        """

        with psycopg.connect(
            **self.connection_params,
            row_factory=dict_row,
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    def get_active_replication_slots(self) -> list[dict]:

        query = """
            SELECT
                slot_name,
                slot_type,
                active,
                restart_lsn,
                confirmed_flush_lsn
            FROM pg_replication_slots;
        """

        with psycopg.connect(
            **self.connection_params,
            row_factory=dict_row,
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    def checkpoint(self) -> dict:
        query = "CHECKPOINT;"

        with psycopg.connect(
            **self.connection_params,
            row_factory=dict_row,
            autocommit=True,
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute(query)

        return {
            "checkpoint": True
        }

    def analyze_table(self, table_name: str) -> dict:

        parts = table_name.split(".", 1)

        if len(parts) == 2:
            schema_name, relation_name = parts

            query = sql.SQL("ANALYZE {}.{};").format(
                sql.Identifier(schema_name),
                sql.Identifier(relation_name),
            )
        else:
            query = sql.SQL("ANALYZE {};").format(
                sql.Identifier(table_name)
            )

        with psycopg.connect(
            **self.connection_params,
            row_factory=dict_row,
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute(query)

        return {
            "table": table_name,
            "analyzed": True,
        }

    def vacuum_table(self, table_name: str) -> dict:
        parts = table_name.split(".", 1)

        if len(parts) == 2:
            schema_name, relation_name = parts

            query = sql.SQL("VACUUM {}.{};").format(
                sql.Identifier(schema_name),
                sql.Identifier(relation_name),
            )
        else:
            query = sql.SQL("VACUUM {};").format(
                sql.Identifier(table_name)
            )

        with psycopg.connect(
            **self.connection_params,
            row_factory=dict_row,
            autocommit=True,
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute(query)

        return {
            "table": table_name,
            "vacuumed": True,
        }

    def postgres_set_parameter(
        self,
        parameter: str,
        value: str,
    ) -> dict:

        query = sql.SQL(
            "ALTER SYSTEM SET {} = {};"
        ).format(
            sql.Identifier(parameter),
            sql.Literal(value),
        )

        with psycopg.connect(
            **self.connection_params,
            row_factory=dict_row,
            autocommit=True,
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute(query)

                cursor.execute(
                    "SELECT pg_reload_conf() AS reloaded;"
                )

                return cursor.fetchone()

    def check_postgres(
        self,
        datadir: str,
        mode: str,
    ) -> dict:

        sql_dir = f"{datadir}/sql"

        list_query = """
            SELECT filename
            FROM pg_ls_dir(%s) AS filename
            WHERE filename LIKE '%%.sql'
            ORDER BY filename;
        """

        with psycopg.connect(
            **self.connection_params,
            row_factory=dict_row,
            autocommit=True,
        ) as conn:

            with conn.cursor() as cursor:

                cursor.execute(
                    list_query,
                    (sql_dir,),
                )

                files = cursor.fetchall()
                scripts = []

                for row in files:
                    filename = row["filename"]
                    full_path = f"{sql_dir}/{filename}"

                    cursor.execute(
                        "SELECT pg_read_file(%s) AS sql;",
                        (full_path,),
                    )

                    content = cursor.fetchone()["sql"]

                    statements = [
                        statement.strip() + ";"
                        for statement in content.split(";")
                        if statement.strip()
                    ]

                    scripts.append({
                        "file": filename,
                        "statements": statements,
                    })

                if mode == "dry-run":
                    return {
                        "mode": "dry-run",
                        "files": scripts,
                    }

                if mode != "run":
                    raise ValueError(
                        "mode must be either 'dry-run' or 'run'"
                    )

                results = []

                for script in scripts:
                    statement_results = []

                    for statement in script["statements"]:
                        try:
                            cursor.execute(
                                statement,
                                prepare=False,
                            )

                            statement_results.append({
                                "sql": statement,
                                "success": True,
                            })

                        except Exception as exc:
                            statement_results.append({
                                "sql": statement,
                                "success": False,
                                "error": str(exc),
                            })

                    results.append({
                        "file": script["file"],
                        "statements": statement_results,
                    })

                return {
                    "mode": "run",
                    "files": results,
                }