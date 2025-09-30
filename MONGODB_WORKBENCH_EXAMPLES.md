# 📝 MongoDB Workbench Query Examples

Use these queries in your MongoDB Workbench! Copy and paste into the query editor.

---

## 🔍 **BASIC FIND QUERIES**

### Find All Documents
```json
{}
```

### Find with Simple Filter
```json
{"status": "active"}
```

### Find by ID
```json
{"user_id": 1}
```

---

## 👥 **USERS COLLECTION**

### Find Active Users
```json
{"status": "active"}
```

### Find Users from Specific Country
```json
{"country": "USA"}
```

### Find Premium Users
```json
{"is_premium": true}
```

### Find Users by City
```json
{"city": "New York"}
```

### Find Users with High Credits
```json
{"credits": {"$gte": 500}}
```

---

## 👔 **EMPLOYEES COLLECTION**

### Find Active Employees
```json
{"is_active": true}
```

### Find Employees by Department
```json
{"department_id": 1}
```

### Find Managers
```json
{"position": "Manager"}
```

### Find High Salary Employees
```json
{"salary": {"$gte": 80000}}
```

### Find Developers
```json
{"position": "Developer"}
```

---

## 📦 **PRODUCTS COLLECTION**

### Find Active Products
```json
{"is_active": true}
```

### Find Products by Category
```json
{"category_id": 1}
```

### Find Products with Price Range
```json
{"price": {"$gte": 50, "$lte": 200}}
```

### Find Products in Stock
```json
{"stock_quantity": {"$gt": 0}}
```

### Find Featured Products
```json
{"is_featured": true}
```

### Find Products with High Rating
```json
{"rating": {"$gte": 4.0}}
```

### Find Products by SKU
```json
{"sku": "SKU00001"}
```

---

## 🛒 **CUSTOMERS COLLECTION**

### Find Retail Customers
```json
{"customer_type": "retail"}
```

### Find Customers by City
```json
{"city": "NYC"}
```

### Find VIP Customers
```json
{"customer_type": "vip"}
```

### Find Customers with Many Orders
```json
{"total_orders": {"$gte": 10}}
```

### Find High-Spending Customers
```json
{"total_spent": {"$gte": 5000}}
```

---

## 📋 **ORDERS COLLECTION**

### Find Pending Orders
```json
{"status": "pending"}
```

### Find Delivered Orders
```json
{"status": "delivered"}
```

### Find Shipped Orders
```json
{"status": "shipped"}
```

### Find Orders by Customer
```json
{"customer_id": 1}
```

### Find High-Value Orders
```json
{"total_amount": {"$gte": 1000}}
```

### Find Recent Orders (within last 30 days)
```json
{"order_date": {"$gte": "2025-08-30"}}
```

### Find Cancelled Orders
```json
{"status": "cancelled"}
```

---

## 💳 **PAYMENTS COLLECTION**

### Find Completed Payments
```json
{"status": "completed"}
```

### Find Pending Payments
```json
{"status": "pending"}
```

### Find Credit Card Payments
```json
{"payment_method": "Credit Card"}
```

### Find PayPal Payments
```json
{"payment_method": "PayPal"}
```

### Find Large Payments
```json
{"amount": {"$gte": 500}}
```

---

## 🚚 **SHIPMENTS COLLECTION**

### Find In-Transit Shipments
```json
{"status": "in_transit"}
```

### Find Delivered Shipments
```json
{"status": "delivered"}
```

### Find FedEx Shipments
```json
{"carrier": "FedEx"}
```

### Find UPS Shipments
```json
{"carrier": "UPS"}
```

---

## ⭐ **REVIEWS COLLECTION**

### Find 5-Star Reviews
```json
{"rating": 5}
```

### Find Reviews for Specific Product
```json
{"product_id": 1}
```

### Find Reviews by Customer
```json
{"customer_id": 1}
```

### Find Helpful Reviews
```json
{"helpful_count": {"$gte": 50}}
```

### Find Low-Rated Reviews
```json
{"rating": {"$lte": 2}}
```

---

## 📊 **SALES COLLECTION**

### Find Sales by Region
```json
{"region": "North"}
```

### Find High-Value Sales
```json
{"amount": {"$gte": 1000}}
```

### Find Sales by Employee
```json
{"employee_id": 1}
```

### Find Sales with High Commission
```json
{"commission": {"$gte": 100}}
```

---

## 🏷️ **PROMOTIONS COLLECTION**

### Find Active Promotions
```json
{"is_active": true}
```

### Find Percentage Discount Promotions
```json
{"discount_type": "percentage"}
```

### Find High-Discount Promotions
```json
{"discount_value": {"$gte": 20}}
```

### Find Promotions by Code
```json
{"code": "PROMO001"}
```

---

## 🔢 **COMPARISON OPERATORS**

### Greater Than ($gt)
```json
{"price": {"$gt": 100}}
```

### Greater Than or Equal ($gte)
```json
{"age": {"$gte": 18}}
```

### Less Than ($lt)
```json
{"stock_quantity": {"$lt": 50}}
```

### Less Than or Equal ($lte)
```json
{"price": {"$lte": 200}}
```

### Not Equal ($ne)
```json
{"status": {"$ne": "cancelled"}}
```

### In Array ($in)
```json
{"status": {"$in": ["pending", "processing"]}}
```

### Not In Array ($nin)
```json
{"status": {"$nin": ["cancelled", "refunded"]}}
```

---

## 🎯 **LOGICAL OPERATORS**

### AND ($and)
```json
{"$and": [
  {"status": "active"},
  {"price": {"$gte": 50}}
]}
```

### OR ($or)
```json
{"$or": [
  {"status": "pending"},
  {"status": "processing"}
]}
```

### NOR ($nor)
```json
{"$nor": [
  {"status": "cancelled"},
  {"status": "refunded"}
]}
```

### NOT ($not)
```json
{"price": {"$not": {"$gte": 100}}}
```

---

## 🔍 **ELEMENT OPERATORS**

### Field Exists ($exists)
```json
{"phone": {"$exists": true}}
```

### Field Type ($type)
```json
{"age": {"$type": "number"}}
```

---

## 📝 **ARRAY OPERATORS**

### Array Contains Value ($elemMatch)
```json
{"tags": {"$elemMatch": {"$eq": "electronics"}}}
```

### Array Size ($size)
```json
{"items": {"$size": 3}}
```

---

## 🌟 **COMPLEX QUERIES**

### Multiple Conditions with AND
```json
{
  "status": "active",
  "price": {"$gte": 50, "$lte": 200},
  "is_featured": true
}
```

### Multiple Conditions with OR
```json
{
  "$or": [
    {"customer_type": "vip"},
    {"total_spent": {"$gte": 5000}}
  ]
}
```

### Nested Conditions
```json
{
  "$and": [
    {"status": "delivered"},
    {"$or": [
      {"total_amount": {"$gte": 500}},
      {"customer_type": "vip"}
    ]}
  ]
}
```

### Range Query
```json
{
  "salary": {"$gte": 50000, "$lte": 100000},
  "department_id": {"$in": [1, 2, 3]}
}
```

---

## 📊 **SORTING & LIMITING**

### Note: MongoDB Workbench uses pure JSON queries
### For sorting/limiting, you'd typically use:
```javascript
// In MongoDB Shell or Compass:
db.products.find({"is_active": true}).sort({price: -1}).limit(10)
```

### But in our workbench, just use the filter:
```json
{"is_active": true}
```

---

## 🎯 **QUICK TEST QUERIES**

### Test 1: Find Active Users
```json
{"status": "active"}
```

### Test 2: Find High-Priced Products
```json
{"price": {"$gte": 300}}
```

### Test 3: Find Delivered Orders
```json
{"status": "delivered"}
```

### Test 4: Find Completed Payments
```json
{"status": "completed"}
```

### Test 5: Find 5-Star Reviews
```json
{"rating": 5}
```

### Test 6: Find In-Stock Products
```json
{"stock_quantity": {"$gt": 0}}
```

### Test 7: Find Premium Users
```json
{"is_premium": true}
```

### Test 8: Find Employees in Engineering
```json
{"department_id": 1}
```

### Test 9: Find VIP Customers
```json
{"customer_type": "vip"}
```

### Test 10: Find Active Promotions
```json
{"is_active": true}
```

---

## 💡 **TIPS FOR MONGODB WORKBENCH:**

1. **Always use valid JSON** - Keys and strings must be in double quotes
2. **Start simple** - Begin with basic filters like `{"status": "active"}`
3. **Add complexity** - Gradually add more conditions
4. **Use operators** - Master `$gte`, `$lte`, `$in`, `$or`, etc.
5. **Test incrementally** - Start with one condition, then add more

---

## 🚀 **GETTING STARTED:**

1. Open MongoDB Workbench: http://localhost:5173/mongodb-workbench
2. Select a database (mydb)
3. Select a collection (users, products, orders, etc.)
4. Paste a query from above into the query editor
5. Click "Execute"
6. View results!

---

## 🎊 **EXAMPLE WORKFLOW:**

**Step 1:** Select `users` collection

**Step 2:** Paste this query:
```json
{"status": "active"}
```

**Step 3:** Click Execute

**Step 4:** See all active users!

**Step 5:** Try more complex query:
```json
{"status": "active", "is_premium": true, "credits": {"$gte": 500}}
```

---

**Happy Querying! 🎉**
