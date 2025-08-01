# 🚀 Quick Setup Guide for CyberHealth Assistant

## 📦 What's in the Zip File

The `cyberhealth-assistant.zip` contains:
- Complete Python application with all modules
- Tool integrations for Splunk, Checkpoint, CrowdStrike, Tenable
- AI-powered log analysis capabilities
- Professional PDF report generation
- SQLite database for data persistence
- Comprehensive documentation

## 🛠️ Setup Instructions for VS Code

### 1. Extract the Zip File
```bash
# Extract to your preferred directory
unzip cyberhealth-assistant.zip
cd cyberhealth-assistant
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys and configurations
# At minimum, you can leave them empty for demo mode
```

### 5. Test Installation
```bash
python test_installation.py
```

### 6. Run the Application
```bash
# Option 1: Direct Streamlit run
streamlit run main.py

# Option 2: Use the startup script
python start.py
```

### 7. Access the Application
- Open your browser to: `http://localhost:8501`
- The application will have a modern web interface

## 🎯 VS Code Configuration

### Recommended Extensions
- **Python** (Microsoft)
- **Python Indent** (Kevin Rose)
- **Python Docstring Generator** (njpwerner)
- **autoDocstring** (Nils Werner)

### VS Code Settings
Add to your `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.formatting.provider": "black"
}
```

## 🔧 Configuration Options

### OpenAI API (Optional)
For AI-powered analysis, add your OpenAI API key to `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Tool Integrations (Optional)
Configure your cybersecurity tools in `.env`:
```env
# Splunk
SPLUNK_BASE_URL=https://your-splunk-instance.com:8089
SPLUNK_USERNAME=your_username
SPLUNK_PASSWORD=your_password

# Checkpoint
CHECKPOINT_BASE_URL=https://your-checkpoint-instance.com
CHECKPOINT_USERNAME=your_username
CHECKPOINT_PASSWORD=your_password

# CrowdStrike
CROWDSTRIKE_CLIENT_ID=your_client_id
CROWDSTRIKE_CLIENT_SECRET=your_client_secret

# Tenable
TENABLE_ACCESS_KEY=your_access_key
TENABLE_SECRET_KEY=your_secret_key
```

## 📊 Application Features

### Dashboard
- Real-time cybersecurity health overview
- Interactive charts and metrics
- Recent alerts and critical issues

### Log Analysis
- Upload firewall, system, or security logs
- AI-powered analysis with risk scoring
- Security issue detection and recommendations

### Tool Health Checks
- Monitor Splunk, Checkpoint, CrowdStrike, Tenable
- Comprehensive health assessments
- Detailed status reporting

### Reports
- Generate professional PDF reports
- Executive summaries with AI insights
- Customizable report periods

### Trends
- Historical data analysis
- Pattern recognition
- Risk trajectory tracking

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   streamlit run main.py --server.port 8502
   ```

2. **Missing Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Database Issues**
   ```bash
   # Remove and recreate database
   rm cyberhealth.db
   python test_installation.py
   ```

4. **OpenAI API Errors**
   - Check your API key in `.env`
   - Verify internet connection
   - Check OpenAI account credits

### Debug Mode
```bash
# Run with debug information
streamlit run main.py --logger.level debug
```

## 📁 Project Structure

```
cyberhealth-assistant/
├── main.py                 # Main Streamlit application
├── config.py              # Configuration management
├── database.py            # SQLite database operations
├── ai_analyzer.py         # OpenAI-powered analysis
├── report_generator.py    # PDF report generation
├── utils.py              # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── README.md             # Comprehensive documentation
├── test_installation.py  # Installation verification
├── start.py              # Startup script
├── integrations/         # Tool integration modules
│   ├── splunk.py
│   ├── checkpoint.py
│   ├── crowdstrike.py
│   └── tenable.py
└── sample_log.txt        # Sample log file for testing
```

## 🎉 Ready to Use!

Once you've completed the setup:
1. The application will be available at `http://localhost:8501`
2. You can upload log files for AI analysis
3. Monitor your cybersecurity tools
4. Generate professional reports
5. Track trends and patterns

The CyberHealth Assistant is designed to work in both demo mode (without API keys) and full production mode with all integrations configured.

Happy cybersecurity monitoring! 🔐