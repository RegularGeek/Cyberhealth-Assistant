
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Any

# Import our modules
from config import Config
from database import CyberHealthDB
from ai_analyzer import AIAnalyzer
from report_generator import ReportGenerator
from utils import run_health_checks

# Import tool integrations
from integrations.splunk import SplunkClient
from integrations.checkpoint import CheckpointClient
from integrations.crowdstrike import CrowdStrikeClient
from integrations.tenable import TenableClient

# Page configuration
st.set_page_config(
    page_title="🔐 CyberHealth Assistant",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def init_components():
    """Initialize database and AI components"""
    db = CyberHealthDB()
    ai_analyzer = AIAnalyzer()
    report_generator = ReportGenerator()
    return db, ai_analyzer, report_generator

db, ai_analyzer, report_generator = init_components()

# Sidebar navigation
st.sidebar.title("🔐 CyberHealth Assistant")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Navigation",
    ["📊 Dashboard", "🔍 Log Analysis", "🛠️ Tool Health Checks", "📈 Trends", "📋 Reports", "⚙️ Settings"]
)

# Main dashboard
if page == "📊 Dashboard":
    st.title("🔐 Cybersecurity Health Dashboard")
    st.markdown("Real-time monitoring of your cybersecurity infrastructure")
    
    # Get recent data
    risk_summary = db.get_risk_summary()
    recent_checks = db.get_recent_health_checks()
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Critical Issues",
            value=risk_summary["critical_issues"],
            delta=0
        )
    
    with col2:
        st.metric(
            label="Avg Risk Score",
            value=f"{risk_summary['average_risk_score']}/10",
            delta=0
        )
    
    with col3:
        st.metric(
            label="Tools Monitored",
            value=len(recent_checks) if recent_checks else 0,
            delta=0
        )
    
    with col4:
        st.metric(
            label="Assessment Period",
            value=f"{risk_summary['period_days']} days",
            delta=0
        )
    
    # Create charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Health Status")
        if recent_checks:
            df = pd.DataFrame(recent_checks)
            status_counts = df['status'].value_counts()
            
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Health Status Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No recent health check data available")
    
    with col2:
        st.subheader("Risk Score Trend")
        risk_trends = db.get_trends("risk_score", 7)
        if risk_trends:
            df = pd.DataFrame(risk_trends)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            fig = px.line(
                df, x='timestamp', y='metric_value',
                title="Risk Score Over Time"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trend data available")
    
    # Recent alerts
    st.subheader("Recent Alerts")
    if recent_checks:
        alerts_df = pd.DataFrame(recent_checks)
        alerts_df = alerts_df[alerts_df['severity'].isin(['CRITICAL', 'HIGH'])]
        
        if not alerts_df.empty:
            for _, alert in alerts_df.head(5).iterrows():
                severity_color = "🔴" if alert['severity'] == 'CRITICAL' else "🟡"
                st.markdown(f"{severity_color} **{alert['tool_name']}** - {alert['details']}")
        else:
            st.success("No critical alerts in the last 24 hours")
    else:
        st.info("No recent alerts to display")

# Log Analysis page
elif page == "🔍 Log Analysis":
    st.title("🔍 Log Analysis")
    st.markdown("Upload logs for AI-powered security analysis")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload log file",
        type=["txt", "log", "csv"],
        help="Upload firewall, system, or security logs for analysis"
    )
    
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        
        # Basic health checks
        basic_issues = run_health_checks(content)
        
        # AI analysis
        with st.spinner("Analyzing logs with AI..."):
            ai_analysis = ai_analyzer.analyze_logs(content, uploaded_file.name)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔍 AI Analysis Results")
            
            # Risk score
            risk_score = ai_analysis.get('risk_score', 0)
            risk_color = "green" if risk_score <= 3 else "orange" if risk_score <= 6 else "red"
            st.markdown(f"**Risk Score:** <span style='color: {risk_color}'>{risk_score}/10</span>", unsafe_allow_html=True)
            
            # Health status
            health_status = ai_analysis.get('health_status', 'UNKNOWN')
            status_emoji = "🟢" if health_status == 'HEALTHY' else "🟡" if health_status == 'WARNING' else "🔴"
            st.markdown(f"**Health Status:** {status_emoji} {health_status}")
            
            # Issues found
            st.subheader("Issues Found")
            issues = ai_analysis.get('issues', [])
            for issue in issues:
                st.markdown(f"• {issue}")
            
            # Store in database
            db.store_log_analysis(
                log_source=uploaded_file.name,
                analysis_type="file_upload",
                findings=str(issues),
                ai_summary=ai_analysis.get('summary', ''),
                risk_score=risk_score,
                recommendations=str(ai_analysis.get('recommendations', []))
            )
        
        with col2:
            st.subheader("📊 Severity Breakdown")
            severity_counts = ai_analysis.get('severity_counts', {})
            
            if severity_counts:
                fig = px.bar(
                    x=list(severity_counts.keys()),
                    y=list(severity_counts.values()),
                    title="Issues by Severity"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("💡 AI Recommendations")
            recommendations = ai_analysis.get('recommendations', [])
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")

# Tool Health Checks page
elif page == "🛠️ Tool Health Checks":
    st.title("🛠️ Tool Health Checks")
    st.markdown("Monitor the health of your cybersecurity tools")
    
    # Tool selection
    tools = {
        "Splunk": "SIEM and Log Management",
        "Checkpoint": "Firewall and Network Security",
        "CrowdStrike": "Endpoint Detection and Response",
        "Tenable": "Vulnerability Management"
    }
    
    selected_tools = st.multiselect(
        "Select tools to check",
        options=list(tools.keys()),
        default=["Splunk"],
        help="Choose which cybersecurity tools to perform health checks on"
    )
    
    if st.button("🔍 Run Health Checks", type="primary"):
        if not selected_tools:
            st.warning("Please select at least one tool to check")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            all_results = {}
            
            for i, tool in enumerate(selected_tools):
                status_text.text(f"Checking {tool}...")
                progress_bar.progress((i + 1) / len(selected_tools))
                
                try:
                    if tool == "Splunk":
                        client = SplunkClient(
                            Config.SPLUNK_CONFIG["base_url"],
                            Config.SPLUNK_CONFIG["username"],
                            Config.SPLUNK_CONFIG["password"]
                        )
                        # For demo, create mock results
                        results = {
                            "tool_name": "Splunk",
                            "overall_status": "HEALTHY",
                            "summary": "Splunk is running normally",
                            "timestamp": datetime.now().isoformat(),
                            "checks": {
                                "system_status": {"status": "HEALTHY", "details": "System operational"},
                                "index_health": {"status": "HEALTHY", "details": "All indexes healthy"},
                                "search_performance": {"status": "HEALTHY", "details": "Search performance normal"}
                            }
                        }
                    
                    elif tool == "Checkpoint":
                        client = CheckpointClient()
                        results = client.run_health_checks()
                    
                    elif tool == "CrowdStrike":
                        client = CrowdStrikeClient()
                        results = client.run_health_checks()
                    
                    elif tool == "Tenable":
                        client = TenableClient()
                        results = client.run_health_checks()
                    
                    all_results[tool] = results
                    
                    # Store in database
                    for check_name, check_result in results.get('checks', {}).items():
                        db.store_health_check(
                            tool_name=tool,
                            check_type=check_name,
                            status=check_result.get('status', 'UNKNOWN'),
                            severity=check_result.get('status', 'UNKNOWN'),
                            details=str(check_result.get('details', '')),
                            raw_data=check_result
                        )
                    
                except Exception as e:
                    st.error(f"Error checking {tool}: {str(e)}")
                    all_results[tool] = {
                        "tool_name": tool,
                        "overall_status": "CRITICAL",
                        "summary": f"Connection failed: {str(e)}",
                        "timestamp": datetime.now().isoformat(),
                        "checks": {}
                    }
            
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            st.subheader("📊 Health Check Results")
            
            for tool, results in all_results.items():
                status = results.get('overall_status', 'UNKNOWN')
                status_emoji = "🟢" if status == 'HEALTHY' else "🟡" if status == 'WARNING' else "🔴"
                
                with st.expander(f"{status_emoji} {tool} - {status}"):
                    st.markdown(f"**Summary:** {results.get('summary', 'No summary available')}")
                    st.markdown(f"**Timestamp:** {results.get('timestamp', 'Unknown')}")
                    
                    checks = results.get('checks', {})
                    if checks:
                        st.subheader("Detailed Checks")
                        for check_name, check_result in checks.items():
                            check_status = check_result.get('status', 'UNKNOWN')
                            check_emoji = "🟢" if check_status == 'HEALTHY' else "🟡" if check_status == 'WARNING' else "🔴"
                            st.markdown(f"{check_emoji} **{check_name.replace('_', ' ').title()}:** {check_status}")
                            if check_result.get('details'):
                                st.markdown(f"   Details: {check_result['details']}")

# Trends page
elif page == "📈 Trends":
    st.title("📈 Security Trends")
    st.markdown("Analyze trends and patterns in your security data")
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        days = st.selectbox("Analysis Period", [7, 30, 90], index=0)
    with col2:
        metric = st.selectbox("Metric to Analyze", ["risk_score", "critical_issues", "warning_issues"])
    
    # Get trend data
    trends = db.get_trends(metric, days)
    
    if trends:
        df = pd.DataFrame(trends)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create trend chart
        fig = px.line(
            df, x='timestamp', y='metric_value',
            title=f"{metric.replace('_', ' ').title()} Over {days} Days"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # AI trend analysis
        with st.spinner("Analyzing trends with AI..."):
            trend_analysis = ai_analyzer.analyze_trends(trends)
        
        st.subheader("🤖 AI Trend Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Key Trends:**")
            trends_list = trend_analysis.get('trends', [])
            for trend in trends_list:
                st.markdown(f"• {trend}")
        
        with col2:
            st.markdown("**Risk Trajectory:**")
            trajectory = trend_analysis.get('risk_trajectory', 'stable')
            trajectory_emoji = "📈" if trajectory == "deteriorating" else "📉" if trajectory == "improving" else "➡️"
            st.markdown(f"{trajectory_emoji} {trajectory.title()}")
        
        st.markdown("**Recommendations:**")
        recommendations = trend_analysis.get('recommendations', [])
        for rec in recommendations:
            st.markdown(f"• {rec}")
    else:
        st.info("No trend data available for the selected period")

# Reports page
elif page == "📋 Reports":
    st.title("📋 Generate Reports")
    st.markdown("Create comprehensive cybersecurity health reports")
    
    # Report options
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Report Type",
            ["Comprehensive Health Report", "Executive Summary", "Technical Details", "Trend Analysis"]
        )
    
    with col2:
        include_ai = st.checkbox("Include AI Analysis", value=True)
    
    # Date range for report
    report_days = st.slider("Report Period (days)", 1, 90, 7)
    
    if st.button("📄 Generate Report", type="primary"):
        with st.spinner("Generating report..."):
            # Get data for report
            recent_checks = db.get_recent_health_checks(hours=report_days * 24)
            risk_summary = db.get_risk_summary(report_days)
            
            # Create report data structure
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "report_type": report_type,
                "period_days": report_days,
                "overall_status": "HEALTHY" if risk_summary["critical_issues"] == 0 else "WARNING" if risk_summary["critical_issues"] < 3 else "CRITICAL",
                "tool_results": {},
                "risk_summary": risk_summary,
                "recent_checks": recent_checks
            }
            
            # Add AI analysis if requested
            if include_ai:
                # Get recent log analysis for AI insights
                # This would normally come from actual log analysis data
                ai_insights = ai_analyzer.generate_health_report(report_data)
                report_data["ai_analysis"] = ai_insights
                report_data["ai_recommendations"] = [
                    "Implement additional monitoring for detected patterns",
                    "Review and update security policies",
                    "Schedule regular security assessments"
                ]
            
            # Generate PDF
            try:
                pdf_path = report_generator.generate_health_report(report_data)
                
                # Store report in database
                db.store_report(
                    report_type=report_type,
                    report_data=report_data,
                    file_path=pdf_path,
                    generated_by="CyberHealth Assistant"
                )
                
                st.success("✅ Report generated successfully!")
                
                # Provide download link
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=file.read(),
                        file_name=f"cyberhealth_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                
                # Show report preview
                st.subheader("📋 Report Preview")
                st.json(report_data)
                
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")

# Settings page
elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.markdown("Configure CyberHealth Assistant")
    
    # Configuration sections
    tab1, tab2, tab3 = st.tabs(["🔑 API Keys", "🛠️ Tool Configuration", "📊 Database"])
    
    with tab1:
        st.subheader("API Configuration")
        
        openai_key = st.text_input(
            "OpenAI API Key",
            value=Config.OPENAI_API_KEY,
            type="password",
            help="Enter your OpenAI API key for AI-powered analysis"
        )
        
        if st.button("Save API Keys"):
            # In a real application, you'd save this to a secure configuration
            st.success("API keys saved (demo mode)")
    
    with tab2:
        st.subheader("Tool Configuration")
        
        # Splunk settings
        with st.expander("Splunk Configuration"):
            splunk_url = st.text_input("Splunk Base URL", value=Config.SPLUNK_CONFIG["base_url"])
            splunk_user = st.text_input("Username", value=Config.SPLUNK_CONFIG["username"])
            splunk_pass = st.text_input("Password", value=Config.SPLUNK_CONFIG["password"], type="password")
        
        # Checkpoint settings
        with st.expander("Checkpoint Configuration"):
            checkpoint_url = st.text_input("Checkpoint Base URL", value=Config.CHECKPOINT_CONFIG["base_url"])
            checkpoint_user = st.text_input("Username", value=Config.CHECKPOINT_CONFIG["username"])
            checkpoint_pass = st.text_input("Password", value=Config.CHECKPOINT_CONFIG["password"], type="password")
        
        if st.button("Save Tool Configuration"):
            st.success("Tool configuration saved (demo mode)")
    
    with tab3:
        st.subheader("Database Information")
        
        # Database stats
        recent_checks = db.get_recent_health_checks()
        st.metric("Recent Health Checks", len(recent_checks))
        
        if st.button("Clear Database"):
            st.warning("This will clear all stored data. Are you sure?")
            # In a real application, you'd implement database clearing
            st.info("Database clearing not implemented in demo mode")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        🔐 CyberHealth Assistant v1.0 | Built for enterprise cybersecurity monitoring
    </div>
    """,
    unsafe_allow_html=True
)
