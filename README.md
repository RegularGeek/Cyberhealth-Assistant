# 🔐 CyberHealth Assistant

**AI-Powered Cybersecurity Health Check Assistant**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

**CyberHealth Assistant** is an AI-driven tool designed to **analyze logs**, **track cybersecurity solution performance**, and **generate detailed health reports** for enterprise environments. It assists cybersecurity professionals in continuously monitoring the health of deployed tools such as:

- **Splunk** (SIEM)
- **Checkpoint, Palo Alto, CrowdStrike** (EDR/NDR/Firewall)
- **Imperva** (WAF)
- **Tenable** (Vulnerability Management)

This project integrates AI via OpenAI's API and connects to cybersecurity tools via REST APIs and log files, offering automation and insights that would normally take hours of manual work.

## ✨ Key Features

### 🔍 **AI-Powered Log Analysis**
- Upload firewall, system, or security logs for instant analysis
- AI identifies security issues, risk scores, and provides recommendations
- Supports multiple log formats (txt, log, csv)

### 🛠️ **Multi-Tool Health Monitoring**
- **Splunk**: SIEM health checks, index status, search performance
- **Checkpoint**: Firewall status, threat prevention, system health
- **CrowdStrike**: EDR status, endpoint health, detection summary
- **Tenable**: Vulnerability management, scan status, asset inventory

### 📊 **Real-Time Dashboard**
- Live metrics and health status across all tools
- Interactive charts and trend analysis
- Risk score tracking and alerting

### 📋 **Professional PDF Reports**
- Executive summaries with AI-generated insights
- Technical details and recommendations
- Customizable report periods and types

### 🗄️ **Data Persistence**
- SQLite database for trend tracking
- Historical health check data
- Performance metrics and analytics

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional, for AI features)
- Access to cybersecurity tools (optional, for live monitoring)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cyberhealth-assistant.git
   cd cyberhealth-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and tool configurations
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📖 Usage Guide

### Dashboard
The main dashboard provides an overview of your cybersecurity infrastructure:
- **Metrics**: Critical issues, risk scores, tools monitored
- **Charts**: Health status distribution, risk trends
- **Alerts**: Recent critical and high-severity alerts

### Log Analysis
1. Navigate to "🔍 Log Analysis"
2. Upload your log files (txt, log, csv)
3. View AI-generated analysis including:
   - Risk score (1-10)
   - Health status (HEALTHY/WARNING/CRITICAL)
   - Security issues found
   - AI recommendations

### Tool Health Checks
1. Go to "🛠️ Tool Health Checks"
2. Select the tools you want to monitor
3. Click "Run Health Checks"
4. Review detailed results for each tool

### Reports
1. Visit "📋 Reports"
2. Choose report type and period
3. Generate and download PDF reports
4. Reports include executive summaries and technical details

## 🏗️ Architecture

```
cyberhealth-assistant/
├── main.py                 # Main Streamlit application
├── config.py              # Configuration management
├── database.py            # SQLite database operations
├── ai_analyzer.py         # OpenAI-powered analysis
├── report_generator.py    # PDF report generation
├── utils.py              # Utility functions
├── requirements.txt       # Python dependencies
├── integrations/          # Tool integration modules
│   ├── splunk.py         # Splunk SIEM integration
│   ├── checkpoint.py     # Checkpoint firewall integration
│   ├── crowdstrike.py    # CrowdStrike EDR integration
│   └── tenable.py        # Tenable vulnerability management
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Database Configuration
DATABASE_PATH=cyberhealth.db

# Splunk Configuration
SPLUNK_BASE_URL=https://splunk.company.com:8089
SPLUNK_USERNAME=admin
SPLUNK_PASSWORD=your_password

# Checkpoint Configuration
CHECKPOINT_BASE_URL=https://checkpoint.company.com
CHECKPOINT_USERNAME=admin
CHECKPOINT_PASSWORD=your_password
CHECKPOINT_API_KEY=your_api_key

# CrowdStrike Configuration
CROWDSTRIKE_BASE_URL=https://api.crowdstrike.com
CROWDSTRIKE_CLIENT_ID=your_client_id
CROWDSTRIKE_CLIENT_SECRET=your_client_secret

# Tenable Configuration
TENABLE_BASE_URL=https://cloud.tenable.com
TENABLE_ACCESS_KEY=your_access_key
TENABLE_SECRET_KEY=your_secret_key

# Report Configuration
COMPANY_NAME=Your Company Name
```

### Tool Integration Setup

Each cybersecurity tool requires specific configuration:

#### Splunk
- Enable REST API access
- Create dedicated user with appropriate permissions
- Configure SSL certificates if needed

#### Checkpoint
- Enable API access in SmartConsole
- Generate API key or use username/password
- Configure firewall rules for API access

#### CrowdStrike
- Create API client in Falcon console
- Generate client ID and secret
- Assign appropriate permissions

#### Tenable
- Generate API keys from Tenable.io
- Configure API access permissions
- Set up asset groups and scan policies

## 📊 Features in Detail

### AI-Powered Analysis
- **Log Analysis**: Upload any security log for instant AI analysis
- **Risk Scoring**: 1-10 risk scale with detailed breakdown
- **Issue Detection**: Automatic identification of security problems
- **Recommendations**: AI-generated actionable recommendations

### Health Monitoring
- **Real-time Status**: Live health checks across all tools
- **Performance Metrics**: Response times, error rates, availability
- **Alert System**: Critical and warning alerts with details
- **Trend Analysis**: Historical data and pattern recognition

### Reporting
- **Executive Reports**: High-level summaries for management
- **Technical Reports**: Detailed technical analysis
- **Customizable**: Select report type, period, and content
- **PDF Export**: Professional PDF reports with charts and data

### Data Management
- **SQLite Database**: Lightweight, persistent storage
- **Historical Data**: Track trends and patterns over time
- **Metrics Storage**: Performance and health metrics
- **Report History**: Store generated reports for reference

## 🔒 Security Considerations

### API Key Management
- Store API keys securely in environment variables
- Use dedicated service accounts for tool access
- Rotate API keys regularly
- Implement least-privilege access

### Network Security
- Use HTTPS for all API communications
- Implement proper firewall rules
- Use VPN for remote access if needed
- Monitor API access logs

### Data Protection
- Encrypt sensitive data at rest
- Implement proper access controls
- Regular security audits
- Compliance with data protection regulations

## 🛠️ Development

### Adding New Tool Integrations

1. Create a new file in `integrations/` directory
2. Implement the required methods:
   - `__init__()`: Initialize connection
   - `run_health_checks()`: Perform health checks
   - Tool-specific methods for detailed monitoring

3. Add configuration to `config.py`
4. Update the main application to include the new tool

### Example Tool Integration

```python
# integrations/example_tool.py
class ExampleToolClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        # Initialize connection
        
    def run_health_checks(self):
        # Perform health checks
        return {
            "tool_name": "Example Tool",
            "overall_status": "HEALTHY",
            "checks": {
                "system_status": {"status": "HEALTHY", "details": "..."}
            }
        }
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/cyberhealth-assistant.git
cd cyberhealth-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run main.py --server.port 8501
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT-4 API for AI-powered analysis
- **Streamlit** for the excellent web application framework
- **ReportLab** for PDF generation capabilities
- **Plotly** for interactive data visualization
- **Pandas** for data manipulation and analysis

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/cyberhealth-assistant/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/cyberhealth-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/cyberhealth-assistant/discussions)
- **Email**: support@cyberhealth-assistant.com

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- AI-powered log analysis
- Multi-tool health monitoring
- PDF report generation
- Real-time dashboard
- SQLite data persistence

### Planned Features
- Additional tool integrations (Palo Alto, Imperva)
- Advanced AI models and analysis
- Email alerts and notifications
- REST API for external integrations
- Docker containerization
- Kubernetes deployment support

---

**🔐 CyberHealth Assistant** - Making cybersecurity monitoring smarter, faster, and more effective.