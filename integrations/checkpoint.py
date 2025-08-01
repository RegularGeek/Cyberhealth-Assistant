import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from config import Config

class CheckpointClient:
    """Checkpoint Firewall integration for health checks"""
    
    def __init__(self, base_url: str = None, username: str = None, password: str = None, api_key: str = None):
        config = Config.CHECKPOINT_CONFIG
        self.base_url = base_url or config["base_url"]
        self.username = username or config["username"]
        self.password = password or config["password"]
        self.api_key = api_key or config["api_key"]
        self.session = requests.Session()
        self.session.verify = False  # For testing, set to True in production
        
        # Don't authenticate during initialization to avoid connection errors in tests
        if self.api_key:
            self.session.headers.update({"X-chkp-sid": self.api_key})
    
    def _authenticate(self):
        """Authenticate with Checkpoint API"""
        auth_url = f"{self.base_url}/web_api/login"
        auth_data = {
            "user": self.username,
            "password": self.password
        }
        
        response = self.session.post(auth_url, json=auth_data)
        response.raise_for_status()
        
        # Extract session ID
        session_data = response.json()
        if "sid" in session_data:
            self.session.headers.update({"X-chkp-sid": session_data["sid"]})
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system health status"""
        try:
            url = f"{self.base_url}/web_api/show-system-status"
            response = self.session.post(url, json={})
            response.raise_for_status()
            
            status_data = response.json()
            return {
                "status": "HEALTHY" if status_data.get("status") == "OK" else "WARNING",
                "details": status_data,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "CRITICAL",
                "details": f"Connection failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_firewall_status(self) -> Dict[str, Any]:
        """Get firewall policy and rule status"""
        try:
            url = f"{self.base_url}/web_api/show-packages"
            response = self.session.post(url, json={})
            response.raise_for_status()
            
            packages = response.json().get("packages", [])
            active_packages = [p for p in packages if p.get("installation-targets")]
            
            return {
                "status": "HEALTHY" if active_packages else "WARNING",
                "active_packages": len(active_packages),
                "total_packages": len(packages),
                "details": packages,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "CRITICAL",
                "details": f"Failed to get firewall status: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_threat_prevention_status(self) -> Dict[str, Any]:
        """Get threat prevention and IPS status"""
        try:
            url = f"{self.base_url}/web_api/show-threat-prevention"
            response = self.session.post(url, json={})
            response.raise_for_status()
            
            tp_data = response.json()
            return {
                "status": "HEALTHY",
                "threat_prevention_enabled": tp_data.get("threat-prevention", {}).get("enabled", False),
                "ips_enabled": tp_data.get("ips", {}).get("enabled", False),
                "details": tp_data,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "WARNING",
                "details": f"Failed to get threat prevention status: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_logs(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent firewall logs"""
        try:
            url = f"{self.base_url}/web_api/show-logs"
            log_data = {
                "limit": 1000,
                "query": f"time_range: {hours}h"
            }
            
            response = self.session.post(url, json=log_data)
            response.raise_for_status()
            
            logs = response.json().get("logs", [])
            return logs
            
        except Exception as e:
            print(f"Failed to get logs: {e}")
            return []
    
    def run_health_checks(self) -> Dict[str, Any]:
        """Run comprehensive health checks"""
        results = {
            "tool_name": "Checkpoint Firewall",
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # System status check
        results["checks"]["system_status"] = self.get_system_status()
        
        # Firewall status check
        results["checks"]["firewall_status"] = self.get_firewall_status()
        
        # Threat prevention check
        results["checks"]["threat_prevention"] = self.get_threat_prevention_status()
        
        # Overall health assessment
        critical_count = sum(1 for check in results["checks"].values() 
                           if check["status"] == "CRITICAL")
        warning_count = sum(1 for check in results["checks"].values() 
                           if check["status"] == "WARNING")
        
        if critical_count > 0:
            overall_status = "CRITICAL"
        elif warning_count > 0:
            overall_status = "WARNING"
        else:
            overall_status = "HEALTHY"
        
        results["overall_status"] = overall_status
        results["summary"] = f"Checkpoint health check completed: {overall_status} status with {critical_count} critical and {warning_count} warning issues"
        
        return results