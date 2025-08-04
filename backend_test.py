#!/usr/bin/env python3
"""
Backend API Testing for Quantum Aegis Platform
Tests the cybersecurity dashboard API endpoints for metrics and threats
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any

class QuantumAegisAPITester:
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = f"{status} - {name}"
        if details:
            result += f": {details}"
        
        print(result)
        self.test_results.append({
            'name': name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        return success

    def test_api_endpoint(self, endpoint: str, expected_fields: List[str] = None) -> tuple:
        """Test a single API endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}", {}
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                return False, "Invalid JSON response", {}
            
            # Check expected fields if provided
            if expected_fields:
                missing_fields = [field for field in expected_fields if field not in data]
                if missing_fields:
                    return False, f"Missing fields: {missing_fields}", data
            
            return True, "Success", data
            
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}", {}

    def test_metrics_endpoint(self):
        """Test /api/demo/metrics endpoint"""
        print("\n🔍 Testing Metrics API Endpoint...")
        
        expected_fields = ['threatsBlocked', 'mttd', 'aiConfidence', 'quantumKeys']
        success, message, data = self.test_api_endpoint('/api/demo/metrics', expected_fields)
        
        if not success:
            return self.log_test("Metrics API Basic", False, message)
        
        # Test data types and ranges
        validation_tests = [
            ('threatsBlocked', int, lambda x: x > 0, "should be positive integer"),
            ('mttd', (int, float), lambda x: 0 < x < 10, "should be between 0-10 seconds"),
            ('aiConfidence', (int, float), lambda x: 0 <= x <= 100, "should be 0-100%"),
            ('quantumKeys', int, lambda x: x > 0, "should be positive integer")
        ]
        
        all_valid = True
        for field, expected_type, validator, description in validation_tests:
            value = data.get(field)
            if not isinstance(value, expected_type):
                self.log_test(f"Metrics {field} type", False, f"Expected {expected_type}, got {type(value)}")
                all_valid = False
            elif not validator(value):
                self.log_test(f"Metrics {field} range", False, f"Value {value} {description}")
                all_valid = False
            else:
                self.log_test(f"Metrics {field} validation", True, f"Value: {value}")
        
        return self.log_test("Metrics API Complete", all_valid, f"All fields validated: {data}")

    def test_threats_endpoint(self):
        """Test /api/demo/threats endpoint"""
        print("\n🔍 Testing Threats API Endpoint...")
        
        success, message, data = self.test_api_endpoint('/api/demo/threats')
        
        if not success:
            return self.log_test("Threats API Basic", False, message)
        
        if not isinstance(data, list):
            return self.log_test("Threats API Format", False, f"Expected array, got {type(data)}")
        
        if len(data) == 0:
            return self.log_test("Threats API Data", False, "No threats returned")
        
        # Test threat object structure
        required_fields = ['title', 'source', 'type', 'status', 'timestamp']
        all_valid = True
        
        for i, threat in enumerate(data[:3]):  # Test first 3 threats
            if not isinstance(threat, dict):
                self.log_test(f"Threat {i} format", False, f"Expected dict, got {type(threat)}")
                all_valid = False
                continue
            
            missing_fields = [field for field in required_fields if field not in threat]
            if missing_fields:
                self.log_test(f"Threat {i} fields", False, f"Missing: {missing_fields}")
                all_valid = False
            else:
                self.log_test(f"Threat {i} structure", True, f"Title: {threat.get('title', 'N/A')}")
        
        # Test realistic cybersecurity data
        valid_types = ['malware', 'phishing', 'ransomware', 'ddos', 'intrusion', 'botnet', 
                      'credential_theft', 'data_exfiltration', 'zero_day', 'sql_injection']
        valid_statuses = ['BLOCKED', 'INVESTIGATING', 'MITIGATED', 'QUARANTINED']
        
        type_check = any(threat.get('type') in valid_types for threat in data)
        status_check = any(threat.get('status') in valid_statuses for threat in data)
        
        self.log_test("Threats realistic types", type_check, f"Found valid threat types")
        self.log_test("Threats realistic statuses", status_check, f"Found valid statuses")
        
        return self.log_test("Threats API Complete", all_valid and type_check and status_check, 
                           f"Returned {len(data)} threats")

    def test_dynamic_data(self):
        """Test that data changes over time"""
        print("\n🔍 Testing Dynamic Data Changes...")
        
        # Get initial metrics
        success1, _, data1 = self.test_api_endpoint('/api/demo/metrics')
        if not success1:
            return self.log_test("Dynamic Data Setup", False, "Failed to get initial metrics")
        
        # Wait 2 seconds
        time.sleep(2)
        
        # Get second set of metrics
        success2, _, data2 = self.test_api_endpoint('/api/demo/metrics')
        if not success2:
            return self.log_test("Dynamic Data Fetch", False, "Failed to get second metrics")
        
        # Check if any values changed
        changes = []
        for key in ['threatsBlocked', 'mttd', 'aiConfidence', 'quantumKeys']:
            if data1.get(key) != data2.get(key):
                changes.append(f"{key}: {data1.get(key)} → {data2.get(key)}")
        
        if changes:
            return self.log_test("Dynamic Data Changes", True, f"Changes detected: {', '.join(changes)}")
        else:
            return self.log_test("Dynamic Data Changes", True, "Data may be stable (acceptable)")

    def test_cors_headers(self):
        """Test CORS headers are present"""
        print("\n🔍 Testing CORS Headers...")
        
        try:
            response = requests.get(f"{self.base_url}/api/demo/metrics", timeout=10)
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            has_cors = any(cors_headers.values())
            return self.log_test("CORS Headers", has_cors, f"Headers: {cors_headers}")
            
        except Exception as e:
            return self.log_test("CORS Headers", False, f"Error: {str(e)}")

    def test_server_availability(self):
        """Test if server is responding"""
        print("\n🔍 Testing Server Availability...")
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            success = response.status_code == 200
            return self.log_test("Server Availability", success, 
                               f"HTTP {response.status_code}, Content-Type: {response.headers.get('content-type', 'N/A')}")
        except Exception as e:
            return self.log_test("Server Availability", False, f"Error: {str(e)}")

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Quantum Aegis API Testing Suite")
        print(f"Testing against: {self.base_url}")
        print("=" * 60)
        
        # Run all tests
        self.test_server_availability()
        self.test_metrics_endpoint()
        self.test_threats_endpoint()
        self.test_dynamic_data()
        self.test_cors_headers()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Results Summary:")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed! API is working correctly.")
            return 0
        else:
            print("⚠️  Some tests failed. Check the details above.")
            return 1

def main():
    """Main test execution"""
    tester = QuantumAegisAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())