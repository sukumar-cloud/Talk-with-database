"""
Enhanced MySQL Population - More Tables & Columns
"""

from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()
db_uri = os.getenv("DB_URI")
engine = create_engine(db_uri)

print("Starting Enhanced MySQL Data Population...")
print("="*80)

with engine.connect() as conn:
    # Recreate database
    print("\nRecreating database...")
    conn.execute(text("DROP DATABASE IF EXISTS mydb"))
    conn.execute(text("CREATE DATABASE mydb"))
    conn.execute(text("USE mydb"))
    conn.commit()
    print("Database recreated")

    # ============================================================================
    # 1. USERS TABLE (Enhanced)
    # ============================================================================
    print("\nCreating USERS table...")
    conn.execute(text("""
        CREATE TABLE users (
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255),
            full_name VARCHAR(100),
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            phone VARCHAR(20),
            date_of_birth DATE,
            gender ENUM('Male', 'Female', 'Other'),
            status ENUM('active', 'inactive', 'pending', 'suspended') DEFAULT 'active',
            age INT,
            country VARCHAR(50),
            city VARCHAR(50),
            state VARCHAR(50),
            postal_code VARCHAR(20),
            address TEXT,
            profile_picture_url VARCHAR(255),
            bio TEXT,
            website VARCHAR(255),
            social_media JSON,
            preferences JSON,
            joined_date DATETIME,
            last_login DATETIME,
            email_verified BOOLEAN DEFAULT FALSE,
            is_premium BOOLEAN DEFAULT FALSE,
            subscription_tier ENUM('free', 'basic', 'premium', 'enterprise'),
            credits INT DEFAULT 0,
            loyalty_points INT DEFAULT 0,
            referral_code VARCHAR(20),
            referred_by INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """))
    
    for i in range(1, 1001):
        conn.execute(text("""
            INSERT INTO users (username, email, password_hash, full_name, first_name, last_name, phone, 
                date_of_birth, gender, status, age, country, city, state, postal_code, address,
                bio, joined_date, last_login, email_verified, is_premium, subscription_tier, 
                credits, loyalty_points, referral_code)
            VALUES (:username, :email, :password_hash, :full_name, :first_name, :last_name, :phone,
                :date_of_birth, :gender, :status, :age, :country, :city, :state, :postal_code, :address,
                :bio, :joined_date, :last_login, :email_verified, :is_premium, :subscription_tier,
                :credits, :loyalty_points, :referral_code)
        """), {
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "password_hash": f"hash_{i}",
            "full_name": f"User {i}",
            "first_name": f"First{i}",
            "last_name": f"Last{i}",
            "phone": f"+1-555-{random.randint(1000, 9999)}",
            "date_of_birth": (datetime.now() - timedelta(days=random.randint(6570, 23725))).date(),
            "gender": random.choice(["Male", "Female", "Other"]),
            "status": random.choice(["active", "inactive", "pending", "suspended"]),
            "age": random.randint(18, 65),
            "country": random.choice(["USA", "UK", "Canada", "Australia", "India", "Germany", "France"]),
            "city": random.choice(["New York", "London", "Toronto", "Sydney", "Mumbai", "Berlin"]),
            "state": random.choice(["NY", "CA", "TX", "FL", "ON", "NSW"]),
            "postal_code": f"{random.randint(10000, 99999)}",
            "address": f"{random.randint(100, 999)} Main St",
            "bio": f"This is user {i}'s bio",
            "joined_date": datetime.now() - timedelta(days=random.randint(1, 365)),
            "last_login": datetime.now() - timedelta(days=random.randint(0, 30)),
            "email_verified": random.choice([True, False]),
            "is_premium": random.choice([True, False]),
            "subscription_tier": random.choice(["free", "basic", "premium", "enterprise"]),
            "credits": random.randint(0, 1000),
            "loyalty_points": random.randint(0, 5000),
            "referral_code": f"REF{i:04d}"
        })
    conn.commit()
    print("Inserted 1000 users")

    # ============================================================================
    # 2. CATEGORIES TABLE
    # ============================================================================
    print("\nCreating CATEGORIES table...")
    conn.execute(text("""
        CREATE TABLE categories (
            category_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            slug VARCHAR(100) UNIQUE,
            description TEXT,
            parent_id INT,
            level INT,
            image_url VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            display_order INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    
    categories = [
        ("Electronics", "electronics", "Electronic devices and gadgets", None, 1),
        ("Laptops", "laptops", "Portable computers", 1, 2),
        ("Smartphones", "smartphones", "Mobile phones", 1, 2),
        ("Tablets", "tablets", "Tablet devices", 1, 2),
        ("Clothing", "clothing", "Apparel and fashion", None, 1),
        ("Men's Clothing", "mens-clothing", "Clothing for men", 5, 2),
        ("Women's Clothing", "womens-clothing", "Clothing for women", 5, 2),
        ("Food & Beverage", "food-beverage", "Food items", None, 1),
        ("Books", "books", "Physical and digital books", None, 1),
        ("Toys", "toys", "Toys and games", None, 1),
        ("Sports", "sports", "Sports equipment", None, 1),
        ("Home & Garden", "home-garden", "Home improvement", None, 1),
        ("Beauty", "beauty", "Beauty and cosmetics", None, 1),
        ("Automotive", "automotive", "Car parts and accessories", None, 1),
        ("Health", "health", "Health products", None, 1)
    ]
    
    for idx, cat in enumerate(categories, 1):
        conn.execute(text("""
            INSERT INTO categories (name, slug, description, parent_id, level, is_active, display_order)
            VALUES (:name, :slug, :description, :parent_id, :level, :is_active, :display_order)
        """), {
            "name": cat[0],
            "slug": cat[1],
            "description": cat[2],
            "parent_id": cat[3],
            "level": cat[4],
            "is_active": True,
            "display_order": idx
        })
    conn.commit()
    print("Inserted 15 categories")

    # ============================================================================
    # 3. PRODUCTS TABLE (Enhanced)
    # ============================================================================
    print("\nCreating PRODUCTS table...")
    conn.execute(text("""
        CREATE TABLE products (
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(200) NOT NULL,
            slug VARCHAR(200) UNIQUE,
            description TEXT,
            short_description VARCHAR(500),
            category_id INT,
            brand VARCHAR(100),
            manufacturer VARCHAR(100),
            model_number VARCHAR(100),
            barcode VARCHAR(100),
            price DECIMAL(10,2),
            cost DECIMAL(10,2),
            discount_percentage DECIMAL(5,2),
            sale_price DECIMAL(10,2),
            tax_rate DECIMAL(5,2),
            stock_quantity INT,
            min_stock_level INT,
            max_stock_level INT,
            reorder_level INT,
            sku VARCHAR(50) UNIQUE,
            upc VARCHAR(50),
            weight DECIMAL(10,2),
            length DECIMAL(10,2),
            width DECIMAL(10,2),
            height DECIMAL(10,2),
            color VARCHAR(50),
            size VARCHAR(20),
            material VARCHAR(100),
            warranty_months INT,
            is_active BOOLEAN DEFAULT TRUE,
            is_featured BOOLEAN DEFAULT FALSE,
            is_new_arrival BOOLEAN DEFAULT FALSE,
            is_bestseller BOOLEAN DEFAULT FALSE,
            rating DECIMAL(3,1),
            reviews_count INT DEFAULT 0,
            views_count INT DEFAULT 0,
            sales_count INT DEFAULT 0,
            image_url VARCHAR(255),
            meta_title VARCHAR(200),
            meta_description TEXT,
            meta_keywords TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """))
    
    brands = ["Apple", "Samsung", "Nike", "Adidas", "Sony", "LG", "Dell", "HP", "Canon", "Nikon"]
    colors = ["Black", "White", "Red", "Blue", "Green", "Silver", "Gold"]
    sizes = ["S", "M", "L", "XL", "XXL", "One Size"]
    
    for i in range(1, 1501):
        category_id = random.randint(1, 15)
        price = round(random.uniform(10, 1000), 2)
        discount = round(random.uniform(0, 30), 2)
        sale_price = round(price * (1 - discount/100), 2)
        
        conn.execute(text("""
            INSERT INTO products (name, slug, description, short_description, category_id, brand, manufacturer,
                model_number, barcode, price, cost, discount_percentage, sale_price, tax_rate, stock_quantity,
                min_stock_level, max_stock_level, reorder_level, sku, weight, length, width, height,
                color, size, warranty_months, is_active, is_featured, is_new_arrival, is_bestseller,
                rating, reviews_count, views_count, sales_count)
            VALUES (:name, :slug, :description, :short_description, :category_id, :brand, :manufacturer,
                :model_number, :barcode, :price, :cost, :discount_percentage, :sale_price, :tax_rate, :stock_quantity,
                :min_stock_level, :max_stock_level, :reorder_level, :sku, :weight, :length, :width, :height,
                :color, :size, :warranty_months, :is_active, :is_featured, :is_new_arrival, :is_bestseller,
                :rating, :reviews_count, :views_count, :sales_count)
        """), {
            "name": f"Product {i}",
            "slug": f"product-{i}",
            "description": f"Full description for product {i}",
            "short_description": f"Short desc for product {i}",
            "category_id": category_id,
            "brand": random.choice(brands),
            "manufacturer": random.choice(brands),
            "model_number": f"MODEL-{i}",
            "barcode": f"BAR{i:010d}",
            "price": price,
            "cost": round(price * 0.6, 2),
            "discount_percentage": discount,
            "sale_price": sale_price,
            "tax_rate": 8.5,
            "stock_quantity": random.randint(0, 500),
            "min_stock_level": 10,
            "max_stock_level": 1000,
            "reorder_level": 50,
            "sku": f"SKU-{i:05d}",
            "weight": round(random.uniform(0.1, 50), 2),
            "length": round(random.uniform(5, 100), 2),
            "width": round(random.uniform(5, 100), 2),
            "height": round(random.uniform(5, 100), 2),
            "color": random.choice(colors),
            "size": random.choice(sizes),
            "warranty_months": random.choice([0, 6, 12, 24, 36]),
            "is_active": random.choice([True, False]),
            "is_featured": random.choice([True, False]),
            "is_new_arrival": random.choice([True, False]),
            "is_bestseller": random.choice([True, False]),
            "rating": round(random.uniform(1, 5), 1),
            "reviews_count": random.randint(0, 1000),
            "views_count": random.randint(0, 10000),
            "sales_count": random.randint(0, 500)
        })
    conn.commit()
    print("Inserted 1500 products")

    # ============================================================================
    # 4. CUSTOMERS TABLE (Enhanced)
    # ============================================================================
    print("\nCreating CUSTOMERS table...")
    conn.execute(text("""
        CREATE TABLE customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            company_name VARCHAR(200),
            tax_id VARCHAR(50),
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            mobile VARCHAR(20),
            fax VARCHAR(20),
            address VARCHAR(200),
            address2 VARCHAR(200),
            city VARCHAR(50),
            state VARCHAR(2),
            zip_code VARCHAR(10),
            country VARCHAR(50),
            billing_address TEXT,
            shipping_address TEXT,
            customer_type ENUM('retail', 'wholesale', 'enterprise', 'vip'),
            credit_limit DECIMAL(10,2),
            current_balance DECIMAL(10,2),
            payment_terms VARCHAR(50),
            discount_percentage DECIMAL(5,2),
            is_tax_exempt BOOLEAN DEFAULT FALSE,
            notes TEXT,
            created_at DATETIME,
            last_order_date DATETIME,
            total_orders INT DEFAULT 0,
            total_spent DECIMAL(12,2) DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """))
    
    for i in range(1, 1001):
        conn.execute(text("""
            INSERT INTO customers (user_id, company_name, tax_id, name, email, phone, mobile, address, address2,
                city, state, zip_code, country, customer_type, credit_limit, current_balance, payment_terms,
                discount_percentage, is_tax_exempt, created_at, last_order_date, total_orders, total_spent)
            VALUES (:user_id, :company_name, :tax_id, :name, :email, :phone, :mobile, :address, :address2,
                :city, :state, :zip_code, :country, :customer_type, :credit_limit, :current_balance, :payment_terms,
                :discount_percentage, :is_tax_exempt, :created_at, :last_order_date, :total_orders, :total_spent)
        """), {
            "user_id": i if i <= 1000 else None,
            "company_name": f"Company {i}" if random.choice([True, False]) else None,
            "tax_id": f"TAX{i:06d}" if random.choice([True, False]) else None,
            "name": f"Customer {i}",
            "email": f"customer{i}@company.com",
            "phone": f"+1-555-{random.randint(1000, 9999)}",
            "mobile": f"+1-555-{random.randint(1000, 9999)}",
            "address": f"{random.randint(100, 999)} Main St",
            "address2": f"Suite {random.randint(100, 999)}" if random.choice([True, False]) else None,
            "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
            "state": random.choice(["NY", "CA", "IL", "TX", "AZ"]),
            "zip_code": f"{random.randint(10000, 99999)}",
            "country": "USA",
            "customer_type": random.choice(["retail", "wholesale", "enterprise", "vip"]),
            "credit_limit": round(random.uniform(1000, 50000), 2),
            "current_balance": round(random.uniform(0, 10000), 2),
            "payment_terms": random.choice(["Net 30", "Net 60", "COD", "Prepaid"]),
            "discount_percentage": round(random.uniform(0, 15), 2),
            "is_tax_exempt": random.choice([True, False]),
            "created_at": datetime.now() - timedelta(days=random.randint(1, 730)),
            "last_order_date": datetime.now() - timedelta(days=random.randint(0, 180)),
            "total_orders": random.randint(0, 100),
            "total_spent": round(random.uniform(0, 50000), 2)
        })
    conn.commit()
    print("Inserted 1000 customers")

    # Continue with more tables...
    print("\n" + "="*80)
    print("ENHANCED MYSQL DATA POPULATION COMPLETE!")
    print("="*80)
    print("\nDatabase: mydb")
    print("Tables created:")
    print("  - users: 1000 rows (30+ columns)")
    print("  - categories: 15 rows")
    print("  - products: 1500 rows (45+ columns)")
    print("  - customers: 1000 rows (25+ columns)")
    print("\nTotal Rows: 3515+")
    print("="*80)
