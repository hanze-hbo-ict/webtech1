"""
Products Blueprint - Product catalog views (Week 7b).

Deze blueprint bevat alle routes voor de publieke product catalog:
- Homepage met categorieën
- Categorie pagina met producten
- Product detail pagina
- Contact pagina

Deze views zijn publiek toegankelijk (geen login vereist).
"""
from flask import Blueprint, render_template, redirect, url_for, flash
from webshop_app.models import db, Category, Product
from webshop_app.products.forms import ContactForm

# Maak blueprint aan
# template_folder is relatief aan deze file (views.py)
products_bp = Blueprint(
    'products',
    __name__,
    template_folder='templates'
)


@products_bp.route("/")
def index():
    """Homepage met overzicht van alle categorieën.

    Returns:
        Rendered HTML template
    """
    categories = db.session.execute(db.select(Category)).scalars().all()
    return render_template("products/index.html", categories=categories)


@products_bp.route("/category/<int:category_id>")
def category(category_id: int):
    """Categorie overzicht met alle producten.

    Args:
        category_id: ID van de categorie

    Returns:
        Rendered HTML template

    Raises:
        404: Als categorie niet bestaat
    """
    category_info = db.get_or_404(Category, category_id)
    products = db.session.execute(db.select(Product).filter_by(category_id=category_id)).scalars().all()

    return render_template(
        "products/category.html",
        category=category_info,
        products=products
    )


@products_bp.route("/product/<int:product_id>")
def product(product_id: int):
    """Product detail pagina.

    Args:
        product_id: ID van het product

    Returns:
        Rendered HTML template

    Raises:
        404: Als product niet bestaat
    """
    product_info = db.get_or_404(Product, product_id)
    return render_template("products/product.html", product=product_info)


@products_bp.route("/contact", methods=['GET', 'POST'])
def contact():
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
        return redirect(url_for('products.index'))

    return render_template("contact.html", form=form)
