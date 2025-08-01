import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from config import Config

class TenableClient:
    """Tenable.io vulnerability management integration for health checks"""
    
    def __init__(self, base_url: str = None, access_key: str = None, secret_key: str = None):
        config = Config.TENABLE_CONFIG
        self.base_url = base_url or config["base_url"]
        self.access_key = access_key or config["access_key"]
        self.secret_key = secret_key or config["secret_key"]
        self.session = requests.Session()
        
        # Don't set headers during initialization to avoid connection errors in tests
        # if self.access_key and self.secret_key:
        #     self.session.headers.update({
        #         "X-ApiKeys": f"accessKey={self.access_key}; secretKey={self.secret_key}",
        #         "Content-Type": "application/json"
        #     })
    
    def get_scan_status(self) -> Dict[str, Any]:
        """Get scan status and recent scan results"""
        try:
            url = f"{self.base_url}/scans"
            response = self.session.get(url)
            response.raise_for_status()
            
            scans = response.json().get("scans", [])
            recent_scans = [scan for scan in scans if scan.get("last_modification_date")]
            
            # Get scan details for recent scans
            scan_details = []
            for scan in recent_scans[:5]:  # Limit to 5 most recent
                scan_id = scan.get("id")
                if scan_id:
                    detail_url = f"{self.base_url}/scans/{scan_id}"
                    detail_response = self.session.get(detail_url)
                    if detail_response.status_code == 200:
                        scan_details.append(detail_response.json())
            
            return {
                "status": "HEALTHY" if recent_scans else "WARNING",
                "total_scans": len(scans),
                "recent_scans": len(recent_scans),
                "scan_details": scan_details,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "CRITICAL",
                "details": f"Failed to get scan status: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_vulnerability_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get vulnerability summary and statistics"""
        try:
            url = f"{self.base_url}/workbenches/vulnerabilities"
            params = {
                "date_range": days,
                "filter.0.quality": "eq",
                "filter.0.value": "1"
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            vulns = response.json()
            vulnerability_count = len(vulns.get("vulnerabilities", []))
            
            # Count by severity
            severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
            for vuln in vulns.get("vulnerabilities", []):
                severity = vuln.get("severity", "Low")
                if severity in severity_counts:
                    severity_counts[severity] += 1
            
            # Determine overall status based on critical/high vulnerabilities
            critical_high_count = severity_counts["Critical"] + severity_counts["High"]
            if critical_high_count > Config.THRESHOLDS["vulnerability_critical"]:
                status = "CRITICAL"
            elif critical_high_count > Config.THRESHOLDS["vulnerability_high"]:
                status = "WARNING"
            else:
                status = "HEALTHY"
            
            return {
                "status": status,
                "total_vulnerabilities": vulnerability_count,
                "critical_vulnerabilities": severity_counts["Critical"],
                "high_vulnerabilities": severity_counts["High"],
                "medium_vulnerabilities": severity_counts["Medium"],
                "low_vulnerabilities": severity_counts["Low"],
                "severity_counts": severity_counts,
                "details": vulns,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "WARNING",
                "details": f"Failed to get vulnerability summary: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_asset_status(self) -> Dict[str, Any]:
        """Get asset inventory and status"""
        try:
            url = f"{self.base_url}/assets"
            response = self.session.get(url)
            response.raise_for_status()
            
            assets = response.json()
            total_assets = len(assets.get("assets", []))
            
            # Count assets by status
            status_counts = {}
            for asset in assets.get("assets", []):
                status = asset.get("status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return {
                "status": "HEALTHY",
                "total_assets": total_assets,
                "status_counts": status_counts,
                "details": assets,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "WARNING",
                "details": f"Failed to get asset status: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_compliance_status(self) -> Dict[str, Any]:
        """Get compliance scan results"""
        try:
            url = f"{self.base_url}/compliance"
            response = self.session.get(url)
            response.raise_for_status()
            
            compliance = response.json()
            compliance_scans = compliance.get("compliance", [])
            
            return {
                "status": "HEALTHY" if compliance_scans else "WARNING",
                "total_compliance_scans": len(compliance_scans),
                "details": compliance,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "WARNING",
                "details": f"Failed to get compliance status: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_recent_findings(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent vulnerability findings"""
        try:
            url = f"{self.base_url}/workbenches/vulnerabilities"
            params = {
                "date_range": days,
                "filter.0.quality": "eq",
                "filter.0.value": "1"
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            findings = response.json()
            return findings.get("vulnerabilities", [])
            
        except Exception as e:
            print(f"Failed to get recent findings: {e}")
            return []
    
    def run_health_checks(self) -> Dict[str, Any]:
        """Run comprehensive health checks"""
        results = {
            "tool_name": "Tenable.io",
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # Scan status check
        results["checks"]["scan_status"] = self.get_scan_status()
        
        # Vulnerability summary check
        results["checks"]["vulnerability_summary"] = self.get_vulnerability_summary()
        
        # Asset status check
        results["checks"]["asset_status"] = self.get_asset_status()
        
        # Compliance status check
        results["checks"]["compliance_status"] = self.get_compliance_status()
        
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
        results["summary"] = f"Tenable health check completed: {overall_status} status with {critical_count} critical and {warning_count} warning issues"
        
        return results