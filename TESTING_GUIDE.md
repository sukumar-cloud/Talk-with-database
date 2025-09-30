# 🧪 Complete Testing Guide - All Objectives

This guide helps you manually test all implemented features.

---

## 🚀 Quick Start

### 1. Start Backend:
```bash
cd backend
uvicorn fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend:
```bash
cd project
npm run dev
```

### 3. Run Automated Tests:
```bash
cd backend
python test_all_features.py
```

---

## ✅ Test Checklist (All 5 Objectives)

### **Objective 1: NLU & Intent Classification (100%)**

#### ✅ Test 1.1: Intent Classification
```bash
curl -X POST http://localhost:8000/nlu/parse \
  -H "Content-Type: application/json" \
  -d '{"text": "show all customers", "use_transformer": false}'
```

**Expected Response:**
```json
{
  "intent": "SELECT",
  "confidence": 0.xx,
  "method": "keyword",
  "entities": {...},
  "dependencies": [...]
}
```

**Test Cases:**
- "show all customers" → SELECT
- "delete old records" → DELETE
- "update user names" → UPDATE
- "insert new order" → INSERT
- "call api endpoint" → API_FETCH

---

#### ✅ Test 1.2: Named Entity Recognition (NER)
```bash
curl -X POST http://localhost:8000/nlu/parse \
  -H "Content-Type: application/json" \
  -d '{
    "text": "show customers from orders table",
    "schema": {
      "tables": ["customers", "orders"],
      "columns": {"customers": [{"name": "id"}]}
    }
  }'
```

**Expected:** Should extract `["customers", "orders"]` from text

---

#### ✅ Test 1.3: Dependency Parsing
```bash
curl -X POST http://localhost:8000/nlu/parse \
  -H "Content-Type: application/json" \
  -d '{"text": "show all customers from database"}'
```

**Expected:** Should return dependencies array with POS tags and syntactic relations

---

### **Objective 2: Schema-Aware Generation (100%)**

#### ✅ Test 2.1: Schema Introspection
```bash
curl -X POST http://localhost:8000/schema/inspect \
  -H "Content-Type: application/json" \
  -d '{"db_type": "mysql"}'
```

**Expected Response:**
```json
{
  "db": "mydb",
  "tables": ["customers", "orders", ...],
  "columns": {...},
  "primary_keys": {...},
  "foreign_keys": [...]
}
```

---

#### ✅ Test 2.2: Query Generation
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "show all customers",
    "schema": {"tables": ["customers"]},
    "db_type": "mysql"
  }'
```

**Expected:** Should return array of SQL queries

---

#### ✅ Test 2.3: Beam Search Parameters
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "show customers",
    "n_candidates": 10,
    "temperature": 0.5,
    "top_p": 0.9,
    "max_tokens": 200
  }'
```

**Expected Response:**
```json
{
  "candidates": ["SELECT...", ...],
  "provider": "mixtral",
  "generation_params": {
    "n_candidates": 10,
    "temperature": 0.5,
    "top_p": 0.9,
    "max_tokens": 200
  }
}
```

---

### **Objective 3: Safety Layer & Validation (100%)**

#### ✅ Test 3.1: Safe Query Validation
```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "candidates": ["SELECT * FROM customers WHERE id = 1"],
    "db_type": "mysql"
  }'
```

**Expected:**
```json
{
  "results": [{
    "valid_syntax": true,
    "blocked": false,
    "reasons": []
  }]
}
```

---

#### ✅ Test 3.2: SQL Injection Detection
```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "candidates": ["SELECT * FROM users WHERE id=1 OR 1=1"],
    "db_type": "mysql"
  }'
```

**Expected:**
```json
{
  "results": [{
    "valid_syntax": true,
    "blocked": true,
    "injection_severity": "MEDIUM",
    "reasons": ["SQL_INJECTION: Boolean-based injection (OR 1=1) detected"]
  }]
}
```

**Test Attack Patterns:**
- `OR 1=1` → Boolean injection
- `UNION SELECT` → Union injection
- `; DROP TABLE` → Stacked query
- `AND SLEEP(5)` → Time-based
- `--` comment → Comment injection
- `0x616263` → Hex encoding
- `information_schema` → Info schema
- `LOAD_FILE` → File operation

---

#### ✅ Test 3.3: Dangerous Query Detection
```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "candidates": ["DELETE FROM customers"],
    "db_type": "mysql"
  }'
```

**Expected:** Should block DELETE without WHERE

---

### **Objective 4: Weighted Ranking (100%)**

#### ✅ Test 4.1: Sentence-BERT Ranking
```bash
curl -X POST http://localhost:8000/rank \
  -H "Content-Type: application/json" \
  -d '{
    "text": "show all customers",
    "candidates": [
      "SELECT * FROM customers LIMIT 10;",
      "SELECT name FROM customers;",
      "SELECT * FROM orders;"
    ],
    "schema": {"tables": ["customers", "orders"]},
    "db_type": "mysql"
  }'
```

**Expected Response:**
```json
{
  "ranked": [
    {
      "query": "SELECT * FROM customers LIMIT 10;",
      "score": 2.87,
      "syntax_ok": true,
      "schema_score": 1.0,
      "sim": 0.87
    },
    ...
  ]
}
```

**Check:** 
- `sim` score should be present (Sentence-BERT)
- Higher score = better match
- Queries ranked by total score

---

### **Objective 5: Interactive UI (100%)**

#### ✅ Test 5.1: Frontend Pages
Visit these URLs in browser:

1. **Home:** http://localhost:5173/
2. **SQL Query:** http://localhost:5173/sql-query
3. **SQL Workbench:** http://localhost:5173/sql-workbench
4. **Schema Workbench:** http://localhost:5173/schema
5. **MongoDB Query:** http://localhost:5173/mongodb-query
6. **Query History:** http://localhost:5173/history
7. **Documentation:** http://localhost:5173/docs

---

#### ✅ Test 5.2: SQL Query Page Features
1. Enter: "show all customers"
2. Click "Generate SQL"
3. **Check:**
   - Query generated
   - If dangerous query (e.g., "delete all"), red warning appears
   - Can execute or copy query

---

#### ✅ Test 5.3: SQL Workbench Features
1. Open SQL Workbench
2. **Check:**
   - Left panel: Schema browser loads
   - Middle: Query editor works
   - Bottom: Results display
   - Double-click table name → inserts into editor
3. Try dangerous query: `DELETE FROM customers`
4. **Check:** Confirmation dialog appears

---

#### ✅ Test 5.4: Schema Workbench
1. Open Schema Workbench
2. **Check:**
   - List View: Tables displayed
   - Diagram View: ER diagram renders
   - Can drag nodes
   - Foreign keys shown as lines
   - Primary keys highlighted

---

#### ✅ Test 5.5: Query History
1. Execute some queries
2. Visit History page
3. **Check:**
   - All queries logged
   - Statistics shown (total, success rate, avg time)
   - Can search queries
   - Can delete individual queries

---

## 🔥 Advanced Integration Tests

### Test A: Full Workflow
```bash
# 1. Parse intent
curl -X POST http://localhost:8000/nlu/parse \
  -H "Content-Type: application/json" \
  -d '{"text": "show top 10 customers by orders"}'

# 2. Get schema
curl -X POST http://localhost:8000/schema/inspect \
  -H "Content-Type: application/json" \
  -d '{"db_type": "mysql"}'

# 3. Generate queries
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "show top 10 customers by orders",
    "schema": {...},
    "n_candidates": 5
  }'

# 4. Validate safety
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{"candidates": [...], "db_type": "mysql"}'

# 5. Rank queries
curl -X POST http://localhost:8000/rank \
  -H "Content-Type: application/json" \
  -d '{
    "text": "show top 10 customers by orders",
    "candidates": [...],
    "schema": {...}
  }'

# 6. Execute best query
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "...", "db_type": "mysql"}'
```

---

## 📊 Expected Test Results

### Automated Test Suite (`test_all_features.py`)
**Expected Output:**
```
✅ SQL Injection Detection: 10/10 passed
✅ Intent Classification: 7/7 passed
✅ Named Entity Recognition: 3/3 passed
✅ Dependency Parsing: 3/3 passed
✅ Beam Search Parameters: 3/3 passed
✅ Sentence-BERT Ranking: 2/2 passed
✅ Schema Introspection: 1/1 passed
✅ Full Integration: 1/1 passed

TOTAL: 30/30 tests passed (100% success rate)
🎉 ALL TESTS PASSED! PROJECT 100% COMPLETE! 🎉
```

---

## 🐛 Troubleshooting

### Issue: Tests fail with connection error
**Solution:**
```bash
# Check if backend is running
curl http://localhost:8000/

# If not, start it
cd backend
uvicorn fastapi_app.main:app --reload
```

---

### Issue: "Module not found" errors
**Solution:**
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

### Issue: Slow tests
**Note:** First request loads AI models (2-5 seconds). Subsequent requests are fast (<100ms).

---

## 📝 Manual Testing Checklist

Print this and check off each item:

```
□ Backend starts without errors
□ Frontend loads at localhost:5173
□ SQL Injection detection blocks malicious queries
□ Safe queries are allowed
□ Intent classification works (7 types)
□ NER extracts tables/columns from text
□ Dependency parsing returns syntactic structure
□ Schema introspection returns tables
□ Query generation works with beam search params
□ Ranking includes semantic similarity (sim score)
□ All frontend pages load
□ SQL Query page shows dangerous query warnings
□ SQL Workbench has confirmation for dangerous ops
□ Schema Workbench shows ER diagram
□ Query history tracks all queries
□ Documentation page renders correctly
□ Automated test suite: 30/30 passed
```

---

## 🎯 Success Criteria

**All objectives complete when:**
- ✅ `test_all_features.py` passes 100%
- ✅ `test_sql_injection.py` passes 25/25
- ✅ All frontend pages accessible
- ✅ No errors in browser console
- ✅ No errors in backend logs
- ✅ Sentence-BERT returns similarity scores
- ✅ Beam search parameters work
- ✅ Intent classification works
- ✅ NER extracts entities
- ✅ Dependency parsing works

---

## 🎊 Verification Complete!

After running all tests successfully, you have verified:

1. **Objective 1 (100%):** NLU with intent classification, NER, dependency parsing
2. **Objective 2 (100%):** Schema-aware generation with beam search control
3. **Objective 3 (100%):** Safety layer with 19 SQL injection patterns
4. **Objective 4 (100%):** Weighted ranking with Sentence-BERT
5. **Objective 5 (100%):** Interactive UI with all features

**Your project is production-ready! 🚀**
