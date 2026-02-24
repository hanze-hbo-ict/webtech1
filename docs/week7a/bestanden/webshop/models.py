"""
SQLAlchemy models voor de webshop applicatie met User Authentication (Week 7a).

Dit bestand bevat alle database models (ORM) voor de webshop.

Week 7a toevoegingen:
- Flask-Login integratie voor user authentication
- Password hashing met Werkzeug
- Admin vs Customer roles
- UserMixin voor ingebouwde Flask-Login methoden

Models:
- Category: Productcategorieën
- Product: Producten (met foreign key naar Category)
- Customer: Klanten met authenticatie
- Order: Bestellingen (met foreign key naar Customer)
- OrderItem: Bestelregels (many-to-many tussen Order en Product)
"""
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: int) -> 'Customer | None':
    """Laad een gebruiker op basis van het user ID.

    Deze functie wordt gebruikt door Flask-Login om de huidige gebruiker
    te laden uit de sessie.

    Args:
        user_id: Het ID van de gebruiker om te laden

    Returns:
        De Customer instantie als gevonden, anders None
    """
    return db.session.get(Customer, int(user_id))


class Category(db.Model):
    """Model voor productcategorieën.

    Relationships:
        products: One-to-Many naar Product
    """
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None]

    # Relationship
    products: Mapped[list['Product']] = relationship(back_populates='category')

    def __init__(self, name: str, description: str | None = None):
        """Maak nieuwe categorie aan.

        Args:
            name: Categorienaam
            description: Optionele beschrijving
        """
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f'<Category {self.name}>'

    @property
    def product_count(self) -> int:
        """Tel aantal producten in deze categorie.

        Returns:
            Aantal producten
        """
        return len(self.products)


class Product(db.Model):
    """Model voor producten.

    Attributes:
        id: Primary key
        name: Productnaam
        price: Prijs in euro's
        stock: Voorraad aantal
        description: Product beschrijving
        category_id: Foreign key naar Category

    Relationships:
        category: Many-to-One naar Category
        order_items: One-to-Many naar OrderItem
    """
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    price: Mapped[float]
    stock: Mapped[int] = mapped_column(default=0)
    description: Mapped[str | None]

    # Foreign Key
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    # Relationships
    category: Mapped['Category'] = relationship(back_populates='products')
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='product')

    def __init__(
        self,
        name: str,
        price: float,
        stock: int,
        category_id: int,
        description: str | None = None
    ):
        """Maak nieuw product aan.

        Args:
            name: Productnaam
            price: Prijs in euro's
            stock: Voorraad aantal
            category_id: ID van de categorie
            description: Optionele beschrijving
        """
        self.name = name
        self.price = price
        self.stock = stock
        self.category_id = category_id
        self.description = description

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f'<Product {self.name}>'

    @property
    def in_stock(self) -> bool:
        """Check of product op voorraad is.

        Returns:
            True als voorraad > 0
        """
        return self.stock > 0


class Customer(db.Model, UserMixin):
    """Model voor klanten met authenticatie (Week 7a).

    Erft van db.Model voor database functionaliteit en UserMixin voor
    ingebouwde Flask-Login methoden zoals is_authenticated(), is_active(),
    is_anonymous(), en get_id().

    Attributes:
        id: Primary key
        name: Klantnaam
        email: Email adres (uniek)
        password_hash: Gehashed wachtwoord
        is_admin: Admin rechten (True voor admin, False voor customer)
        created_at: Registratie datum

    Relationships:
        orders: One-to-Many naar Order
    """
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(200))
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    # Relationship
    orders: Mapped[list['Order']] = relationship(back_populates='customer')

    def __init__(self, name: str, email: str, password: str, is_admin: bool = False):
        """Maak nieuwe klant aan met authenticatie.

        Het wachtwoord wordt automatisch gehashed voordat het opgeslagen wordt.

        Args:
            name: Klantnaam
            email: Email adres
            password: Wachtwoord in plain text (wordt automatisch gehashed)
            is_admin: True voor admin rechten, False voor normale customer
        """
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def check_password(self, password: str) -> bool:
        """Controleer of het opgegeven wachtwoord correct is.

        Args:
            password: Het te verifiëren wachtwoord in plain text

        Returns:
            True als het wachtwoord overeenkomt, anders False
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        admin_tag = " (Admin)" if self.is_admin else ""
        return f'<Customer {self.name}{admin_tag}>'

    @property
    def order_count(self) -> int:
        """Tel aantal bestellingen van deze klant.

        Returns:
            Aantal bestellingen
        """
        return len(self.orders)


class Order(db.Model):
    """Model voor bestellingen.

    Attributes:
        id: Primary key
        customer_id: Foreign key naar Customer
        order_date: Bestellingsdatum
        status: Bestellingstatus
        total_amount: Totaalbedrag

    Relationships:
        customer: Many-to-One naar Customer
        order_items: One-to-Many naar OrderItem
    """
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))
    order_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    status: Mapped[str] = mapped_column(String(50), default='Pending')  # Pending, Confirmed, Shipped, Delivered
    total_amount: Mapped[float] = mapped_column(default=0.0)

    # Relationships
    customer: Mapped['Customer'] = relationship(back_populates='orders')
    order_items: Mapped[list['OrderItem']] = relationship(
        back_populates='order', cascade='all, delete-orphan'
    )

    def __init__(self, customer_id: int):
        """Maak nieuwe bestelling aan.

        Args:
            customer_id: ID van de klant
        """
        self.customer_id = customer_id

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f'<Order {self.id} - {self.status}>'

    def calculate_total(self) -> float:
        """Bereken totaalbedrag van bestelling.

        Returns:
            Totaalbedrag in euro's
        """
        total = sum(item.subtotal for item in self.order_items)
        self.total_amount = total
        return total

    @property
    def item_count(self) -> int:
        """Tel aantal items in bestelling.

        Returns:
            Aantal order items
        """
        return sum(item.quantity for item in self.order_items)


class OrderItem(db.Model):
    """Model voor bestelregels (many-to-many tussen Order en Product).

    Attributes:
        id: Primary key
        order_id: Foreign key naar Order
        product_id: Foreign key naar Product
        quantity: Aantal
        price: Prijs op moment van bestellen

    Relationships:
        order: Many-to-One naar Order
        product: Many-to-One naar Product
    """
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[float]  # Prijs op moment van bestellen

    # Relationships
    order: Mapped['Order'] = relationship(back_populates='order_items')
    product: Mapped['Product'] = relationship(back_populates='order_items')

    def __init__(self, order_id: int, product_id: int, quantity: int, price: float):
        """Maak nieuwe bestelregel aan.

        Args:
            order_id: ID van de bestelling
            product_id: ID van het product
            quantity: Aantal
            price: Prijs per stuk
        """
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f'<OrderItem {self.quantity}x Product #{self.product_id}>'

    @property
    def subtotal(self) -> float:
        """Bereken subtotaal van deze order regel.

        Returns:
            Quantity * price
        """
        return self.quantity * self.price
