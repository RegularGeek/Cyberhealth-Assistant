import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
from config import Config

class CyberHealthDB:
    """Database management for CyberHealth Assistant"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Health check results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    tool_name TEXT NOT NULL,
                    check_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    details TEXT,
                    raw_data TEXT
                )
            ''')
            
            # Log analysis results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS log_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    log_source TEXT NOT NULL,
                    analysis_type TEXT NOT NULL,
                    findings TEXT,
                    ai_summary TEXT,
                    risk_score INTEGER,
                    recommendations TEXT
                )
            ''')
            
            # Trends and metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metric_name TEXT NOT NULL,
                    metric_value REAL,
                    tool_name TEXT,
                    category TEXT
                )
            ''')
            
            # Reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    report_type TEXT NOT NULL,
                    report_data TEXT,
                    file_path TEXT,
                    generated_by TEXT
                )
            ''')
            
            conn.commit()
    
    def store_health_check(self, tool_name: str, check_type: str, status: str, 
                          severity: str, details: str = None, raw_data: Dict = None):
        """Store health check results"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO health_checks (tool_name, check_type, status, severity, details, raw_data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (tool_name, check_type, status, severity, details, 
                  json.dumps(raw_data) if raw_data else None))
            conn.commit()
    
    def store_log_analysis(self, log_source: str, analysis_type: str, findings: str,
                          ai_summary: str, risk_score: int, recommendations: str = None):
        """Store log analysis results"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO log_analysis (log_source, analysis_type, findings, ai_summary, risk_score, recommendations)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (log_source, analysis_type, findings, ai_summary, risk_score, recommendations))
            conn.commit()
    
    def store_metric(self, metric_name: str, metric_value: float, 
                    tool_name: str = None, category: str = None):
        """Store metrics and trends"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO metrics (metric_name, metric_value, tool_name, category)
                VALUES (?, ?, ?, ?)
            ''', (metric_name, metric_value, tool_name, category))
            conn.commit()
    
    def store_report(self, report_type: str, report_data: Dict, 
                    file_path: str = None, generated_by: str = "system"):
        """Store generated reports"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reports (report_type, report_data, file_path, generated_by)
                VALUES (?, ?, ?, ?)
            ''', (report_type, json.dumps(report_data), file_path, generated_by))
            conn.commit()
    
    def get_recent_health_checks(self, hours: int = 24, tool_name: str = None) -> List[Dict]:
        """Get recent health check results"""
        with sqlite3.connect(self.db_path) as conn:
            query = '''
                SELECT * FROM health_checks 
                WHERE timestamp >= datetime('now', '-{} hours')
            '''.format(hours)
            
            if tool_name:
                query += f" AND tool_name = '{tool_name}'"
            
            query += " ORDER BY timestamp DESC"
            
            df = pd.read_sql_query(query, conn)
            return df.to_dict('records')
    
    def get_trends(self, metric_name: str, days: int = 30) -> List[Dict]:
        """Get metric trends over time"""
        with sqlite3.connect(self.db_path) as conn:
            query = '''
                SELECT timestamp, metric_value FROM metrics 
                WHERE metric_name = ? AND timestamp >= datetime('now', '-{} days')
                ORDER BY timestamp
            '''.format(days)
            
            df = pd.read_sql_query(query, conn, params=(metric_name,))
            return df.to_dict('records')
    
    def get_risk_summary(self, days: int = 7) -> Dict:
        """Get risk summary for dashboard"""
        with sqlite3.connect(self.db_path) as conn:
            # Get critical issues count
            critical_query = '''
                SELECT COUNT(*) as critical_count FROM health_checks 
                WHERE severity = 'CRITICAL' AND timestamp >= datetime('now', '-{} days')
            '''.format(days)
            
            # Get average risk score
            risk_query = '''
                SELECT AVG(risk_score) as avg_risk FROM log_analysis 
                WHERE timestamp >= datetime('now', '-{} days')
            '''.format(days)
            
            cursor = conn.cursor()
            cursor.execute(critical_query)
            critical_count = cursor.fetchone()[0]
            
            cursor.execute(risk_query)
            avg_risk = cursor.fetchone()[0] or 0
            
            return {
                "critical_issues": critical_count,
                "average_risk_score": round(avg_risk, 2),
                "period_days": days
            }
    
    def get_tool_performance(self, tool_name: str, days: int = 30) -> Dict:
        """Get performance metrics for a specific tool"""
        with sqlite3.connect(self.db_path) as conn:
            query = '''
                SELECT 
                    check_type,
                    status,
                    COUNT(*) as count
                FROM health_checks 
                WHERE tool_name = ? AND timestamp >= datetime('now', '-{} days')
                GROUP BY check_type, status
            '''.format(days)
            
            df = pd.read_sql_query(query, conn, params=(tool_name,))
            return df.to_dict('records')