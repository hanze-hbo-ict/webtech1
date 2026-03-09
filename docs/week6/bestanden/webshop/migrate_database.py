"""
Migrate data van Week 3 webshop.sqlite naar Week 6 SQLAlchemy database.

Dit script kopieert categorieën en producten van de raw SQL database
naar de nieuwe SQLAlchemy database. Handig voor migratie en om te
zien hoe ORM en raw SQL samen kunnen werken.
"""
import sqlite3
import os
from app import app, db
from models import Category, Product

# Pad naar Week 3 database
SOURCE_DB = "../../../week3/bestanden/webshop.sqlite"


def migrate_data():
    """Migreer alle data van Week 3 database naar Week 6 ORM database."""

    if not os.path.exists(SOURCE_DB):
        print(f"❌ Source database niet gevonden: {SOURCE_DB}")
        print("   Pas het pad aan in dit script.")
        return

    print("=== Database Migratie: Raw SQL → SQLAlchemy ORM ===\n")

    # Maak connection naar source database
    source_conn = sqlite3.connect(SOURCE_DB)
    source_conn.row_factory = sqlite3.Row
    source_cursor = source_conn.cursor()

    with app.app_context():
        # Drop existing tables and recreate
        print("1️⃣  Creating fresh database tables...")
        db.drop_all()
        db.create_all()
        print("   ✅ Tabellen aangemaakt\n")

        # Migreer categorieën
        print("2️⃣  Migrating categories...")
        source_cursor.execute("SELECT * FROM categories ORDER BY id")
        categories_data = source_cursor.fetchall()

        category_count = 0
        for row in categories_data:
            category = Category(
                name=row['name'],
                description=row['description']
            )
            # Preserve original ID
            category.id = row['id']
            db.session.add(category)
            category_count += 1

        db.session.commit()
        print(f"   ✅ {category_count} categorieën gemigreerd\n")

        # Migreer producten
        print("3️⃣  Migrating products...")
        source_cursor.execute("SELECT * FROM products ORDER BY id")
        products_data = source_cursor.fetchall()

        product_count = 0
        for row in products_data:
            product = Product(
                name=row['name'],
                price=row['price'],
                stock=row['stock'],
                category_id=row['category_id'],
                description=row['description']
            )
            # Preserve original ID
            product.id = row['id']
            db.session.add(product)
            product_count += 1

        db.session.commit()
        print(f"   ✅ {product_count} producten gemigreerd\n")

    source_conn.close()

    print("=" * 50)
    print("✅ Migratie succesvol!")
    print(f"   Categorieën: {category_count}")
    print(f"   Producten: {product_count}")
    print("=" * 50)


def verify_migration():
    """Verifieer de gemigreerde data."""
    print("\n=== Verificatie ===\n")

    with app.app_context():
        categories = db.session.execute(db.select(Category)).scalars().all()
        products = db.session.execute(db.select(Product)).scalars().all()

        print(f"Categories in database: {len(categories)}")
        print(f"Products in database: {len(products)}")

        # Toon eerste paar categorieën
        print("\nEerste 3 categorieën:")
        for cat in categories[:3]:
            print(f"  - {cat.name} ({cat.product_count} producten)")

        # Toon eerste paar producten
        print("\nEerste 3 producten:")
        for prod in products[:3]:
            print(f"  - {prod.name} (€{prod.price:.2f}) - {prod.category.name}")


if __name__ == "__main__":
    migrate_data()
    verify_migration()

    print("\n💡 Tip: Run nu 'python app.py' om de applicatie te starten!")
