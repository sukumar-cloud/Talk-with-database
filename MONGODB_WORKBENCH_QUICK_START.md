# 🚀 MongoDB Workbench - Quick Start

## ✅ **What I Just Fixed:**
1. ✅ Query persistence - Queries now save automatically
2. ✅ Operation persistence - Selected operation remembered
3. ✅ Works like SQL Workbench - No more lost queries!

---

## 📝 **What to Type in Query Editor:**

### **JSON Queries (not natural language!):**

```json
{}
```
**↑ This finds ALL documents**

```json
{"status": "active"}
```
**↑ Find documents where status = "active"**

```json
{"is_active": true}
```
**↑ Find documents where is_active = true**

```json
{"price": {"$gte": 100}}
```
**↑ Find documents where price >= 100**

---

## 🎯 **Quick Copy-Paste Examples:**

### **Find Active Users:**
```json
{"status": "active"}
```

### **Find High-Priced Products:**
```json
{"price": {"$gte": 300}}
```

### **Find Delivered Orders:**
```json
{"status": "delivered"}
```

### **Find Premium Users:**
```json
{"is_premium": true}
```

### **Find Employees in Department 1:**
```json
{"department_id": 1}
```

### **Find Products in Stock:**
```json
{"stock_quantity": {"$gt": 0}}
```

### **Find VIP Customers:**
```json
{"customer_type": "vip"}
```

### **Find Completed Payments:**
```json
{"status": "completed"}
```

### **Find 5-Star Reviews:**
```json
{"rating": 5}
```

### **Find Active Promotions:**
```json
{"is_active": true}}
```

---

## 🔄 **How It Works:**

1. **Select Collection** (left sidebar)
   - Click on: users, products, orders, etc.

2. **Paste JSON Query** (query editor)
   - Paste one of the examples above

3. **Click Execute** (green button)
   - See results below!

4. **Query Saved!**
   - Leave page and come back - query is still there!

---

## 💡 **Pro Tips:**

- **Use "Sample" button** - Gets a starter query
- **Use "Clear" button** - Resets to `{}`
- **JSON only** - Not natural language
- **Valid JSON** - Use double quotes: `{"status": "active"}`

---

**🎊 Your MongoDB Workbench is now ready! Queries persist across page navigation!**
