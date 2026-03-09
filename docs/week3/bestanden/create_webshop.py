"""
Script om webshop.sqlite database te maken met realistische data.
"""
import sqlite3
import random

# Database connectie
conn = sqlite3.connect('webshop.sqlite')
cursor = conn.cursor()

# Maak tabellen
cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    description TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
''')

# Categories data
categories = [
    (1, 'Electronics', 'Electronic devices and accessories'),
    (2, 'Books', 'Books, e-books, and audiobooks'),
    (3, 'Clothing', 'Fashion and apparel'),
    (4, 'Home & Garden', 'Home improvement and garden supplies'),
    (5, 'Sports', 'Sports equipment and outdoor gear'),
    (6, 'Toys & Games', 'Toys, games, and puzzles'),
    (7, 'Food & Drinks', 'Groceries and beverages'),
    (8, 'Beauty', 'Cosmetics and personal care'),
    (9, 'Office Supplies', 'Stationery and office equipment'),
    (10, 'Music & Movies', 'CDs, DVDs, and streaming devices')
]

cursor.executemany('INSERT INTO categories (id, name, description) VALUES (?, ?, ?)', categories)

# Products data per category
products = []
product_id = 1

# Electronics (15 products)
electronics = [
    ('Laptop HP EliteBook', 899.99, 12, 'Professional laptop with 16GB RAM'),
    ('Wireless Mouse Logitech', 24.99, 45, 'Ergonomic wireless mouse'),
    ('USB-C Hub', 39.99, 28, '7-in-1 USB-C adapter'),
    ('Bluetooth Headphones Sony', 149.99, 18, 'Noise-cancelling headphones'),
    ('Smartphone Samsung Galaxy', 699.99, 8, 'Latest Android smartphone'),
    ('Tablet iPad Air', 599.99, 15, 'Apple tablet with 256GB storage'),
    ('Webcam Logitech HD', 79.99, 32, '1080p HD webcam'),
    ('Keyboard Mechanical', 119.99, 22, 'RGB mechanical gaming keyboard'),
    ('Monitor Dell 27 inch', 349.99, 10, '4K UHD monitor'),
    ('External SSD 1TB', 89.99, 40, 'Portable solid state drive'),
    ('Smartwatch Fitbit', 199.99, 25, 'Fitness tracker and smartwatch'),
    ('Power Bank 20000mAh', 34.99, 55, 'Fast charging power bank'),
    ('HDMI Cable 2m', 12.99, 60, 'High-speed HDMI 2.1 cable'),
    ('Wireless Charger', 29.99, 38, 'Qi wireless charging pad'),
    ('Gaming Controller Xbox', 59.99, 20, 'Wireless Xbox controller')
]
for name, price, stock, desc in electronics:
    products.append((product_id, name, price, stock, desc, 1))
    product_id += 1

# Books (20 products)
books = [
    ('Python Crash Course', 29.99, 35, 'Beginner-friendly Python programming'),
    ('Clean Code', 34.99, 28, 'A handbook of agile software craftsmanship'),
    ('The Pragmatic Programmer', 39.99, 22, 'Your journey to mastery'),
    ('Design Patterns', 44.99, 18, 'Elements of reusable object-oriented software'),
    ('Harry Potter Box Set', 79.99, 12, 'Complete series'),
    ('The Hobbit', 14.99, 40, 'J.R.R. Tolkien classic'),
    ('1984', 12.99, 45, 'George Orwell dystopian novel'),
    ('To Kill a Mockingbird', 13.99, 38, 'Harper Lee classic'),
    ('Pride and Prejudice', 11.99, 42, 'Jane Austen romance'),
    ('The Great Gatsby', 10.99, 50, 'F. Scott Fitzgerald'),
    ('Algorithms Unlocked', 32.99, 25, 'Understanding algorithms'),
    ('SQL Performance Explained', 29.99, 20, 'Database optimization guide'),
    ('JavaScript: The Good Parts', 24.99, 30, 'Douglas Crockford'),
    ('Eloquent JavaScript', 27.99, 28, 'Modern introduction to programming'),
    ('The Martian', 15.99, 35, 'Andy Weir sci-fi thriller'),
    ('Educated', 16.99, 32, 'Tara Westover memoir'),
    ('Atomic Habits', 18.99, 40, 'James Clear self-help'),
    ('Sapiens', 19.99, 30, 'Yuval Noah Harari history'),
    ('Thinking, Fast and Slow', 17.99, 25, 'Daniel Kahneman psychology'),
    ('The Art of War', 9.99, 48, 'Sun Tzu strategy classic')
]
for name, price, stock, desc in books:
    products.append((product_id, name, price, stock, desc, 2))
    product_id += 1

# Clothing (15 products)
clothing = [
    ('T-Shirt Cotton Blue', 19.99, 60, 'Comfortable cotton t-shirt'),
    ('Jeans Slim Fit', 49.99, 35, 'Classic blue jeans'),
    ('Hoodie Grey', 39.99, 28, 'Warm fleece hoodie'),
    ('Sneakers Nike', 89.99, 22, 'Running shoes'),
    ('Winter Jacket', 129.99, 15, 'Waterproof winter coat'),
    ('Dress Black Elegant', 59.99, 18, 'Evening dress'),
    ('Polo Shirt White', 24.99, 40, 'Classic polo shirt'),
    ('Sweatpants', 29.99, 45, 'Comfortable joggers'),
    ('Leather Belt', 19.99, 50, 'Genuine leather belt'),
    ('Socks Pack (5 pairs)', 12.99, 80, 'Cotton socks'),
    ('Baseball Cap', 14.99, 55, 'Adjustable cap'),
    ('Scarf Wool', 24.99, 30, 'Winter scarf'),
    ('Gloves Leather', 34.99, 25, 'Touchscreen compatible'),
    ('Backpack', 44.99, 20, 'Laptop backpack'),
    ('Sunglasses Polarized', 39.99, 32, 'UV protection')
]
for name, price, stock, desc in clothing:
    products.append((product_id, name, price, stock, desc, 3))
    product_id += 1

# Home & Garden (12 products)
home_garden = [
    ('Coffee Maker', 79.99, 18, 'Programmable drip coffee maker'),
    ('Vacuum Cleaner', 149.99, 12, 'Bagless upright vacuum'),
    ('LED Desk Lamp', 29.99, 40, 'Adjustable brightness lamp'),
    ('Plant Pot Set (3)', 19.99, 35, 'Ceramic plant pots'),
    ('Garden Hose 15m', 24.99, 28, 'Flexible garden hose'),
    ('Tool Set 50-piece', 59.99, 15, 'Complete home tool kit'),
    ('Throw Pillows (2)', 24.99, 45, 'Decorative cushions'),
    ('Wall Clock', 34.99, 30, 'Modern minimalist clock'),
    ('Picture Frames Set', 22.99, 38, 'Wooden photo frames'),
    ('Garbage Bins (3)', 29.99, 25, 'Recycling bin set'),
    ('Kitchen Knife Set', 89.99, 20, 'Professional chef knives'),
    ('Bath Towels (4)', 39.99, 32, 'Soft cotton towels')
]
for name, price, stock, desc in home_garden:
    products.append((product_id, name, price, stock, desc, 4))
    product_id += 1

# Sports (12 products)
sports = [
    ('Yoga Mat', 24.99, 40, 'Non-slip exercise mat'),
    ('Dumbbells 10kg Set', 49.99, 20, 'Adjustable dumbbells'),
    ('Resistance Bands', 19.99, 45, 'Set of 5 resistance bands'),
    ('Tennis Racket', 89.99, 15, 'Professional tennis racket'),
    ('Football (Soccer Ball)', 29.99, 35, 'Official size 5'),
    ('Basketball', 34.99, 28, 'Indoor/outdoor ball'),
    ('Running Shoes Adidas', 99.99, 22, 'Marathon running shoes'),
    ('Bicycle Helmet', 44.99, 25, 'Safety certified helmet'),
    ('Water Bottle 1L', 14.99, 60, 'Insulated sports bottle'),
    ('Gym Bag', 39.99, 30, 'Durable sports bag'),
    ('Jump Rope', 12.99, 50, 'Speed jump rope'),
    ('Cycling Gloves', 19.99, 35, 'Padded cycling gloves')
]
for name, price, stock, desc in sports:
    products.append((product_id, name, price, stock, desc, 5))
    product_id += 1

# Toys & Games (10 products)
toys = [
    ('LEGO City Set', 49.99, 25, 'Building blocks set'),
    ('Board Game Settlers of Catan', 39.99, 18, 'Strategy board game'),
    ('Puzzle 1000 pieces', 19.99, 30, 'Landscape jigsaw puzzle'),
    ('Action Figure Marvel', 24.99, 35, 'Collectible superhero figure'),
    ('Card Game Uno', 9.99, 60, 'Classic card game'),
    ('Chess Set Wooden', 34.99, 20, 'Handcrafted chess set'),
    ('RC Car', 59.99, 15, 'Remote control race car'),
    ('Teddy Bear', 19.99, 40, 'Soft plush toy'),
    ('Play-Doh Set', 14.99, 45, 'Modeling clay set'),
    ('Rubiks Cube', 12.99, 50, 'Classic 3x3 cube')
]
for name, price, stock, desc in toys:
    products.append((product_id, name, price, stock, desc, 6))
    product_id += 1

# Food & Drinks (8 products)
food = [
    ('Coffee Beans 1kg', 24.99, 40, 'Arabica coffee beans'),
    ('Green Tea Box', 12.99, 50, 'Organic green tea'),
    ('Chocolate Bar Dark 70%', 3.99, 100, 'Premium dark chocolate'),
    ('Olive Oil Extra Virgin 500ml', 14.99, 35, 'Italian olive oil'),
    ('Pasta Variety Pack', 9.99, 45, 'Assorted pasta shapes'),
    ('Honey Natural 500g', 11.99, 30, 'Raw organic honey'),
    ('Energy Drink Pack (12)', 19.99, 28, 'Sugar-free energy drinks'),
    ('Protein Powder 1kg', 39.99, 25, 'Whey protein vanilla')
]
for name, price, stock, desc in food:
    products.append((product_id, name, price, stock, desc, 7))
    product_id += 1

# Beauty (8 products)
beauty = [
    ('Shampoo & Conditioner Set', 24.99, 35, 'Natural hair care set'),
    ('Face Cream Anti-Aging', 34.99, 25, 'Moisturizing face cream'),
    ('Lipstick Set (5 colors)', 29.99, 30, 'Matte finish lipsticks'),
    ('Perfume Eau de Parfum 50ml', 59.99, 18, 'Floral fragrance'),
    ('Nail Polish Kit', 19.99, 40, 'Gel nail polish set'),
    ('Electric Toothbrush', 79.99, 20, 'Sonic toothbrush'),
    ('Hair Dryer', 49.99, 22, 'Professional hair dryer'),
    ('Makeup Brush Set', 39.99, 28, '10-piece brush set')
]
for name, price, stock, desc in beauty:
    products.append((product_id, name, price, stock, desc, 8))
    product_id += 1

# Office Supplies (10 products)
office = [
    ('Notebook A4 (5 pack)', 12.99, 60, 'Ruled notebooks'),
    ('Pen Set Ballpoint (20)', 9.99, 70, 'Blue and black pens'),
    ('Desk Organizer', 19.99, 35, 'Bamboo desk organizer'),
    ('Printer Paper 500 sheets', 8.99, 50, 'A4 white paper'),
    ('Stapler + Staples', 14.99, 45, 'Heavy-duty stapler'),
    ('Whiteboard 90x60cm', 39.99, 15, 'Magnetic whiteboard'),
    ('Filing Cabinet', 89.99, 8, '3-drawer metal cabinet'),
    ('Calculator Scientific', 24.99, 30, 'Graphing calculator'),
    ('Highlighter Set (6)', 7.99, 55, 'Assorted colors'),
    ('Sticky Notes Pack', 11.99, 65, 'Colorful sticky notes')
]
for name, price, stock, desc in office:
    products.append((product_id, name, price, stock, desc, 9))
    product_id += 1

# Music & Movies (10 products)
music_movies = [
    ('Spotify Gift Card €50', 50.00, 100, 'Digital gift card'),
    ('Netflix Gift Card €25', 25.00, 100, 'Streaming gift card'),
    ('Vinyl Record Player', 129.99, 12, 'Retro turntable'),
    ('The Beatles Abbey Road Vinyl', 29.99, 20, 'Classic album vinyl'),
    ('4K Blu-ray Player', 199.99, 10, 'Ultra HD player'),
    ('Movie Collection Marvel Phase 1', 79.99, 15, 'Blu-ray box set'),
    ('Guitar Strings Set', 12.99, 40, 'Steel acoustic strings'),
    ('Microphone USB', 69.99, 18, 'Condenser microphone'),
    ('Portable Bluetooth Speaker', 49.99, 35, 'Waterproof speaker'),
    ('DJ Headphones', 89.99, 16, 'Professional DJ headphones')
]
for name, price, stock, desc in music_movies:
    products.append((product_id, name, price, stock, desc, 10))
    product_id += 1

# Insert all products
cursor.executemany('''
    INSERT INTO products (id, name, price, stock, description, category_id)
    VALUES (?, ?, ?, ?, ?, ?)
''', products)

# Commit en sluit
conn.commit()
conn.close()

print(f"Database aangemaakt met {len(categories)} categorieën en {len(products)} producten!")
