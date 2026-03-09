"""
Webshop Flask Applicatie met Formulieren (Week 5).

Deze uitgebreide versie voegt formulieren toe voor het toevoegen
en bewerken van producten. Dit bouwt voort op Week 4 door CRUD
operaties toe te voegen met Flask-WTF.
"""
from flask import Flask, render_template, abort, redirect, url_for, flash
from database import WebshopDatabase
from forms import AddProductForm, EditProductForm, ContactForm

app = Flask(__name__)

# Secret key voor CSRF-beveiliging (vereist voor Flask-WTF)
app.config['SECRET_KEY'] = 'webshop-secret-key-2025'

db = WebshopDatabase()


@app.route("/")
def index() -> str:
    """Homepage met overzicht van alle categorieën.

    Returns:
        Rendered HTML template
    """
    categories = db.get_category_stats()
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
    category_info = db.get_category_by_id(category_id)

    if not category_info:
        abort(404)

    products = db.get_products_by_category(category_id)

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
    product_info = db.get_product_by_id(product_id)

    if not product_info:
        abort(404)

    return render_template("product.html", product=product_info)


@app.route("/admin/products")
def admin_products() -> str:
    """Admin overzicht van alle producten.

    Returns:
        Rendered HTML template met product lijst
    """
    products = db.get_all_products(limit=100)
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

    # Populate categorie choices
    form.category_id.choices = db.get_category_choices()

    if form.validate_on_submit():
        # Voeg product toe aan database
        new_product_id = db.add_product(
            name=form.name.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data,
            description=form.description.data
        )

        flash(f'Product "{form.name.data}" succesvol toegevoegd!', 'success')
        return redirect(url_for('product', product_id=new_product_id))

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
    product_info = db.get_product_by_id(product_id)

    if not product_info:
        abort(404)

    form = EditProductForm()

    # Populate categorie choices
    form.category_id.choices = db.get_category_choices()

    if form.validate_on_submit():
        # Update product in database
        success = db.update_product(
            product_id=product_id,
            name=form.name.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data,
            description=form.description.data
        )

        if success:
            flash(f'Product "{form.name.data}" succesvol gewijzigd!', 'success')
            return redirect(url_for('product', product_id=product_id))
        else:
            flash('Er ging iets mis bij het wijzigen van het product.', 'danger')

    # Pre-fill form met huidige product data (bij GET request)
    elif not form.is_submitted():
        form.name.data = product_info['name']
        form.price.data = product_info['price']
        form.stock.data = product_info['stock']
        form.description.data = product_info['description']
        form.category_id.data = product_info['category_id']

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
    product_info = db.get_product_by_id(product_id)

    if not product_info:
        abort(404)

    success = db.delete_product(product_id)

    if success:
        flash(f'Product "{product_info["name"]}" succesvol verwijderd.', 'success')
    else:
        flash('Er ging iets mis bij het verwijderen van het product.', 'danger')

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
        # In een echte applicatie zou je hier een email versturen
        # Voor nu tonen we alleen een bevestiging
        flash(
            f'Bedankt voor je bericht, {form.name.data}! '
            f'We nemen zo snel mogelijk contact met je op.',
            'success'
        )

        # Redirect naar homepage na succesvol verzenden
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
    app.run(debug=True)
