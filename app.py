import streamlit as st
import requests
from newspaper import Article

# Set up API key and base URL for Needle API
API_KEY = "your_needle_api_key"  # Replace with your actual Needle API key
BASE_URL = "https://api.needle-ai.com"

headers = {
    "x-api-key": API_KEY
}

# Function to fetch article content from a URL
def fetch_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Error fetching content: {str(e)}"

# Function to upload content to Needle
def upload_content_to_needle(content):
    url = f"{BASE_URL}/v1/collections/upload"
    data = {"text": content}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to ask questions on the uploaded content
def ask_question_to_needle(collection_id, query):
    url = f"{BASE_URL}/v1/collections/{collection_id}/search"
    data = {"text": query}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Streamlit UI for the chatbot
st.title("Website Content Chatbot with Needle.ai")

# Input for user to provide a URL
url_input = st.text_input("Enter a website URL:")

# Fetch and upload the article content
if url_input:
    st.write(f"Fetching content from: {url_input}")
    article_content = fetch_article_content(url_input)
    
    if article_content.startswith("Error"):
        st.write(article_content)  # Display any error in fetching content
    else:
        st.write("Uploading content to Needle.ai...")
        upload_response = upload_content_to_needle(article_content)
        
        if "error" in upload_response:
            st.write(f"Error uploading to Needle: {upload_response['error']}")
        else:
            st.write("Content uploaded successfully!")

            # Input for the user query
            user_input = st.text_input("Ask a question based on the content:")
            
            if user_input:
                st.write("Retrieving the answer...")
                collection_id = upload_response.get('collection_id', 'default')
                result = ask_question_to_needle(collection_id, user_input)
                
                if "error" in result:
                    st.write(f"Error retrieving answer: {result['error']}")
                else:
                    st.write(f"Answer: {result['answer']}")
