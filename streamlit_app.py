import streamlit as st
import google.generativeai as genai
import re
import nltk
from nltk.tokenize import wordpiece_tokenizer
from typing import Dict, List

# Configure API key securely
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Email Analysis and Culprit Detection")

# Email input field
email_text = st.text_area("Enter email text:", height=200)

# Analysis options
analysis_options = st.expander("Analysis Options")
with analysis_options:
    root_cause_analysis = st.checkbox("Root Cause Analysis")
    culprit_detection = st.checkbox("Culprit Detection")
    sentiment_analysis = st.checkbox("Sentiment Analysis")
    entity_extraction = st.checkbox("Entity Extraction")

# Button to analyze email
if st.button("Analyze Email"):
    try:
        # Load and configure Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Preprocess email text
        email_text = email_text.strip()
        email_lines = email_text.split('\n')
        
        # Tokenize email text
        tokenizer = wordpiece_tokenizer.WordPieceTokenizer()
        tokens = tokenizer.tokenize(email_text)
        
        # Generate analysis using Gemini API
        prompt = f"Analyze email with tokens {tokens}. "
        if root_cause_analysis:
            prompt += "Identify root cause using causal analysis. "
        if culprit_detection:
            prompt += "Detect culprit using named entity recognition. "
        if sentiment_analysis:
            prompt += "Perform sentiment analysis using sentiment classification. "
        if entity_extraction:
            prompt += "Extract relevant entities using named entity recognition. "
        
        response = model.generate_content(prompt)
        
        # Parse response
        analysis: Dict[str, str] = {}
        for line in response.text.split('\n'):
            match = re.match(r'^(Root Cause|Culprit|Sentiment|Entity): (.*)$', line)
            if match:
                analysis[match.group(1)] = match.group(2)
        
        # Post-processing
        if root_cause_analysis:
            root_cause = analysis.get('Root Cause', '')
            root_cause = re.sub(r'\[.*?\]', '', root_cause)  # Remove Gemini's confidence scores
        if culprit_detection:
            culprit = analysis.get('Culprit', '')
            culprit = re.sub(r'\[.*?\]', '', culprit)  # Remove Gemini's confidence scores
        
        # Display analysis in Streamlit
        st.write("Analysis:")
        if root_cause_analysis:
            st.write(f"**Root Cause:** {root_cause}")
        if culprit_detection:
            st.write(f"**Culprit:** {culprit}")
        if sentiment_analysis:
            st.write(f"**Sentiment:** {analysis.get('Sentiment', 'Not analyzed')}")
        if entity_extraction:
            st.write(f"**Entities:** {analysis.get('Entity', 'Not extracted')}")
    except Exception as e:
        st.error(f"Error: {e}")
