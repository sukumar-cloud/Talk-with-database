"""
Test SQL Injection Detection
Run this to verify the enhanced safety module detects various SQL injection attempts.
"""

from fastapi_app.core.safety import detect_sql_injection, validate_query

# Test cases for SQL injection detection
test_cases = [
    # Safe queries
    ("SELECT * FROM customers WHERE id = 1;", False, "Safe SELECT with WHERE"),
    ("INSERT INTO orders (customer_id, amount) VALUES (1, 100);", False, "Safe INSERT"),
    ("UPDATE customers SET name = 'John' WHERE id = 1;", False, "Safe UPDATE with WHERE"),
    
    # UNION-based injection
    
    ("SELECT * FROM users WHERE id = 1 UNION SELECT * FROM passwords;", True, "UNION SELECT injection"),
    ("SELECT * FROM users WHERE id = 1 UNION ALL SELECT username, password FROM admin;", True, "UNION ALL SELECT injection"),
    
    # Boolean-based injection
    ("SELECT * FROM users WHERE id = 1 OR 1=1;", True, "OR 1=1 injection"),
    ("SELECT * FROM users WHERE username = 'admin' AND '1'='1';", True, "AND '1'='1' injection"),
    ("SELECT * FROM users WHERE id = 1 OR 'a'='a';", True, "OR 'a'='a' injection"),
    
    # Time-based injection
    ("SELECT * FROM users WHERE id = 1 AND SLEEP(5);", True, "SLEEP injection"),
    ("SELECT * FROM users WHERE id = 1 AND BENCHMARK(1000000, MD5('test'));", True, "BENCHMARK injection"),
    ("SELECT * FROM users; WAITFOR DELAY '00:00:05';", True, "WAITFOR injection"),
    
    # Stacked queries
    ("SELECT * FROM users; DROP TABLE users;", True, "Stacked DROP query"),
    ("SELECT * FROM users; DELETE FROM logs;", True, "Stacked DELETE query"),
    
    # Comment-based injection
    ("SELECT * FROM users WHERE username = 'admin' -- AND password = 'pass';", True, "Comment injection --"),
    ("SELECT * FROM users WHERE id = 1 # comment", True, "Comment injection #"),
    ("SELECT * FROM users WHERE id = 1 /* comment */;", True, "Comment injection /**/"),
    
    # Hex encoding
    ("SELECT * FROM users WHERE username = 0x61646d696e;", True, "Hex-encoded value"),
    
    # CHAR encoding
    ("SELECT * FROM users WHERE username = CHAR(97,100,109,105,110);", True, "CHAR encoding"),
    
    # Information schema
    ("SELECT table_name FROM INFORMATION_SCHEMA.TABLES;", True, "Information schema access"),
    ("SELECT * FROM SYS.TABLES;", True, "System catalog access"),
    
    # File access
    ("SELECT LOAD_FILE('/etc/passwd');", True, "LOAD_FILE injection"),
    ("SELECT * FROM users INTO OUTFILE '/tmp/users.txt';", True, "INTO OUTFILE injection"),
    
    # Command execution
    ("EXEC xp_cmdshell 'dir';", True, "xp_cmdshell execution"),
    
    # Concatenation-based
    ("SELECT 'a' || (SELECT password FROM users WHERE id=1);", True, "Concatenation injection"),
    ("SELECT CONCAT('user', (SELECT password FROM users));", True, "CONCAT with SELECT"),
]

def run_tests():
    print("=" * 80)
    print("SQL INJECTION DETECTION TEST SUITE")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for query, should_detect, description in test_cases:
        result = detect_sql_injection(query)
        is_detected = result["detected"]
        
        if is_detected == should_detect:
            status = "[PASS]"
            passed += 1
        else:
            status = "[FAIL]"
            failed += 1
        
        print(f"{status} | {description}")
        print(f"  Query: {query[:70]}{'...' if len(query) > 70 else ''}")
        print(f"  Expected: {'Blocked' if should_detect else 'Allowed'}")
        print(f"  Got: {'Blocked' if is_detected else 'Allowed'}")
        
        if is_detected and result["threats"]:
            print(f"  Severity: {result['severity']}")
            print(f"  Threats detected: {', '.join(result['threats'][:2])}")
        
        print()
    
    print("=" * 80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
    print("=" * 80)
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
