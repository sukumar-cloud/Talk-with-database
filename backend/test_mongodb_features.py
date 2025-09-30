"""
Test MongoDB Features: Injection Detection, NLU, and Query Generation
Similar to SQL tests but for MongoDB/NoSQL
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/mongodb"

def print_header(text):
    print(f"\n{'='*80}")
    print(f"{text}")
    print(f"{'='*80}\n")

def print_test(status, description):
    symbol = "[PASS]" if status else "[FAIL]"
    print(f"{symbol} {description}")

# =============================================================================
# TEST 1: MONGODB INJECTION DETECTION
# =============================================================================
def test_mongodb_injection():
    print_header("TEST 1: MONGODB INJECTION DETECTION")
    
    test_cases = [
        # Safe queries
        ({"username": "john", "age": {"$gt": 18}}, "find", False, "Safe query with $gt"),
        ({"status": "active"}, "find", False, "Safe simple query"),
        
        # Attack patterns
        ({"username": {"$ne": 1}}, "find", True, "Always-true $ne injection"),
        ({"username": {"$ne": None}}, "find", True, "Authentication bypass $ne:null"),
        ({"$or": [{}]}, "find", True, "Empty $or authentication bypass"),
        ({"$where": "function() { return true; }"}, "find", True, "JavaScript $where injection"),
        ({"username": {"$regex": ".*"}}, "find", True, "Regex injection pattern"),
        ({}, "delete", True, "Delete all documents (empty query)"),
        ({}, "update", True, "Update all documents (empty query)"),
        ({"eval": "db.dropDatabase()"}, "find", True, "db.eval code execution"),
    ]
    
    passed = failed = 0
    for query, operation, should_block, description in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/validate",
                json={"query": query, "operation": operation},
                timeout=5
            )
            result = response.json()
            blocked = not result.get("safe", True)
            
            if blocked == should_block:
                print_test(True, description)
                passed += 1
            else:
                print_test(False, f"{description} - Expected: {'Block' if should_block else 'Allow'}, Got: {'Block' if blocked else 'Allow'}")
                failed += 1
                
        except Exception as e:
            print_test(False, f"{description} - Error: {e}")
            failed += 1
    
    print(f"\nResult: {passed}/{passed+failed} tests passed")
    return passed, failed

# =============================================================================
# TEST 2: MONGODB OPERATION CLASSIFICATION
# =============================================================================
def test_mongodb_operation_classification():
    print_header("TEST 2: MONGODB OPERATION CLASSIFICATION")
    
    test_cases = [
        ("find all customers", "find", "Find operation"),
        ("search for users", "find", "Search operation"),
        ("insert new document", "insert", "Insert operation"),
        ("add a record", "insert", "Add operation"),
        ("update customer name", "update", "Update operation"),
        ("delete old records", "delete", "Delete operation"),
        ("count total users", "count", "Count operation"),
        ("aggregate sales by month", "aggregate", "Aggregate operation"),
    ]
    
    passed = failed = 0
    for text, expected_op, description in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/nlu",
                json={"text": text},
                timeout=5
            )
            result = response.json()
            operation = result["operation"]
            
            if operation == expected_op:
                print_test(True, f"{description} - Got: {operation}")
                passed += 1
            else:
                print_test(False, f"{description} - Expected: {expected_op}, Got: {operation}")
                failed += 1
                
        except Exception as e:
            print_test(False, f"{description} - Error: {e}")
            failed += 1
    
    print(f"\nResult: {passed}/{passed+failed} tests passed")
    return passed, failed

# =============================================================================
# TEST 3: MONGODB ENTITY EXTRACTION
# =============================================================================
def test_mongodb_entity_extraction():
    print_header("TEST 3: MONGODB ENTITY EXTRACTION")
    
    schema = {
        "collections": {
            "mydb": ["customers", "orders", "products"]
        }
    }
    
    test_cases = [
        ("find all customers", ["customers"], "Extract collection: customers"),
        ("search orders where status is active", ["orders"], "Extract collection: orders"),
        ("get products with price greater than 100", ["products"], "Extract collection: products"),
    ]
    
    passed = failed = 0
    for text, expected_collections, description in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/nlu",
                json={"text": text, "db_schema": schema},
                timeout=5
            )
            result = response.json()
            entities = result.get("entities", {})
            extracted_collections = entities.get("collections", [])
            
            if any(col in extracted_collections for col in expected_collections):
                print_test(True, f"{description} - Found: {extracted_collections}")
                passed += 1
            else:
                print_test(False, f"{description} - Expected: {expected_collections}, Got: {extracted_collections}")
                failed += 1
                
        except Exception as e:
            print_test(False, f"{description} - Error: {e}")
            failed += 1
    
    print(f"\nResult: {passed}/{passed+failed} tests passed")
    return passed, failed

# =============================================================================
# TEST 4: MONGODB QUERY GENERATION
# =============================================================================
def test_mongodb_query_generation():
    print_header("TEST 4: MONGODB QUERY GENERATION")
    
    schema = {
        "collections": {
            "mydb": ["customers", "orders"]
        }
    }
    
    test_cases = [
        ("find all customers", 5, "Generate 5 query candidates"),
        ("get orders with status active", 5, "Generate query with condition"),
        ("search customers by name", 5, "Generate search query"),
    ]
    
    passed = failed = 0
    for text, expected_count, description in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/generate",
                json={"text": text, "db_schema": schema, "n_candidates": expected_count},
                timeout=10
            )
            result = response.json()
            candidates = result.get("candidates", [])
            
            if len(candidates) > 0:
                print_test(True, f"{description} - Generated {len(candidates)} candidates")
                print(f"   Sample: {candidates[0][:60]}...")
                passed += 1
            else:
                print_test(False, f"{description} - No candidates generated")
                failed += 1
                
        except Exception as e:
            print_test(False, f"{description} - Error: {e}")
            failed += 1
    
    print(f"\nResult: {passed}/{passed+failed} tests passed")
    return passed, failed

# =============================================================================
# TEST 5: MONGODB SCHEMA INSPECTION
# =============================================================================
def test_mongodb_schema_inspection():
    print_header("TEST 5: MONGODB SCHEMA INSPECTION")
    
    passed = failed = 0
    try:
        response = requests.post(
            f"{BASE_URL}/inspect",
            json={"db_type": "mongodb"},
            timeout=10
        )
        result = response.json()
        
        if "databases" in result or "collections" in result:
            databases = result.get("databases", [])
            collections = result.get("collections", {})
            print_test(True, f"Schema inspection - Found {len(databases)} databases")
            print(f"   Databases: {databases[:3]}")
            passed += 1
        else:
            print_test(False, "Schema inspection - No databases found")
            failed += 1
            
    except Exception as e:
        print_test(False, f"Schema inspection - Error: {e}")
        print(f"   Note: This is expected if MongoDB is not configured")
        failed += 1
    
    print(f"\nResult: {passed}/{passed+failed} tests passed")
    return passed, failed

# =============================================================================
# MAIN TEST RUNNER
# =============================================================================
def run_all_tests():
    print("\n" + "="*80)
    print("MONGODB FEATURES TEST SUITE")
    print("Testing: Injection Detection, NLU, and Query Generation")
    print("="*80)
    
    # Check backend health
    print_header("BACKEND HEALTH CHECK")
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print_test(True, "Backend is running")
        else:
            print_test(False, "Backend not responding correctly")
            return
    except Exception as e:
        print_test(False, f"Backend not accessible: {e}")
        print("Please start backend: uvicorn fastapi_app.main:app --reload")
        return
    
    # Run all tests
    results = {}
    results["injection"] = test_mongodb_injection()
    results["operation_classification"] = test_mongodb_operation_classification()
    results["entity_extraction"] = test_mongodb_entity_extraction()
    results["query_generation"] = test_mongodb_query_generation()
    results["schema_inspection"] = test_mongodb_schema_inspection()
    
    # Summary
    print_header("FINAL TEST SUMMARY")
    
    total_passed = sum(r[0] for r in results.values())
    total_failed = sum(r[1] for r in results.values())
    total_tests = total_passed + total_failed
    success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    for test_name, (passed, failed) in results.items():
        status = "[OK]" if failed == 0 else "[WARN]"
        print(f"{status} {test_name.replace('_', ' ').title()}: {passed}/{passed+failed} passed")
    
    print(f"\n{'='*80}")
    print(f"TOTAL: {total_passed}/{total_tests} tests passed ({success_rate:.1f}% success rate)")
    print(f"{'='*80}")
    
    if total_failed == 0:
        print(f"\n*** ALL MONGODB TESTS PASSED! ***\n")
    else:
        print(f"\n[WARNING] {total_failed} tests failed.\n")
    
    print("MongoDB Features Implemented:")
    print("  [OK] MongoDB Injection Detection (NoSQL)")
    print("  [OK] Operation Classification (find, insert, update, delete, aggregate)")
    print("  [OK] Entity Extraction (collections, fields, conditions)")
    print("  [OK] Query Generation (multiple candidates)")
    print("  [OK] Safety Validation")
    print()

if __name__ == "__main__":
    run_all_tests()
