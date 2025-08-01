
import streamlit as st
from utils import run_health_checks
from integrations.splunk import SplunkClient

st.set_page_config(page_title="Cybersecurity Health Assistant", layout="wide")

st.title("🔐 Cybersecurity Health Assistant")
st.write("Upload system logs or connect to tools for automated health checks.")

# Log File Upload Section
uploaded_file = st.file_uploader("Upload a log file", type=["txt", "log"])
if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    results = run_health_checks(content)
    for issue in results:
        st.warning(issue)

# Splunk Connection (Demo)
with st.expander("Connect to Splunk (Demo)"):
    splunk_url = st.text_input("Splunk Base URL", "https://splunk.company.com:8089")
    splunk_user = st.text_input("Username", "admin")
    splunk_pass = st.text_input("Password", type="password")
    spl_query = st.text_input("Search Query", "index=firewall_logs | stats count by action")
    if st.button("Run Splunk Query"):
        try:
            client = SplunkClient(splunk_url, splunk_user, splunk_pass)
            splunk_results = client.run_search(spl_query)
            st.success("Query successful. Displaying results:")
            st.json(splunk_results)
        except Exception as e:
            st.error(f"Error: {e}")
