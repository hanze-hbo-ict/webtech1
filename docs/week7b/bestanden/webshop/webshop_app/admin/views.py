"""
Admin Blueprint - Admin panel views (Week 7b).

Deze blueprint bevat alle admin routes voor product beheer:
- Product overzicht
- Product toevoegen
- Product bewerken
- Product verwijderen

Alle routes zijn beschermd met @admin_required decorator.
Deze blueprint wordt geregistreerd met url_prefix='/admin'.
"""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from functools import wraps
from webshop_app.models import db, Category, Product
from webshop_app.admin.forms import AddProductForm, EditProductForm

# Maak blueprint aan
admin_bp = Blueprint(
    'admin',
    __name__,
    template_folder='templates'
)


def admin_required(f):
    """Decorator om routes te beschermen voor alleen admins.

    Gebruik dit naast @login_required om te controleren of de ingelogde
    gebruiker admin rechten heeft.

    Args:
        f: De view functie om te beschermen

    Returns:
        Wrapped functie die admin rechten controleert
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Log in om deze pagina te bekijken.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash('Deze pagina is alleen toegankelijk voor admins.', 'danger')
            return redirect(url_for('products.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/products")
@admin_required
def products():
    """Admin overzicht van alle producten.

    Route: /admin/products

    Alleen toegankelijk voor admins.

    Returns:
        Rendered HTML template met product lijst
    """
    all_products = db.session.execute(db.select(Product).join(Category)).scalars().all()
    return render_template("admin/products.html", products=all_products)


@admin_bp.route("/product/add", methods=['GET', 'POST'])
@admin_required
def add_product():
    """Admin formulier om een nieuw product toe te voegen.

    Route: /admin/product/add

    Alleen toegankelijk voor admins.

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
        return redirect(url_for('products.product', product_id=new_product.id))

    return render_template("admin/add_product.html", form=form)


@admin_bp.route("/product/edit/<int:product_id>", methods=['GET', 'POST'])
@admin_required
def edit_product(product_id: int):
    """Admin formulier om een bestaand product te bewerken.

    Route: /admin/product/edit/<id>

    Alleen toegankelijk voor admins.

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
        return redirect(url_for('products.product', product_id=product_id))

    # Pre-fill form met huidige product data (bij GET request)
    elif not form.is_submitted():
        form.name.data = product_info.name
        form.price.data = product_info.price
        form.stock.data = product_info.stock
        form.description.data = product_info.description
        form.category_id.data = product_info.category_id

    return render_template(
        "admin/edit_product.html",
        form=form,
        product=product_info
    )


@admin_bp.route("/product/delete/<int:product_id>", methods=['POST'])
@admin_required
def delete_product(product_id: int):
    """Admin route om een product te verwijderen.

    Route: /admin/product/delete/<id>

    Alleen toegankelijk voor admins.

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

    product_name = product_info.name

    # Delete product
    db.session.delete(product_info)
    db.session.commit()

    flash(f'Product "{product_name}" succesvol verwijderd.', 'success')
    return redirect(url_for('admin.products'))
