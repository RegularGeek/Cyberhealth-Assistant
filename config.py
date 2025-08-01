import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management for CyberHealth Assistant"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Database Configuration
    DATABASE_PATH = os.getenv("DATABASE_PATH", "cyberhealth.db")
    
    # Splunk Configuration
    SPLUNK_CONFIG = {
        "base_url": os.getenv("SPLUNK_BASE_URL", "https://splunk.company.com:8089"),
        "username": os.getenv("SPLUNK_USERNAME", "admin"),
        "password": os.getenv("SPLUNK_PASSWORD", ""),
        "verify_ssl": os.getenv("SPLUNK_VERIFY_SSL", "False").lower() == "true"
    }
    
    # Checkpoint Configuration
    CHECKPOINT_CONFIG = {
        "base_url": os.getenv("CHECKPOINT_BASE_URL", "https://checkpoint.company.com"),
        "username": os.getenv("CHECKPOINT_USERNAME", "admin"),
        "password": os.getenv("CHECKPOINT_PASSWORD", ""),
        "api_key": os.getenv("CHECKPOINT_API_KEY", "")
    }
    
    # Palo Alto Configuration
    PALO_ALTO_CONFIG = {
        "base_url": os.getenv("PALO_ALTO_BASE_URL", "https://paloalto.company.com"),
        "username": os.getenv("PALO_ALTO_USERNAME", "admin"),
        "password": os.getenv("PALO_ALTO_PASSWORD", ""),
        "api_key": os.getenv("PALO_ALTO_API_KEY", "")
    }
    
    # CrowdStrike Configuration
    CROWDSTRIKE_CONFIG = {
        "base_url": os.getenv("CROWDSTRIKE_BASE_URL", "https://api.crowdstrike.com"),
        "client_id": os.getenv("CROWDSTRIKE_CLIENT_ID", ""),
        "client_secret": os.getenv("CROWDSTRIKE_CLIENT_SECRET", "")
    }
    
    # Imperva Configuration
    IMPERVA_CONFIG = {
        "base_url": os.getenv("IMPERVA_BASE_URL", "https://imperva.company.com"),
        "username": os.getenv("IMPERVA_USERNAME", "admin"),
        "password": os.getenv("IMPERVA_PASSWORD", ""),
        "api_key": os.getenv("IMPERVA_API_KEY", "")
    }
    
    # Tenable Configuration
    TENABLE_CONFIG = {
        "base_url": os.getenv("TENABLE_BASE_URL", "https://cloud.tenable.com"),
        "access_key": os.getenv("TENABLE_ACCESS_KEY", ""),
        "secret_key": os.getenv("TENABLE_SECRET_KEY", "")
    }
    
    # Health Check Thresholds
    THRESHOLDS = {
        "critical_errors": 5,
        "failed_logins": 10,
        "firewall_alerts": 3,
        "vulnerability_high": 2,
        "vulnerability_critical": 1
    }
    
    # Report Configuration
    REPORT_CONFIG = {
        "company_name": os.getenv("COMPANY_NAME", "Your Company"),
        "logo_path": os.getenv("LOGO_PATH", ""),
        "report_title": "Cybersecurity Health Report",
        "include_trends": True,
        "include_recommendations": True
    }