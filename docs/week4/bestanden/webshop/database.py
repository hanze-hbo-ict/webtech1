"""
Database module voor de webshop Flask applicatie.

Deze module bevat de WebshopDatabase class die alle database operaties
afhandelt. We hergebruiken de webshop.sqlite database uit Week 3.
"""
import sqlite3
from sqlite3 import Row


class WebshopDatabase:
    """Database class voor webshop queries."""

    def __init__(self, db_path: str = "../../../week3/bestanden/webshop.sqlite"):
        """Initialiseer database connectie.

        Args:
            db_path: Pad naar de webshop.sqlite database
        """
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        """Maak database connectie met Row factory.

        Returns:
            Database connectie object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = Row
        return conn

    # ==================== CATEGORIES ====================

    def get_all_categories(self) -> list[Row]:
        """Haal alle categorieën op.

        Returns:
            Lijst met alle categorieën
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, name, description
                FROM categories
                ORDER BY name
            """)
            return cursor.fetchall()

    def get_category_by_id(self, category_id: int) -> Row | None:
        """Haal één categorie op op basis van ID.

        Args:
            category_id: ID van de categorie

        Returns:
            Row met categorie data of None
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, name, description FROM categories WHERE id = ?",
                (category_id,)
            )
            return cursor.fetchone()

    # ==================== PRODUCTS ====================

    def get_all_products(self, limit: int = 50) -> list[Row]:
        """Haal alle producten op met categorie info.

        Args:
            limit: Maximum aantal producten (default: 50)

        Returns:
            Lijst met producten
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    p.id,
                    p.name,
                    p.price,
                    p.stock,
                    p.description,
                    c.name AS category_name,
                    c.id AS category_id
                FROM products p
                JOIN categories c ON p.category_id = c.id
                ORDER BY p.name
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()

    def get_product_by_id(self, product_id: int) -> Row | None:
        """Haal één product op met categorie info.

        Args:
            product_id: ID van het product

        Returns:
            Row met product data of None
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    p.id,
                    p.name,
                    p.price,
                    p.stock,
                    p.description,
                    c.name AS category_name,
                    c.id AS category_id
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.id = ?
            """, (product_id,))
            return cursor.fetchone()

    def get_products_by_category(self, category_id: int) -> list[Row]:
        """Haal alle producten van een categorie op.

        Args:
            category_id: ID van de categorie

        Returns:
            Lijst met producten in deze categorie
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    p.id,
                    p.name,
                    p.price,
                    p.stock,
                    p.description
                FROM products p
                WHERE p.category_id = ?
                ORDER BY p.name
            """, (category_id,))
            return cursor.fetchall()

    def search_products(self, search_term: str) -> list[Row]:
        """Zoek producten op naam.

        Args:
            search_term: Zoekterm voor product naam

        Returns:
            Lijst met matchende producten
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    p.id,
                    p.name,
                    p.price,
                    p.stock,
                    c.name AS category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.name LIKE ?
                ORDER BY p.name
            """, (f"%{search_term}%",))
            return cursor.fetchall()

    # ==================== STATISTICS ====================

    def get_category_stats(self) -> list[Row]:
        """Haal statistieken op per categorie.

        Returns:
            Lijst met statistieken per categorie
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    c.id,
                    c.name,
                    COUNT(p.id) AS product_count,
                    AVG(p.price) AS avg_price
                FROM categories c
                LEFT JOIN products p ON c.id = p.category_id
                GROUP BY c.id, c.name
                ORDER BY c.name
            """)
            return cursor.fetchall()
