"""
SQL Runtime Service (User-Space)

Executes SQL using the system `psql` binary.
No Python database drivers.
No pip.
No venv.
"""

import os
import subprocess
import tempfile


class SqlRuntimeService:
    def __init__(self):
        self.db_url = os.environ.get("SUPABASE_DB_URL")
        if not self.db_url:
            raise RuntimeError("SUPABASE_DB_URL not set")

    def execute(self, sql: str) -> str:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".sql") as f:
            f.write(sql)
            f.flush()

            proc = subprocess.run(
                [
                    "psql",
                    self.db_url,
                    "-f",
                    f.name,
                    "-A",      # unaligned
                    "-F", ",", # CSV
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

        if proc.returncode != 0:
            raise RuntimeError(proc.stderr)

        return proc.stdout
