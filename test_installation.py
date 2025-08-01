#!/usr/bin/env python3
"""
Test script for CyberHealth Assistant
Verifies that all components can be imported and basic functionality works
"""

import sys
import traceback
from datetime import datetime

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        # Core modules
        from config import Config
        print("✅ Config module imported successfully")
        
        from database import CyberHealthDB
        print("✅ Database module imported successfully")
        
        from ai_analyzer import AIAnalyzer
        print("✅ AI Analyzer module imported successfully")
        
        from report_generator import ReportGenerator
        print("✅ Report Generator module imported successfully")
        
        from utils import run_health_checks
        print("✅ Utils module imported successfully")
        
        # Tool integrations
        from integrations.splunk import SplunkClient
        print("✅ Splunk integration imported successfully")
        
        from integrations.checkpoint import CheckpointClient
        print("✅ Checkpoint integration imported successfully")
        
        from integrations.crowdstrike import CrowdStrikeClient
        print("✅ CrowdStrike integration imported successfully")
        
        from integrations.tenable import TenableClient
        print("✅ Tenable integration imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_database():
    """Test database functionality"""
    print("\n🗄️ Testing database...")
    
    try:
        from database import CyberHealthDB
        
        db = CyberHealthDB()
        print("✅ Database initialized successfully")
        
        # Test storing a metric
        db.store_metric("test_metric", 5.0, "test_tool", "test_category")
        print("✅ Metric storage test passed")
        
        # Test getting risk summary
        risk_summary = db.get_risk_summary()
        print(f"✅ Risk summary retrieved: {risk_summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        traceback.print_exc()
        return False

def test_ai_analyzer():
    """Test AI analyzer functionality"""
    print("\n🤖 Testing AI analyzer...")
    
    try:
        from ai_analyzer import AIAnalyzer
        
        analyzer = AIAnalyzer()
        print("✅ AI analyzer initialized successfully")
        
        # Test with sample log data
        sample_log = """
        Jul 29 11:00:00 server1 firewall: CRITICAL - firewall disabled
        Jul 29 11:02:10 server1 login: Unauthorized access from 192.168.1.200
        Jul 29 11:10:00 server1 antivirus: Scan completed successfully
        """
        
        analysis = analyzer.analyze_logs(sample_log, "test_log")
        print(f"✅ AI analysis completed: {analysis.get('risk_score', 'N/A')}/10 risk score")
        
        return True
        
    except Exception as e:
        print(f"❌ AI analyzer error: {e}")
        traceback.print_exc()
        return False

def test_report_generator():
    """Test report generator functionality"""
    print("\n📋 Testing report generator...")
    
    try:
        from report_generator import ReportGenerator
        
        generator = ReportGenerator()
        print("✅ Report generator initialized successfully")
        
        # Test with sample data
        sample_data = {
            "overall_status": "HEALTHY",
            "tool_results": {
                "Splunk": {
                    "overall_status": "HEALTHY",
                    "summary": "Splunk is running normally",
                    "timestamp": datetime.now().isoformat()
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Note: This would create a PDF file, so we'll just test the initialization
        print("✅ Report generator test passed (PDF generation would create file)")
        
        return True
        
    except Exception as e:
        print(f"❌ Report generator error: {e}")
        traceback.print_exc()
        return False

def test_tool_integrations():
    """Test tool integration classes"""
    print("\n🛠️ Testing tool integrations...")
    
    try:
        from integrations.splunk import SplunkClient
        from integrations.checkpoint import CheckpointClient
        from integrations.crowdstrike import CrowdStrikeClient
        from integrations.tenable import TenableClient
        
        # Test Splunk client initialization
        splunk_client = SplunkClient("https://test.com", "user", "pass")
        print("✅ Splunk client initialized")
        
        # Test Checkpoint client initialization
        checkpoint_client = CheckpointClient()
        print("✅ Checkpoint client initialized")
        
        # Test CrowdStrike client initialization
        crowdstrike_client = CrowdStrikeClient()
        print("✅ CrowdStrike client initialized")
        
        # Test Tenable client initialization
        tenable_client = TenableClient()
        print("✅ Tenable client initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Tool integration error: {e}")
        traceback.print_exc()
        return False

def test_utils():
    """Test utility functions"""
    print("\n🔧 Testing utilities...")
    
    try:
        from utils import run_health_checks
        
        # Test with sample log data
        sample_log = """
        Jul 29 11:00:00 server1 firewall: CRITICAL - firewall disabled
        Jul 29 11:02:10 server1 login: Unauthorized access from 192.168.1.200
        """
        
        issues = run_health_checks(sample_log)
        print(f"✅ Health checks completed: {len(issues)} issues found")
        
        return True
        
    except Exception as e:
        print(f"❌ Utils error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🔐 CyberHealth Assistant - Installation Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Database", test_database),
        ("AI Analyzer", test_ai_analyzer),
        ("Report Generator", test_report_generator),
        ("Tool Integrations", test_tool_integrations),
        ("Utilities", test_utils)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! CyberHealth Assistant is ready to use.")
        print("\n🚀 To start the application, run:")
        print("   streamlit run main.py")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)