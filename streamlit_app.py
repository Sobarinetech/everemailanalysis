import streamlit as st
import google.generativeai as genai
import pandas as pd
import re
from typing import Dict, List

# Configure the API key securely from Streamlit's secrets
# Make sure to add GOOGLE_API_KEY and GEMINI_API_KEY in secrets.toml (for local) or Streamlit Cloud Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Email Analysis App")

# Email input field
email_text = st.text_area("Enter email text:", height=200)

# Button to analyze email
if st.button("Analyze Email"):
    try:
        # Load and configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Preprocess email text
        email_text = email_text.strip()
        email_lines = email_text.split('\n')
        
        # Extract relevant information
        subject = None
        sender = None
        recipients = []
        body = []
        for line in email_lines:
            if line.startswith('Subject: '):
                subject = line[9:].strip()
            elif line.startswith('From: '):
                sender = line[6:].strip()
            elif line.startswith('To: '):
                recipients = line[4:].strip().split(',')
            else:
                body.append(line)
        
        # Generate analysis using Gemini API
        prompt = f"Analyze email with subject '{subject}' from {sender} to {recipients}. Identify root cause and culprit."
        response = model.generate_content(prompt)
        
        # Parse response
        analysis: Dict[str, str] = {}
        for line in response.text.split('\n'):
            match = re.match(r'^(Root Cause|Culprit): (.*)$', line)
            if match:
                analysis[match.group(1)] = match.group(2)
        
        # Display analysis in Streamlit
        st.write("Analysis:")
        st.write(f"**Subject:** {subject}")
        st.write(f"**Sender:** {sender}")
        st.write(f"**Recipients:** {', '.join(recipients)}")
        st.write(f"**Root Cause:** {analysis.get('Root Cause', 'Not identified')}")
        st.write(f"**Culprit:** {analysis.get('Culprit', 'Not identified')}")
        
        # Display email body
        st.write("Email Body:")
        st.write('\n'.join(body))
    except Exception as e:
        st.error(f"Error: {e}")
