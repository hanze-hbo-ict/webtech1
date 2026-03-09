"""
Hoofdbestand voor het testen van de webshop-klassen
"""

from product import Product, FysiekProduct


# Test basis Product-klasse
print("=== Test basis Product ===")
basis_product = Product("Laptop", 799.99, 5)
print(basis_product)

basis_product.verkoop(2)
print(basis_product)

print("\n" + "="*50 + "\n")

# Test FysiekProduct-klasse
print("=== Test FysiekProduct ===")
java_boek = FysiekProduct("Java voor beginners", 34.95, 12, 0.8)
print(java_boek)
print(f"Verzendkosten: €{java_boek.bereken_verzendkosten():.2f}")

laptop = FysiekProduct("MacBook Pro", 1499.99, 3, 2.1)
print(f"Verzendkosten: €{laptop.bereken_verzendkosten():.2f}")

print("\n" + "="*50 + "\n")

# Hier kun je tests toevoegen voor DigitaalProduct
# Hier kun je tests toevoegen voor Boek
# Hier kun je eventueel ook nog (extra) tests toevoegen voor Customer en Cart
