"""
Webshop Flask Applicatie met SQLAlchemy ORM (Week 6).

Deze versie gebruikt SQLAlchemy models in plaats van raw SQL queries.
We hergebruiken de formulieren uit Week 5, maar vervangen alle
database operaties door ORM queries.
"""
import os
from flask import Flask, render_template, abort, redirect, url_for, flash
from models import db, Category, Product, Customer, Order, OrderItem
from forms import AddProductForm, EditProductForm, ContactForm

# Bepaal database pad
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Flask configuratie
app.config['SECRET_KEY'] = 'webshop-secret-key-2025'

# SQLAlchemy configuratie
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'webshop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)


@app.route("/")
def index() -> str:
    """Homepage met overzicht van alle categorieën.

    Returns:
        Rendered HTML template
    """
    # ORM Query: SELECT * FROM categories
    categories = db.session.execute(db.select(Category)).scalars().all()
    return render_template("index.html", categories=categories)


@app.route("/category/<int:category_id>")
def category(category_id: int) -> str:
    """Categorie overzicht met alle producten.

    Args:
        category_id: ID van de categorie

    Returns:
        Rendered HTML template

    Raises:
        404: Als categorie niet bestaat
    """
    # ORM Query: SELECT * FROM categories WHERE id = ?
    category_info = db.get_or_404(Category, category_id)

    # ORM Query: SELECT * FROM products WHERE category_id = ?
    products = db.session.execute(db.select(Product).filter_by(category_id=category_id)).scalars().all()

    return render_template(
        "category.html",
        category=category_info,
        products=products
    )


@app.route("/product/<int:product_id>")
def product(product_id: int) -> str:
    """Product detail pagina.

    Args:
        product_id: ID van het product

    Returns:
        Rendered HTML template

    Raises:
        404: Als product niet bestaat
    """
    # ORM Query: SELECT * FROM products WHERE id = ?
    product_info = db.get_or_404(Product, product_id)

    return render_template("product.html", product=product_info)


@app.route("/admin/products")
def admin_products() -> str:
    """Admin overzicht van alle producten.

    Returns:
        Rendered HTML template met product lijst
    """
    # ORM Query: SELECT * FROM products JOIN categories
    products = db.session.execute(db.select(Product).join(Category)).scalars().all()
    return render_template("admin_products.html", products=products)


@app.route("/admin/product/add", methods=['GET', 'POST'])
def admin_add_product() -> str:
    """Admin formulier om een nieuw product toe te voegen.

    Returns:
        Rendered HTML template of redirect

    Methods:
        GET: Toon formulier
        POST: Verwerk formulier en voeg product toe
    """
    form = AddProductForm()

    # Populate category choices
    form.category_id.choices = [(c.id, c.name) for c in db.session.execute(db.select(Category)).scalars().all()]

    if form.validate_on_submit():
        # Create new product instance
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data,
            description=form.description.data
        )

        # Save to database
        db.session.add(new_product)
        db.session.commit()

        flash(f'Product "{new_product.name}" succesvol toegevoegd!', 'success')
        return redirect(url_for('product', product_id=new_product.id))

    return render_template("add_product.html", form=form)


@app.route("/admin/product/edit/<int:product_id>", methods=['GET', 'POST'])
def admin_edit_product(product_id: int) -> str:
    """Admin formulier om een bestaand product te bewerken.

    Args:
        product_id: ID van het product om te bewerken

    Returns:
        Rendered HTML template of redirect

    Methods:
        GET: Toon formulier met huidige product data
        POST: Verwerk formulier en update product

    Raises:
        404: Als product niet bestaat
    """
    # Get product or 404
    product_info = db.get_or_404(Product, product_id)

    form = EditProductForm()

    # Populate category choices
    form.category_id.choices = [(c.id, c.name) for c in db.session.execute(db.select(Category)).scalars().all()]

    if form.validate_on_submit():
        # Update product attributes
        product_info.name = form.name.data
        product_info.price = form.price.data
        product_info.stock = form.stock.data
        product_info.category_id = form.category_id.data
        product_info.description = form.description.data

        # Save changes
        db.session.commit()

        flash(f'Product "{product_info.name}" succesvol gewijzigd!', 'success')
        return redirect(url_for('product', product_id=product_id))

    # Pre-fill form met huidige product data (bij GET request)
    elif not form.is_submitted():
        form.name.data = product_info.name
        form.price.data = product_info.price
        form.stock.data = product_info.stock
        form.description.data = product_info.description
        form.category_id.data = product_info.category_id

    return render_template(
        "edit_product.html",
        form=form,
        product=product_info
    )


@app.route("/admin/product/delete/<int:product_id>", methods=['POST'])
def admin_delete_product(product_id: int) -> str:
    """Admin route om een product te verwijderen.

    Args:
        product_id: ID van het product om te verwijderen

    Returns:
        Redirect naar admin products overzicht

    Methods:
        POST: Verwijder product (alleen via POST voor veiligheid)

    Raises:
        404: Als product niet bestaat
    """
    # Get product or 404
    product_info = db.get_or_404(Product, product_id)

    # Delete product
    db.session.delete(product_info)
    db.session.commit()

    flash(f'Product "{product_info.name}" succesvol verwijderd.', 'success')
    return redirect(url_for('admin_products'))


@app.route("/contact", methods=['GET', 'POST'])
def contact() -> str:
    """Contact formulier voor klanten.

    Returns:
        Rendered HTML template

    Methods:
        GET: Toon formulier
        POST: Verwerk formulier (toon bevestiging)
    """
    form = ContactForm()

    if form.validate_on_submit():
        flash(
            f'Bedankt voor je bericht, {form.name.data}! '
            f'We nemen zo snel mogelijk contact met je op.',
            'success'
        )
        return redirect(url_for('index'))

    return render_template("contact.html", form=form)


@app.errorhandler(404)
def page_not_found(error) -> tuple[str, int]:
    """Custom 404 error handler.

    Args:
        error: Error object

    Returns:
        Tuple van (HTML, status_code)
    """
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)
