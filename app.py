# import libraries 
import streamlit as st
from dotenv import load_dotenv

# load env variables
load_dotenv()

def main():
    # Set the page config
    st.set_page_config(page_title="GEN AI Academic guide",
                       page_icon='static\Capstone_bot.ico',
                       menu_items={
                                'About': "This is an *extremely* cool app!"
                                  }
                       )
    # initialise container object
    container1 = st.container(border=True)
    with container1:
        st.title("GEN AI Academic guide")
        st.divider()
        col1, col2 = st.columns([3,1], gap="medium")
        # Making Menu
        with col2:
            st.markdown('**Menu**')
            st.divider()
            st.page_link("pages/admin.py", label="Admin Panel", icon="⚙", help="Go to Admin Page", disabled=False, use_container_width=True)
            st.divider()
            st.page_link("pages/model.py", label="Gen AI Guide", icon="👨‍🎓", help="Go to Academic Guide", disabled=False, use_container_width=True)
            st.divider()
            
        with col1:
            st.image("static/Chat bot-cuate.png",use_column_width=True)
            
        
# Application execution
if __name__=='__main__':
    main()
    