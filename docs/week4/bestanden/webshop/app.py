"""
Webshop Flask Applicatie.

Deze applicatie demonstreert het gebruik van Flask met een SQLite database.
Het bouwt voort op Week 2 (OOP) en Week 3 (SQL) door de webshop.sqlite
database te gebruiken in een Flask webapplicatie.
"""
from flask import Flask, render_template, abort
from database import WebshopDatabase

app = Flask(__name__)
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
