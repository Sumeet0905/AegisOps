from psycopg.rows import dict_row

from app.db.session import get_conn
from app.domain.models import Customer, Order


def get_customer(customer_id: str) -> Customer | None:
    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT customer_id, name, tier, region, created_at
            FROM customers WHERE customer_id = %s
            """,
            (customer_id,),
            row_factory=dict_row,
        ).fetchone()
    return Customer(**row) if row else None


def list_customer_orders(customer_id: str, limit: int = 50) -> list[Order]:
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT order_id, customer_id, status, amount_cents, created_at, updated_at
            FROM orders WHERE customer_id = %s
            ORDER BY created_at DESC LIMIT %s
            """,
            (customer_id, limit),
            row_factory=dict_row,
        ).fetchall()
    return [Order(**row) for row in rows]
