#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Advanced Testing Suite - Web Interface Automated Tests
This script runs automated tests for the web interface.
"""

import os
import sys
import time
import json
import requests
import subprocess
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class WebInterfaceTester:
    """Web interface automated tester"""
    
    def __init__(self):
        self.base_url = "http://localhost:8501"
        self.driver = None
        self.test_results = []
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            # Try to find ChromeDriver
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Chrome WebDriver initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Chrome WebDriver: {e}")
            print("Please install ChromeDriver or check if Chrome is installed")
            sys.exit(1)
    
    def start_web_interface(self):
        """Start the web interface"""
        print("🚀 Starting web interface...")
        
        # Check if web interface is already running
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("✅ Web interface is already running")
                return True
        except requests.exceptions.ConnectionError:
            pass
        
        # Start the web interface
        try:
            # Use the visual_test_interface.py script
            script_path = project_root / "visual_test_interface.py"
            if not script_path.exists():
                print(f"❌ Web interface script not found: {script_path}")
                return False
            
            # Start the web interface in background
            self.web_process = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=project_root
            )
            
            # Wait for web interface to start
            print("⏳ Waiting for web interface to start...")
            for i in range(30):  # Wait up to 30 seconds
                try:
                    response = requests.get(f"{self.base_url}/")
                    if response.status_code == 200:
                        print("✅ Web interface started successfully")
                        return True
                except requests.exceptions.ConnectionError:
                    pass
                time.sleep(1)
            
            print("❌ Web interface failed to start")
            return False
            
        except Exception as e:
            print(f"❌ Error starting web interface: {e}")
            return False
    
    def test_home_page(self):
        """Test the home page"""
        print("🧪 Testing home page...")
        
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("✅ Home page loaded successfully")
                self.test_results.append({
                    "test": "Home Page",
                    "status": "PASS",
                    "message": "Home page loaded successfully"
                })
                return True
            else:
                print(f"❌ Home page returned status code: {response.status_code}")
                self.test_results.append({
                    "test": "Home Page",
                    "status": "FAIL",
                    "message": f"Status code: {response.status_code}"
                })
                return False
        except Exception as e:
            print(f"❌ Error accessing home page: {e}")
            self.test_results.append({
                "test": "Home Page",
                "status": "FAIL",
                "message": str(e)
            })
            return False
    
    def test_api_endpoints(self):
        """Test API endpoints"""
        print("🧪 Testing API endpoints...")
        
        endpoints = [
            ("/api/models", "GET"),
            ("/api/tests", "GET"),
            ("/api/run_test", "POST"),
            ("/api/results", "GET")
        ]
        
        for endpoint, method in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}")
                elif method == "POST":
                    response = requests.post(f"{self.base_url}{endpoint}")
                
                if response.status_code in [200, 201]:
                    print(f"✅ {endpoint} - {method} - SUCCESS")
                    self.test_results.append({
                        "test": f"API {endpoint}",
                        "status": "PASS",
                        "message": f"{method} request successful"
                    })
                else:
                    print(f"❌ {endpoint} - {method} - Status: {response.status_code}")
                    self.test_results.append({
                        "test": f"API {endpoint}",
                        "status": "FAIL",
                        "message": f"Status code: {response.status_code}"
                    })
            except Exception as e:
                print(f"❌ {endpoint} - {method} - ERROR: {e}")
                self.test_results.append({
                    "test": f"API {endpoint}",
                    "status": "FAIL",
                    "message": str(e)
                })
    
    def test_ui_elements(self):
        """Test UI elements using Selenium"""
        print("🧪 Testing UI elements...")
        
        try:
            # Navigate to home page
            self.driver.get(self.base_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Test various UI elements
            tests = [
                ("title", "LLM Advanced Testing Suite"),
                ("header", "LLM Advanced Testing Suite"),
                ("sidebar", "sidebar"),
                ("main_content", "main")
            ]
            
            for element_name, selector in tests:
                try:
                    if selector == "title":
                        element = self.driver.title
                    elif selector == "header":
                        element = self.driver.find_element(By.TAG_NAME, "h1").text
                    elif selector == "sidebar":
                        element = self.driver.find_element(By.CLASS_NAME, "sidebar")
                    elif selector == "main":
                        element = self.driver.find_element(By.CLASS_NAME, "main")
                    
                    print(f"✅ {element_name} - Found")
                    self.test_results.append({
                        "test": f"UI Element - {element_name}",
                        "status": "PASS",
                        "message": f"Found {element_name}"
                    })
                    
                except NoSuchElementException:
                    print(f"❌ {element_name} - Not found")
                    self.test_results.append({
                        "test": f"UI Element - {element_name}",
                        "status": "FAIL",
                        "message": f"{element_name} not found"
                    })
                except Exception as e:
                    print(f"❌ {element_name} - Error: {e}")
                    self.test_results.append({
                        "test": f"UI Element - {element_name}",
                        "status": "FAIL",
                        "message": str(e)
                    })
            
        except Exception as e:
            print(f"❌ Error testing UI elements: {e}")
            self.test_results.append({
                "test": "UI Elements",
                "status": "FAIL",
                "message": str(e)
            })
    
    def test_navigation(self):
        """Test navigation between pages"""
        print("🧪 Testing navigation...")
        
        try:
            # Test navigation to different sections
            sections = ["models", "tests", "results", "about"]
            
            for section in sections:
                try:
                    # Try to navigate to section
                    self.driver.get(f"{self.base_url}/{section}")
                    time.sleep(1)  # Wait for navigation
                    
                    # Check if page loaded successfully
                    if "404" not in self.driver.title and "Error" not in self.driver.title:
                        print(f"✅ Navigation to {section} - SUCCESS")
                        self.test_results.append({
                            "test": f"Navigation - {section}",
                            "status": "PASS",
                            "message": f"Successfully navigated to {section}"
                        })
                    else:
                        print(f"❌ Navigation to {section} - FAILED")
                        self.test_results.append({
                            "test": f"Navigation - {section}",
                            "status": "FAIL",
                            "message": f"Failed to navigate to {section}"
                        })
                        
                except Exception as e:
                    print(f"❌ Navigation to {section} - ERROR: {e}")
                    self.test_results.append({
                        "test": f"Navigation - {section}",
                        "status": "FAIL",
                        "message": str(e)
                    })
            
        except Exception as e:
            print(f"❌ Error testing navigation: {e}")
            self.test_results.append({
                "test": "Navigation",
                "status": "FAIL",
                "message": str(e)
            })
    
    def test_responsiveness(self):
        """Test responsive design"""
        print("🧪 Testing responsive design...")
        
        try:
            # Test different screen sizes
            screen_sizes = [
                (1920, 1080),  # Desktop
                (768, 1024),   # Tablet
                (375, 667),    # Mobile
            ]
            
            for width, height in screen_sizes:
                try:
                    # Set window size
                    self.driver.set_window_size(width, height)
                    time.sleep(1)  # Wait for resize
                    
                    # Check if elements are still visible
                    body = self.driver.find_element(By.TAG_NAME, "body")
                    if body.is_displayed():
                        print(f"✅ Responsive design - {width}x{height} - SUCCESS")
                        self.test_results.append({
                            "test": f"Responsive - {width}x{height}",
                            "status": "PASS",
                            "message": f"Responsive design works at {width}x{height}"
                        })
                    else:
                        print(f"❌ Responsive design - {width}x{height} - FAILED")
                        self.test_results.append({
                            "test": f"Responsive - {width}x{height}",
                            "status": "FAIL",
                            "message": f"Elements not visible at {width}x{height}"
                        })
                        
                except Exception as e:
                    print(f"❌ Responsive design - {width}x{height} - ERROR: {e}")
                    self.test_results.append({
                        "test": f"Responsive - {width}x{height}",
                        "status": "FAIL",
                        "message": str(e)
                    })
            
        except Exception as e:
            print(f"❌ Error testing responsive design: {e}")
            self.test_results.append({
                "test": "Responsive Design",
                "status": "FAIL",
                "message": str(e)
            })
    
    def test_performance(self):
        """Test page load performance"""
        print("🧪 Testing performance...")
        
        try:
            # Test page load times
            pages = ["/", "/api/models", "/api/tests"]
            
            for page in pages:
                start_time = time.time()
                try:
                    self.driver.get(f"{self.base_url}{page}")
                    end_time = time.time()
                    load_time = end_time - start_time
                    
                    if load_time < 3.0:  # Less than 3 seconds
                        print(f"✅ Performance - {page} - {load_time:.2f}s - GOOD")
                        self.test_results.append({
                            "test": f"Performance - {page}",
                            "status": "PASS",
                            "message": f"Load time: {load_time:.2f}s"
                        })
                    else:
                        print(f"⚠️ Performance - {page} - {load_time:.2f}s - SLOW")
                        self.test_results.append({
                            "test": f"Performance - {page}",
                            "status": "WARNING",
                            "message": f"Load time: {load_time:.2f}s (slow)"
                        })
                        
                except Exception as e:
                    print(f"❌ Performance - {page} - ERROR: {e}")
                    self.test_results.append({
                        "test": f"Performance - {page}",
                        "status": "FAIL",
                        "message": str(e)
                    })
            
        except Exception as e:
            print(f"❌ Error testing performance: {e}")
            self.test_results.append({
                "test": "Performance",
                "status": "FAIL",
                "message": str(e)
            })
    
    def run_all_tests(self):
        """Run all tests"""
        print("🎯 Starting web interface automated tests...")
        print("=" * 60)
        
        # Start web interface
        if not self.start_web_interface():
            print("❌ Failed to start web interface")
            return False
        
        # Run tests
        self.test_home_page()
        self.test_api_endpoints()
        self.test_ui_elements()
        self.test_navigation()
        self.test_responsiveness()
        self.test_performance()
        
        # Generate report
        self.generate_report()
        
        return True
    
    def generate_report(self):
        """Generate test report"""
        print("\n📊 Test Report")
        print("=" * 60)
        
        # Count results
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARNING"])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Warnings: {warning_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Print detailed results
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
            print(f"{status_icon} {result['test']}: {result['message']}")
        
        # Save report to file
        report_file = project_root / "test_reports" / "web_interface_test_report.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "warning_tests": warning_tests,
                "success_rate": (passed_tests/total_tests)*100,
                "results": self.test_results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Close web interface
        self.cleanup()
        
        return passed_tests == total_tests
    
    def cleanup(self):
        """Clean up resources"""
        print("\n🧹 Cleaning up...")
        
        if hasattr(self, 'web_process'):
            try:
                self.web_process.terminate()
                self.web_process.wait(timeout=5)
                print("✅ Web interface stopped")
            except:
                print("⚠️ Could not stop web interface gracefully")
        
        if self.driver:
            self.driver.quit()
            print("✅ WebDriver closed")

def main():
    """Main test function"""
    print("🚀 LLM Advanced Testing Suite - Web Interface Automated Tests")
    print("=" * 70)
    print()
    
    tester = WebInterfaceTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()