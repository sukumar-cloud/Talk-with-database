"""
Populate MySQL with comprehensive sample data
Similar to Spider dataset for testing
"""

from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL connection
db_uri = os.getenv("DB_URI")
engine = create_engine(db_uri)

print("🚀 Starting MySQL Data Population...")
print("="*80)

with engine.connect() as conn:
    # Drop database and recreate
    print("\n📦 Recreating database...")
    conn.execute(text("DROP DATABASE IF EXISTS mydb"))
    conn.execute(text("CREATE DATABASE mydb"))
    conn.execute(text("USE mydb"))
    conn.commit()
    print("✅ Database recreated")

    # ============================================================================
    # 1. USERS TABLE
    # ============================================================================
    print("\n👥 Creating USERS table...")
    conn.execute(text("""
        CREATE TABLE users (
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            full_name VARCHAR(100),
            status ENUM('active', 'inactive', 'pending') DEFAULT 'active',
            age INT,
            country VARCHAR(50),
            joined_date DATETIME,
            is_premium BOOLEAN DEFAULT FALSE,
            credits INT DEFAULT 0
        )
    """))
    
    for i in range(1, 1001):
        conn.execute(text("""
            INSERT INTO users (username, email, full_name, status, age, country, joined_date, is_premium, credits)
            VALUES (:username, :email, :full_name, :status, :age, :country, :joined_date, :is_premium, :credits)
        """), {
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "full_name": f"User {i}",
            "status": random.choice(["active", "inactive", "pending"]),
            "age": random.randint(18, 65),
            "country": random.choice(["USA", "UK", "Canada", "Australia", "India"]),
            "joined_date": datetime.now() - timedelta(days=random.randint(1, 365)),
            "is_premium": random.choice([True, False]),
            "credits": random.randint(0, 1000)
        })
    conn.commit()
    print(f"✅ Inserted 1000 users")

    # ============================================================================
    # 2. CUSTOMERS TABLE
    # ============================================================================
    print("\n🛒 Creating CUSTOMERS table...")
    conn.execute(text("""
        CREATE TABLE customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            address VARCHAR(200),
            city VARCHAR(50),
            state VARCHAR(2),
            zip_code VARCHAR(10),
            country VARCHAR(50),
            customer_type ENUM('retail', 'wholesale', 'enterprise'),
            credit_limit DECIMAL(10,2),
            created_at DATETIME
        )
    """))
    
    for i in range(1, 1001):
        conn.execute(text("""
            INSERT INTO customers (name, email, phone, address, city, state, zip_code, country, customer_type, credit_limit, created_at)
            VALUES (:name, :email, :phone, :address, :city, :state, :zip_code, :country, :customer_type, :credit_limit, :created_at)
        """), {
            "name": f"Customer {i}",
            "email": f"customer{i}@company.com",
            "phone": f"+1-555-{random.randint(1000, 9999)}",
            "address": f"{random.randint(100, 999)} Main St",
            "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
            "state": random.choice(["NY", "CA", "IL", "TX", "AZ"]),
            "zip_code": f"{random.randint(10000, 99999)}",
            "country": "USA",
            "customer_type": random.choice(["retail", "wholesale", "enterprise"]),
            "credit_limit": round(random.uniform(1000, 50000), 2),
            "created_at": datetime.now() - timedelta(days=random.randint(1, 730))
        })
    conn.commit()
    print(f"✅ Inserted 1000 customers")

    # ============================================================================
    # 3. PRODUCTS TABLE
    # ============================================================================
    print("\n📦 Creating PRODUCTS table...")
    conn.execute(text("""
        CREATE TABLE products (
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            category VARCHAR(50),
            price DECIMAL(10,2),
            cost DECIMAL(10,2),
            stock_quantity INT,
            sku VARCHAR(50) UNIQUE,
            weight DECIMAL(10,2),
            is_active BOOLEAN DEFAULT TRUE,
            rating DECIMAL(3,1),
            reviews_count INT DEFAULT 0,
            created_at DATETIME
        )
    """))
    
    categories = ["Electronics", "Clothing", "Food", "Books", "Toys", "Sports", "Home", "Beauty"]
    for i in range(1, 1501):
        category = random.choice(categories)
        conn.execute(text("""
            INSERT INTO products (name, description, category, price, cost, stock_quantity, sku, weight, is_active, rating, reviews_count, created_at)
            VALUES (:name, :description, :category, :price, :cost, :stock_quantity, :sku, :weight, :is_active, :rating, :reviews_count, :created_at)
        """), {
            "name": f"{category} Product {i}",
            "description": f"High quality {category.lower()} item",
            "category": category,
            "price": round(random.uniform(10, 1000), 2),
            "cost": round(random.uniform(5, 500), 2),
            "stock_quantity": random.randint(0, 500),
            "sku": f"SKU-{i:05d}",
            "weight": round(random.uniform(0.1, 50), 2),
            "is_active": random.choice([True, False]),
            "rating": round(random.uniform(1, 5), 1),
            "reviews_count": random.randint(0, 1000),
            "created_at": datetime.now() - timedelta(days=random.randint(1, 365))
        })
    conn.commit()
    print(f"✅ Inserted 1500 products")

    # ============================================================================
    # 4. DEPARTMENTS TABLE
    # ============================================================================
    print("\n🏢 Creating DEPARTMENTS table...")
    conn.execute(text("""
        CREATE TABLE departments (
            department_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            budget DECIMAL(12,2)
        )
    """))
    
    departments = [
        ("Engineering", 1000000),
        ("Sales", 500000),
        ("Marketing", 300000),
        ("Human Resources", 200000),
        ("Finance", 400000),
        ("Operations", 600000),
        ("Customer Support", 250000),
        ("Research", 800000),
        ("Legal", 350000),
        ("IT", 700000)
    ]
    
    for dept in departments:
        conn.execute(text("INSERT INTO departments (name, budget) VALUES (:name, :budget)"), 
                    {"name": dept[0], "budget": dept[1]})
    conn.commit()
    print(f"✅ Inserted 10 departments")

    # ============================================================================
    # 5. EMPLOYEES TABLE
    # ============================================================================
    print("\n👔 Creating EMPLOYEES table...")
    conn.execute(text("""
        CREATE TABLE employees (
            employee_id INT PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE,
            phone VARCHAR(20),
            position VARCHAR(50),
            department_id INT,
            salary DECIMAL(10,2),
            hire_date DATE,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (department_id) REFERENCES departments(department_id)
        )
    """))
    
    positions = ["Manager", "Developer", "Designer", "Analyst", "Sales", "HR", "Marketing"]
    for i in range(1, 501):
        conn.execute(text("""
            INSERT INTO employees (first_name, last_name, email, phone, position, department_id, salary, hire_date, is_active)
            VALUES (:first_name, :last_name, :email, :phone, :position, :department_id, :salary, :hire_date, :is_active)
        """), {
            "first_name": f"FirstName{i}",
            "last_name": f"LastName{i}",
            "email": f"employee{i}@company.com",
            "phone": f"+1-555-{random.randint(1000, 9999)}",
            "position": random.choice(positions),
            "department_id": random.randint(1, 10),
            "salary": random.randint(40000, 150000),
            "hire_date": (datetime.now() - timedelta(days=random.randint(30, 1825))).date(),
            "is_active": random.choice([True, False])
        })
    conn.commit()
    print(f"✅ Inserted 500 employees")

    # ============================================================================
    # 6. ORDERS TABLE
    # ============================================================================
    print("\n📋 Creating ORDERS table...")
    conn.execute(text("""
        CREATE TABLE orders (
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT,
            order_date DATETIME,
            status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled'),
            total_amount DECIMAL(10,2),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """))
    
    for i in range(1, 2001):
        conn.execute(text("""
            INSERT INTO orders (customer_id, order_date, status, total_amount)
            VALUES (:customer_id, :order_date, :status, :total_amount)
        """), {
            "customer_id": random.randint(1, 1000),
            "order_date": datetime.now() - timedelta(days=random.randint(1, 180)),
            "status": random.choice(["pending", "processing", "shipped", "delivered", "cancelled"]),
            "total_amount": round(random.uniform(50, 5000), 2)
        })
    conn.commit()
    print(f"✅ Inserted 2000 orders")

    print("\n" + "="*80)
    print("📊 MYSQL DATA POPULATION COMPLETE!")
    print("="*80)
    print("\n✅ Database: mydb")
    print("✅ Tables created with data:")
    print("   - users: 1000 rows")
    print("   - customers: 1000 rows")
    print("   - products: 1500 rows")
    print("   - departments: 10 rows")
    print("   - employees: 500 rows")
    print("   - orders: 2000 rows")
    print(f"\n📈 Total Rows: 6010")
    print("\n🎉 You can now test SQL queries!")
    print("="*80)
