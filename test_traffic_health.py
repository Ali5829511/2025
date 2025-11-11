#!/usr/bin/env python3
"""
Traffic Violations System - Health Check Test
اختبار فحص صحة نظام المخالفات المرورية

This script tests the health check endpoints and basic functionality.
"""
import sys
import requests
import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"{Fore.CYAN}{Style.BRIGHT}{text}")
    print("="*60)

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.YELLOW}ℹ️  {text}")

def test_health_endpoint(base_url):
    """Test health check endpoint"""
    print_header("Testing Health Check Endpoint")
    
    endpoints = ["/health", "/api/health"]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print_info(f"Testing: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    print_success(f"Health check passed: {endpoint}")
                    print(f"   Service: {data.get('service')}")
                    print(f"   Database: {data.get('database')}")
                    print(f"   Timestamp: {data.get('timestamp')}")
                else:
                    print_error(f"Health check returned unhealthy status")
                    return False
            else:
                print_error(f"Health check failed with status {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print_error(f"Request failed: {str(e)}")
            return False
    
    return True

def test_root_endpoint(base_url):
    """Test root endpoint"""
    print_header("Testing Root Endpoint")
    
    url = base_url + "/"
    print_info(f"Testing: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print_success("Root endpoint accessible")
            print(f"   Content-Type: {response.headers.get('Content-Type')}")
            print(f"   Content Length: {len(response.content)} bytes")
            return True
        else:
            print_error(f"Root endpoint failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        return False

def test_api_violations(base_url):
    """Test violations API endpoint"""
    print_header("Testing Violations API")
    
    url = base_url + "/api/violations"
    print_info(f"Testing: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success("Violations API working")
                print(f"   Total violations: {data.get('total', 0)}")
                return True
            else:
                print_error("API returned success=False")
                return False
        else:
            print_error(f"API failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        return False

def test_api_cars(base_url):
    """Test cars API endpoint"""
    print_header("Testing Cars API")
    
    url = base_url + "/api/cars"
    print_info(f"Testing: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success("Cars API working")
                print(f"   Total cars: {data.get('total', 0)}")
                return True
            else:
                print_error("API returned success=False")
                return False
        else:
            print_error(f"API failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        return False

def main():
    """Main test function"""
    # Get base URL from command line or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:10000"
    
    print_header(f"Traffic Violations System Health Check")
    print_info(f"Testing server at: {base_url}")
    print_info(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    tests = [
        ("Health Check", test_health_endpoint),
        ("Root Endpoint", test_root_endpoint),
        ("Violations API", test_api_violations),
        ("Cars API", test_api_cars)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func(base_url)
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test {test_name} crashed: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{Fore.CYAN}Total: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 All tests passed! System is healthy.")
        return 0
    else:
        print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
