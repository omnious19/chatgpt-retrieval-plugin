import streamlit as st
import requests
import json

# Set the base URL
base_url = 'http://localhost:8000'  # Replace with your FastAPI app URL

# Set app title
st.title('NearGPT Plugin Interface')

# Add a dropdown to select endpoints
option = st.selectbox(
    'Select the endpoint',
    ('Upsert Documents', 'Upsert File', 'Query Database', 'Delete Documents'))

# Display help text in a sidebar
with st.sidebar:
    st.header("Instructions")
    st.write("""
    1. **Upsert Documents**: Input your documents in JSON format.
    2. **Upsert File**: Choose a file to upload.
    3. **Query Database**: Input your query in JSON format.
    4. **Delete Documents**: Input your delete request in JSON format.
    """)

# Handle different endpoints based on user's selection
if option == 'Upsert Documents':
    st.subheader('Upsert Documents')

    documents_json = st.text_area('Enter your documents in JSON format', height=200)

    if st.button('Upsert Documents'):
        try:
            documents = json.loads(documents_json)
            response = requests.post(f'{base_url}/upsert', json=documents)
            st.success("Documents successfully upserted")
            st.json(response.json())
        except Exception as e:
            st.error(str(e))

elif option == 'Upsert File':
    st.subheader('Upsert File')

    uploaded_file = st.file_uploader('Choose a file')

    if uploaded_file is not None:
        try:
            files = {
                'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }
            response = requests.post(f'{base_url}/upsert-file', files=files)
            st.success("File successfully upserted")
            st.json(response.json())
        except Exception as e:
            st.error(str(e))

elif option == 'Query Database':
    st.subheader('Query Database')

    query_json = st.text_area('Enter your query in JSON format', height=200)

    if st.button('Query Database'):
        try:
            query = json.loads(query_json)
            response = requests.post(f'{base_url}/query', json=query)
            st.success("Query executed successfully")
            st.json(response.json())
        except Exception as e:
            st.error(str(e))

elif option == 'Delete Documents':
    st.subheader('Delete Documents')

    delete_json = st.text_area('Enter your delete request in JSON format', height=200)

    if st.button('Delete Documents'):
        try:
            delete_request = json.loads(delete_json)
            response = requests.delete(f'{base_url}/delete', json=delete_request)
            st.success("Documents deleted successfully")
            st.json(response.json())
        except Exception as e:
            st.error(str(e))

# Footer
st.markdown("---")
st.markdown("Powered by [Verifiable Interoperable Secure Cognitive Architecture](https://visca.ai)")