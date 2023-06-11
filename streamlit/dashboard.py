import streamlit as st
import requests
import json

# Set the base URL
base_url = 'http://localhost:8000'  # Replace with your FastAPI app URL

# Page configuration
st.set_page_config(page_title="Visca Near Hub", page_icon=":books:", layout="wide", initial_sidebar_state='expanded')

# Define categories and pages
CATEGORIES = {
    "Plugin Management": {
        "Manage Knowledge Base": "page1",
    },
    "Guardrail Management": {
        "Coming Soon": "page2",
    },
    "Middleware Management": {
        "Coming Soon": "page3",
    },
    "Channel Management": {
        "Coming Soon": "page4",
    }
}



# Initialize selected_category and selected_page in the session state
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = list(CATEGORIES.keys())[0]
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = list(CATEGORIES[st.session_state.selected_category].values())[0]

# Sidebar with page selection
st.sidebar.title('NearGPT Admin Hub')
st.sidebar.subheader('Powered By: Verifiable Interoperable Secure Cognitive Architetcture(Visca.AI)')
selected_category = st.sidebar.selectbox('NearGPT Mangement Console', list(CATEGORIES.keys()), list(CATEGORIES.keys()).index(st.session_state.selected_category))
st.session_state.selected_category = selected_category
selected_page_title = st.sidebar.radio(f"Go to {st.session_state.selected_category}", options=list(CATEGORIES[selected_category].keys()), key=selected_category)

# Update the page state based on selected page title
if selected_page_title in CATEGORIES[selected_category]:
    st.session_state.selected_page = CATEGORIES[selected_category][selected_page_title]


# Input for Bearer Token
bearer_token = st.text_input("Enter your HTTP Bearer Token", type="password")
headers = {
    'Authorization': f'Bearer {bearer_token}',
}


# Page contents
if st.session_state.selected_page == "page1":
    # Set app title
    st.title('Manage Knowledge Base')

    # Tabs for endpoints
    tab1, tab2, tab3, tab4 = st.tabs(['Upsert File', 'Upsert Documents', 'Query Database', 'Delete Documents'])

    # Add help section
    show_help = st.checkbox("Show Help")
    if show_help:
        with st.expander("Help"):
            st.write("""
            1. **Upsert Documents**: Insert or update documents in the database. Input your documents in JSON format.
            2. **Upsert File**: Insert or update documents in the database from a file. Choose a file to upload.
            3. **Query Database**: Retrieve data from the database. Input your query in JSON format.
            4. **Delete Documents**: Remove documents from the database. Input your delete request in JSON format.
            """)

    with tab2:
        # 'Upsert Documents' endpoint
        st.subheader('Insert or Update Documents')
        documents_json = st.text_area('Enter your documents in JSON format', height=200, value='{ "doc1": { "field1": "value1" } }')

        if st.button('Upsert Documents'):
            try:
                documents = json.loads(documents_json)
                response = requests.post(f'{base_url}/upsert', headers=headers, json=documents)
                st.success("Documents successfully upserted")
                st.json(response.json())
            except Exception as e:
                st.error(str(e))

    with tab1:
        # 'Upsert File' endpoint
        st.subheader('Insert or Update Documents From File')
        uploaded_file = st.file_uploader('Choose a file')

        if uploaded_file is not None:
            try:
                files = {
                    'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                }
                response = requests.post(f'{base_url}/upsert-file', headers=headers, files=files)
                st.success("File successfully upserted")
                st.json(response.json())
            except Exception as e:
                st.error(str(e))

    with tab3:
        # 'Query Database' endpoint
        st.subheader('Retrieve Data From Database')
        query_json = st.text_area('Enter your query in JSON format', height=200, value='{ "field1": "value1" }')

        if st.button('Query Database'):
            try:
                query = json.loads(query_json)
                response = requests.post(f'{base_url}/query', headers=headers, json=query)
                st.success("Query executed successfully")
                st.json(response.json())
            except Exception as e:
                st.error(str(e))

    with tab4:
        # 'Delete Documents' endpoint
        st.subheader('Remove Documents From Database')
        delete_json = st.text_area('Enter your delete request in JSON format', height=200, value='{ "doc1": { "field1": "value1" } }')

        if st.button('Delete Documents'):
            try:
                delete_request = json.loads(delete_json)
                response = requests.delete(f'{base_url}/delete', headers=headers, json=delete_request)
                st.success("Documents deleted successfully")
                st.json(response.json())
            except Exception as e:
                st.error(str(e))

elif st.session_state.selected_page == "page2":
    st.title('Coming Soon!')
    
    # An image or gif that fits the theme of your page
    #st.image('https://via.placeholder.com/640', caption='Exciting features on the way!', use_column_width=True)

    # A brief message
    st.markdown('''
    #### We're Busy Building Extraordinary!
    Right now, our team of skilled developers is fully immersed in the process of crafting the Guardrail Management feature. A suite of powerful tools that's set to revolutionize your workflow is currently under creation. We're integrating efficiency, usability, and state-of-the-art technology to provide you with a superior guardrail management experience.
    Our aim? To empower you to do more, in less time, with a tool that's as robust as it is user-friendly.
    So hold tight! And get ready for a feature that's more than just an upgrade - it's a game-changer.
    Stay tuned. We promise, it's worth the wait!
    ''')

    # An ETA, if you have one
    st.markdown('Estimated Time of Arrival: End Q3 2023')


elif st.session_state.selected_page == "page3":
    st.title('Coming Soon!')
    
    # An image or gif that fits the theme of your page
    #st.image('https://via.placeholder.com/640', caption='Exciting features on the way!', use_column_width=True)

    # A brief message
    st.markdown('''
    #### Supercharging Connectivity is in Progress!
    Have you ever thought about how powerful it would be if all your software could talk to each other without any hindrance? We have, and we're turning that vision into a reality!
    Our team of tech wizards is currently burning the midnight oil to bring you the Middleware Integrations feature. Designed to transform the way your applications interact, this tool is set to become the backbone of your digital ecosystem.
    Through this feature, we're bridging the gap between your software, allowing them to share data and functionalities like never before. This means smoother operations, efficient processes, and a more cohesive technology environment for your business.
    Wait for it! The ability to tie together all your apps in harmony is just around the corner. We can hardly wait to unveil it for you.
    Stay tuned as we bring the future of software integration to you!
    ''')

    # An ETA, if you have one
    st.markdown('Estimated Time of Arrival: End Q3 2023')

elif st.session_state.selected_page == "page4":
    st.title('Coming Soon!')
    
    # An image or gif that fits the theme of your page
    #st.image('https://via.placeholder.com/640', caption='Exciting features on the way!', use_column_width=True)

    # A brief message
    st.markdown('''
    #### We're Engineering Innovation!
    Just imagine - all your communication channels, seamlessly integrated, and intuitively managed in one place. Well, that's no longer a daydream. Our brilliant team is at this very moment, tirelessly working on creating the Channel Management feature.
    This exceptional tool is designed to revolutionize the way you navigate through multiple communication platforms. Efficiency, convenience, and connectivity will soon be at your fingertips. With this tool, we're eliminating confusion and boosting your productivity by leaps and bounds.
    Our goal? To streamline your communication processes, ensure smooth interaction, and let you take control of your channels like never before.
    So hang in there! Get ready to redefine your communication experience.
    Stay connected and watch this space. We guarantee, it'll be a breakthrough worth your anticipation!
    ''')

    # An ETA, if you have one
    st.markdown('Estimated Time of Arrival: End Q3 2023')

# Footer
st.markdown("---")
#st.markdown("Powered by [Verifiable Interoperable Secure Cognitive Architecture](https://visca.ai)")
