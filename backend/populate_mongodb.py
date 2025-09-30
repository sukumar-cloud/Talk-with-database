"""
Populate MongoDB with comprehensive sample data
Similar to Spider dataset for testing
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client['mydb']

print("🚀 Starting MongoDB Data Population...")
print("="*80)

# Drop existing collections for fresh start
print("\n📦 Dropping existing collections...")
for collection in ['users', 'customers', 'orders', 'products', 'employees', 'departments', 'sales']:
    db[collection].drop()
print("✅ Collections dropped")

# ============================================================================
# 1. USERS COLLECTION
# ============================================================================
print("\n👥 Populating USERS collection...")
users_data = []
for i in range(1, 1001):
    users_data.append({
        "user_id": i,
        "username": f"user{i}",
        "email": f"user{i}@example.com",
        "full_name": f"User {i}",
        "status": random.choice(["active", "inactive", "pending"]),
        "age": random.randint(18, 65),
        "country": random.choice(["USA", "UK", "Canada", "Australia", "India"]),
        "joined_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
        "is_premium": random.choice([True, False]),
        "credits": random.randint(0, 1000)
    })
db.users.insert_many(users_data)
print(f"✅ Inserted {len(users_data)} users")

# ============================================================================
# 2. CUSTOMERS COLLECTION
# ============================================================================
print("\n🛒 Populating CUSTOMERS collection...")
customers_data = []
for i in range(1, 1001):
    customers_data.append({
        "customer_id": i,
        "name": f"Customer {i}",
        "email": f"customer{i}@company.com",
        "phone": f"+1-555-{random.randint(1000, 9999)}",
        "address": f"{random.randint(100, 999)} Main St",
        "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
        "state": random.choice(["NY", "CA", "IL", "TX", "AZ"]),
        "zip_code": f"{random.randint(10000, 99999)}",
        "country": "USA",
        "customer_type": random.choice(["retail", "wholesale", "enterprise"]),
        "credit_limit": random.randint(1000, 50000),
        "created_at": (datetime.now() - timedelta(days=random.randint(1, 730))).isoformat()
    })
db.customers.insert_many(customers_data)
print(f"✅ Inserted {len(customers_data)} customers")

# ============================================================================
# 3. PRODUCTS COLLECTION
# ============================================================================
print("\n📦 Populating PRODUCTS collection...")
categories = ["Electronics", "Clothing", "Food", "Books", "Toys", "Sports", "Home", "Beauty"]
products_data = []
for i in range(1, 1501):
    category = random.choice(categories)
    products_data.append({
        "product_id": i,
        "name": f"{category} Product {i}",
        "description": f"High quality {category.lower()} item",
        "category": category,
        "price": round(random.uniform(10, 1000), 2),
        "cost": round(random.uniform(5, 500), 2),
        "stock_quantity": random.randint(0, 500),
        "sku": f"SKU-{i:05d}",
        "weight": round(random.uniform(0.1, 50), 2),
        "dimensions": {
            "length": round(random.uniform(5, 100), 2),
            "width": round(random.uniform(5, 100), 2),
            "height": round(random.uniform(5, 100), 2)
        },
        "is_active": random.choice([True, False]),
        "rating": round(random.uniform(1, 5), 1),
        "reviews_count": random.randint(0, 1000),
        "created_at": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
    })
db.products.insert_many(products_data)
print(f"✅ Inserted {len(products_data)} products")

# ============================================================================
# 4. ORDERS COLLECTION
# ============================================================================
print("\n📋 Populating ORDERS collection...")
orders_data = []
for i in range(1, 2001):
    num_items = random.randint(1, 5)
    items = []
    total = 0
    for _ in range(num_items):
        product_id = random.randint(1, 1500)
        quantity = random.randint(1, 10)
        price = round(random.uniform(10, 1000), 2)
        items.append({
            "product_id": product_id,
            "quantity": quantity,
            "price": price,
            "subtotal": round(quantity * price, 2)
        })
        total += quantity * price
    
    orders_data.append({
        "order_id": i,
        "customer_id": random.randint(1, 150),
        "order_date": (datetime.now() - timedelta(days=random.randint(1, 180))).isoformat(),
        "status": random.choice(["pending", "processing", "shipped", "delivered", "cancelled"]),
        "items": items,
        "subtotal": round(total, 2),
        "tax": round(total * 0.08, 2),
        "shipping": round(random.uniform(5, 50), 2),
        "total": round(total * 1.08 + random.uniform(5, 50), 2),
        "payment_method": random.choice(["credit_card", "debit_card", "paypal", "cash"]),
        "shipping_address": {
            "street": f"{random.randint(100, 999)} Oak Ave",
            "city": random.choice(["Boston", "Seattle", "Denver", "Miami"]),
            "state": random.choice(["MA", "WA", "CO", "FL"]),
            "zip": f"{random.randint(10000, 99999)}"
        }
    })
db.orders.insert_many(orders_data)
print(f"✅ Inserted {len(orders_data)} orders")

# ============================================================================
# 5. EMPLOYEES COLLECTION
# ============================================================================
print("\n👔 Populating EMPLOYEES collection...")
positions = ["Manager", "Developer", "Designer", "Analyst", "Sales", "HR", "Marketing"]
employees_data = []
for i in range(1, 501):
    employees_data.append({
        "employee_id": i,
        "first_name": f"FirstName{i}",
        "last_name": f"LastName{i}",
        "email": f"employee{i}@company.com",
        "phone": f"+1-555-{random.randint(1000, 9999)}",
        "position": random.choice(positions),
        "department_id": random.randint(1, 10),
        "salary": random.randint(40000, 150000),
        "hire_date": (datetime.now() - timedelta(days=random.randint(30, 1825))).isoformat(),
        "is_active": random.choice([True, False]),
        "manager_id": random.randint(1, 20) if i > 20 else None,
        "address": {
            "street": f"{random.randint(100, 999)} Elm St",
            "city": random.choice(["Portland", "Austin", "Nashville", "Atlanta"]),
            "state": random.choice(["OR", "TX", "TN", "GA"]),
            "zip": f"{random.randint(10000, 99999)}"
        }
    })
db.employees.insert_many(employees_data)
print(f"✅ Inserted {len(employees_data)} employees")

# ============================================================================
# 6. DEPARTMENTS COLLECTION
# ============================================================================
print("\n🏢 Populating DEPARTMENTS collection...")
departments_data = [
    {"department_id": 1, "name": "Engineering", "budget": 1000000, "head_id": 1},
    {"department_id": 2, "name": "Sales", "budget": 500000, "head_id": 2},
    {"department_id": 3, "name": "Marketing", "budget": 300000, "head_id": 3},
    {"department_id": 4, "name": "Human Resources", "budget": 200000, "head_id": 4},
    {"department_id": 5, "name": "Finance", "budget": 400000, "head_id": 5},
    {"department_id": 6, "name": "Operations", "budget": 600000, "head_id": 6},
    {"department_id": 7, "name": "Customer Support", "budget": 250000, "head_id": 7},
    {"department_id": 8, "name": "Research", "budget": 800000, "head_id": 8},
    {"department_id": 9, "name": "Legal", "budget": 350000, "head_id": 9},
    {"department_id": 10, "name": "IT", "budget": 700000, "head_id": 10}
]
db.departments.insert_many(departments_data)
print(f"✅ Inserted {len(departments_data)} departments")

# ============================================================================
# 7. SALES COLLECTION (Transaction records)
# ============================================================================
print("\n💰 Populating SALES collection...")
sales_data = []
for i in range(1, 3001):
    sales_data.append({
        "sale_id": i,
        "order_id": random.randint(1, 2000),
        "employee_id": random.randint(1, 500),
        "customer_id": random.randint(1, 1000),
        "sale_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
        "amount": round(random.uniform(50, 5000), 2),
        "commission": round(random.uniform(5, 500), 2),
        "region": random.choice(["North", "South", "East", "West", "Central"]),
        "payment_status": random.choice(["paid", "pending", "refunded"])
    })
db.sales.insert_many(sales_data)
print(f"✅ Inserted {len(sales_data)} sales records")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("📊 MONGODB DATA POPULATION COMPLETE!")
print("="*80)
print(f"\n✅ Database: mydb")
print(f"✅ Collections created:")
print(f"   - users: {db.users.count_documents({})} documents")
print(f"   - customers: {db.customers.count_documents({})} documents")
print(f"   - products: {db.products.count_documents({})} documents")
print(f"   - orders: {db.orders.count_documents({})} documents")
print(f"   - employees: {db.employees.count_documents({})} documents")
print(f"   - departments: {db.departments.count_documents({})} documents")
print(f"   - sales: {db.sales.count_documents({})} documents")
print(f"\n📈 Total Documents: {sum([
    db.users.count_documents({}),
    db.customers.count_documents({}),
    db.products.count_documents({}),
    db.orders.count_documents({}),
    db.employees.count_documents({}),
    db.departments.count_documents({}),
    db.sales.count_documents({})
])}")
print("\n🎉 You can now test MongoDB queries!")
print("="*80)

client.close()
