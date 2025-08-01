import openai
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from config import Config

class AIAnalyzer:
    """AI-powered log analysis and health assessment"""
    
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
    
    def analyze_logs(self, log_data: str, log_source: str = "unknown") -> Dict[str, Any]:
        """Analyze log data using AI and return insights"""
        
        if not Config.OPENAI_API_KEY:
            return self._fallback_analysis(log_data)
        
        try:
            prompt = f"""
            Analyze the following cybersecurity log data and provide a comprehensive assessment.
            
            Log Source: {log_source}
            Log Data:
            {log_data}
            
            Please provide:
            1. Security issues found (CRITICAL, HIGH, MEDIUM, LOW)
            2. Risk score (1-10, where 10 is highest risk)
            3. Summary of findings
            4. Specific recommendations
            5. Health status (HEALTHY, WARNING, CRITICAL)
            
            Format your response as JSON with these keys:
            - issues: list of security issues
            - risk_score: integer 1-10
            - summary: string summary
            - recommendations: list of recommendations
            - health_status: string
            - severity_counts: dict with counts for each severity level
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert analyzing log data for security issues and health assessment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return self._fallback_analysis(log_data)
    
    def _fallback_analysis(self, log_data: str) -> Dict[str, Any]:
        """Fallback analysis when AI is not available"""
        issues = []
        risk_score = 5
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        # Basic pattern matching
        log_lower = log_data.lower()
        
        if "critical" in log_lower:
            issues.append("Critical errors detected in logs")
            severity_counts["CRITICAL"] += 1
            risk_score = 8
        
        if "unauthorized" in log_lower or "failed login" in log_lower:
            issues.append("Unauthorized access attempts detected")
            severity_counts["HIGH"] += 1
            risk_score = max(risk_score, 7)
        
        if "firewall disabled" in log_lower:
            issues.append("Firewall appears to be disabled")
            severity_counts["CRITICAL"] += 1
            risk_score = 9
        
        if "malware" in log_lower or "virus" in log_lower:
            issues.append("Malware/virus activity detected")
            severity_counts["HIGH"] += 1
            risk_score = max(risk_score, 8)
        
        if not issues:
            issues.append("No critical security issues found")
            severity_counts["LOW"] += 1
            risk_score = 2
        
        health_status = "HEALTHY" if risk_score <= 3 else "WARNING" if risk_score <= 6 else "CRITICAL"
        
        return {
            "issues": issues,
            "risk_score": risk_score,
            "summary": f"Analysis found {len(issues)} security issues with risk score {risk_score}/10",
            "recommendations": [
                "Review and address critical issues immediately",
                "Implement additional monitoring for detected patterns",
                "Consider security training for staff"
            ],
            "health_status": health_status,
            "severity_counts": severity_counts
        }
    
    def generate_health_report(self, tool_results: Dict[str, Any]) -> str:
        """Generate a comprehensive health report using AI"""
        
        if not Config.OPENAI_API_KEY:
            return self._generate_fallback_report(tool_results)
        
        try:
            prompt = f"""
            Generate a professional cybersecurity health report based on the following tool analysis results:
            
            {json.dumps(tool_results, indent=2)}
            
            Please create a comprehensive report that includes:
            1. Executive Summary
            2. Overall Health Status
            3. Critical Issues (if any)
            4. Recommendations
            5. Next Steps
            
            Format the report in a professional, executive-friendly manner.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity consultant creating executive health reports."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"AI report generation failed: {e}")
            return self._generate_fallback_report(tool_results)
    
    def _generate_fallback_report(self, tool_results: Dict[str, Any]) -> str:
        """Generate a fallback report when AI is not available"""
        
        report = f"""
# Cybersecurity Health Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
This report provides an overview of the cybersecurity health status across all monitored tools and systems.

## Overall Health Status
Based on the analysis of {len(tool_results)} tools and systems.

## Critical Issues
"""
        
        critical_issues = []
        for tool, results in tool_results.items():
            if results.get('health_status') == 'CRITICAL':
                critical_issues.append(f"- {tool}: {results.get('summary', 'Critical issues detected')}")
        
        if critical_issues:
            report += "\n".join(critical_issues)
        else:
            report += "No critical issues detected at this time."
        
        report += """

## Recommendations
1. Address any critical issues immediately
2. Review and update security policies
3. Implement additional monitoring where needed
4. Schedule regular security assessments

## Next Steps
- Review this report with the security team
- Prioritize critical issues for immediate action
- Schedule follow-up assessments
"""
        
        return report
    
    def analyze_trends(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """Analyze trends in historical data using AI"""
        
        if not Config.OPENAI_API_KEY:
            return self._fallback_trend_analysis(historical_data)
        
        try:
            prompt = f"""
            Analyze the following historical cybersecurity data and identify trends:
            
            {json.dumps(historical_data, indent=2)}
            
            Please provide:
            1. Key trends identified
            2. Risk trajectory (improving, stable, deteriorating)
            3. Seasonal patterns (if any)
            4. Recommendations based on trends
            
            Format as JSON with keys: trends, risk_trajectory, patterns, recommendations
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity analyst identifying trends in security data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"AI trend analysis failed: {e}")
            return self._fallback_trend_analysis(historical_data)
    
    def _fallback_trend_analysis(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """Fallback trend analysis"""
        return {
            "trends": ["Insufficient data for trend analysis"],
            "risk_trajectory": "stable",
            "patterns": [],
            "recommendations": ["Collect more historical data for better trend analysis"]
        }