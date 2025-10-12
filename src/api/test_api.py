#!/usr/bin/env python3
"""
Test script for the Competency-Based Learning API
Run this to verify all endpoints are working correctly
"""

import requests
import json
import sys

# Configuration
BASE_URL = 'http://localhost:5000'
API_BASE = f'{BASE_URL}/api'

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test a single API endpoint"""
    url = f'{API_BASE}{endpoint}'
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")
            return True
        else:
            print(f"❌ {method} {endpoint} - Expected: {expected_status}, Got: {response.status_code}")
            print(f"   Response: {response.text[:100]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint} - Connection failed. Is the API running?")
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return False

def run_tests():
    """Run all API tests"""
    print("🧪 Testing Competency-Based Learning API")
    print("=" * 50)
    
    tests_passed = 0
    tests_total = 0
    
    # Health check
    print("\n📋 Health Check Tests")
    tests_total += 1
    if test_endpoint('GET', '/health'):
        tests_passed += 1
    
    # Competency tests
    print("\n📚 Competency Tests")
    tests_total += 2
    if test_endpoint('GET', '/competencies'):
        tests_passed += 1
    if test_endpoint('GET', '/competencies/C1'):
        tests_passed += 1
    
    # Skill tests
    print("\n🎯 Skill Tests")
    tests_total += 3
    if test_endpoint('GET', '/competencies/1/skills'):
        tests_passed += 1
    if test_endpoint('GET', '/competencies/code/C1/skills'):
        tests_passed += 1
    if test_endpoint('GET', '/skills/mmr-range?min_mmr=0&max_mmr=1000'):
        tests_passed += 1
    
    # Question tests
    print("\n❓ Question Tests")
    tests_total += 3
    if test_endpoint('GET', '/questions'):
        tests_passed += 1
    if test_endpoint('GET', '/questions/type/MCQ'):
        tests_passed += 1
    if test_endpoint('GET', '/skills/1/questions'):
        tests_passed += 1
    
    # User tests
    print("\n👤 User Tests")
    tests_total += 2
    if test_endpoint('GET', '/users'):
        tests_passed += 1
    if test_endpoint('GET', '/users/1001'):
        tests_passed += 1
    
    # User attempts tests
    print("\n📝 User Attempt Tests")
    tests_total += 3
    if test_endpoint('GET', '/users/1001/attempts'):
        tests_passed += 1
    if test_endpoint('GET', '/users/1001/attempts/correct'):
        tests_passed += 1
    if test_endpoint('GET', '/users/1001/attempts/incorrect'):
        tests_passed += 1
    
    # Skill ranking tests
    print("\n🏆 Skill Ranking Tests")
    tests_total += 2
    if test_endpoint('GET', '/users/1001/skill-rankings'):
        tests_passed += 1
    if test_endpoint('GET', '/competencies/1/users'):
        tests_passed += 1
    
    # Analytics tests
    print("\n📊 Analytics Tests")
    tests_total += 2
    if test_endpoint('GET', '/users/1001/progress-summary'):
        tests_passed += 1
    if test_endpoint('GET', '/competencies/1/statistics'):
        tests_passed += 1
    
    # Test creating new data
    print("\n➕ Data Creation Tests")
    tests_total += 3
    
    # Test adding a new user
    new_user_data = {"username": "test_user_api"}
    if test_endpoint('POST', '/users', new_user_data, 201):
        tests_passed += 1
    
    # Test adding a new competency
    new_competency_data = {
        "competency_code": "C5",
        "competency_name": "Test Competency",
        "domain_code": "D1",
        "domain_name": "Test Domain",
        "description": "Test description"
    }
    if test_endpoint('POST', '/competencies', new_competency_data, 201):
        tests_passed += 1
    
    # Test adding a new question
    new_question_data = {
        "question_type": "MCQ",
        "question_description": "Test question?",
        "options": "[\"Option A\", \"Option B\", \"Option C\"]",
        "questions_answer": "Option A",
        "question_hint": "Test hint"
    }
    if test_endpoint('POST', '/questions', new_question_data, 201):
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{tests_total} tests passed")
    
    if tests_passed == tests_total:
        print("🎉 All tests passed! API is working correctly.")
        return True
    else:
        print(f"⚠️  {tests_total - tests_passed} tests failed. Check the API implementation.")
        return False

def test_specific_endpoints():
    """Test specific endpoints with detailed output"""
    print("\n🔍 Detailed Endpoint Testing")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f'{API_BASE}/health')
        print(f"Health Check: {response.json()}")
    except Exception as e:
        print(f"Health Check failed: {e}")
    
    # Test competencies endpoint
    try:
        response = requests.get(f'{API_BASE}/competencies')
        data = response.json()
        print(f"Competencies: Found {data.get('count', 0)} competencies")
        if data.get('data'):
            print(f"First competency: {data['data'][0].get('CompetencyName', 'N/A')}")
    except Exception as e:
        print(f"Competencies test failed: {e}")
    
    # Test user progress
    try:
        response = requests.get(f'{API_BASE}/users/1001/progress-summary')
        data = response.json()
        print(f"User Progress: Found {data.get('count', 0)} competency records")
    except Exception as e:
        print(f"User progress test failed: {e}")

if __name__ == '__main__':
    print("🚀 Starting API Tests...")
    
    # Check if API is running
    try:
        response = requests.get(f'{BASE_URL}/api/health', timeout=5)
        if response.status_code != 200:
            print("❌ API is not responding correctly")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running on http://localhost:5000")
        print("   Run: python src/api/app.py")
        sys.exit(1)
    
    # Run tests
    success = run_tests()
    
    # Run detailed tests
    test_specific_endpoints()
    
    if not success:
        sys.exit(1)
    
    print("\n✨ API testing completed successfully!")
