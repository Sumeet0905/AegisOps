from pathlib import Path

from app.db.session import get_conn

MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "app" / "db" / "migrations"


def main() -> None:
    with get_conn() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                filename TEXT PRIMARY KEY,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )
        for migration in sorted(MIGRATIONS_DIR.glob("*.sql")):
            applied = connection.execute(
                "SELECT 1 FROM schema_migrations WHERE filename = %s",
                (migration.name,),
            ).fetchone()
            if applied:
                continue
            connection.execute(migration.read_text(encoding="utf-8"), prepare=False)
            connection.execute(
                "INSERT INTO schema_migrations (filename) VALUES (%s)",
                (migration.name,),
            )
            print(f"Applied {migration.name}")


if __name__ == "__main__":
    main()
