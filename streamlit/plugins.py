import streamlit as st
from PIL import Image

# Assuming you have a dictionary of plugins
plugins = {
    'Near Protocol': {
        'description': "Supercharge your Visca AI agents with our Near Protocol Knowledge Enhancer. This plugin imbibes your AI with comprehensive insights about the Near Protocol, a scalable and user-friendly blockchain platform. With this knowledge extension, your Visca AI agent will become an expert on all things Near Protocol, ready to delve into the platform's intricacies and deliver high-quality responses. Empower your Visca AI with the Near Protocol Knowledge Enhancer, and experience a heightened interaction that speaks blockchain fluently!",
        'acccess_link': 'https://plugins.visca.ai/near_query.html',
        #'image': 'path_to_image1.png',
        'category': 'Knowledge Base',
        'version': 1.0
    },
    'Move Programming Language': {
        'description': "Equip your Visca AI agents with the language of blockchain - 'Move'. Our Move Programming Language Knowledge Enhancer plugin arms your AI agents with an exhaustive understanding of this innovative programming language, designed specifically for the creation and management of digital assets. Let your Visca AI agent navigate through the complexities of Move with ease, delivering top-notch, context-specific responses. With the Move Programming Language Knowledge Enhancer, your AI speaks the blockchain lingo!",        'acccess_link': 'https://example.com/acccess2',
        'acccess_link': 'https://plugins.visca.ai/move_query.html',        
        #'image': 'path_to_image2.png',
        'category': 'Knowledge Base',
        'version': 1.0
    },
    'Aptos Network': {
        'description': "Elevate your Visca AI agent's capabilities with the Aptos Network Knowledge Enhancer. This plugin enables your AI to grasp the rich landscape of Aptos Network, an innovative blockchain ecosystem built for scalability and decentralization. With this knowledge enhancement, your Visca AI agent becomes your blockchain whisperer, unravelling the workings of the Aptos Network in every interaction. Equip your AI with the Aptos Network Knowledge Enhancer, and dive into the world of advanced blockchain technology!",
        'acccess_link': 'https://plugins.visca.ai/aptos_query.html',
        #'image': 'path_to_image1.png',
        'category': 'Knowledge Base',
        'version': 1.0
    },
    # add more plugins
}

st.set_page_config(page_title='Visca Plugins Marketplace', page_icon=':world:', layout='wide', initial_sidebar_state='expanded')

st.sidebar.title('Visca Plugins Marketplace')

categories = list(set([details['category'] for details in plugins.values()]))
selected_category = st.sidebar.selectbox('Select Category', categories)

for plugin, details in plugins.items():
    if details['category'] == selected_category:
        col1, col2 = st.columns([1, 3])
        with col1:
            #st.image(details['image'], use_column_width=True)
            st.text("")  # Empty space
        with col2:
            st.subheader(plugin)
            st.write(details['description'])
            st.text(f"Category: {details['category']}")
            st.text(f"Version: {details['version']}")
            st.text("Access Link:")
            st.code(details["acccess_link"])
            
        st.markdown("---")  # Line separator