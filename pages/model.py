# import libraries
import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain import PromptTemplate
from langchain.llms import CTransformers

Faiss_db_Path = "database/vectorestore/faiss_db"

def load_db():
     embeddings = HuggingFaceInstructEmbeddings(model_name ='sentence-transformers/all-MiniLM-L6-v2')
     db = FAISS.load_local(Faiss_db_Path, embeddings)
     return db

def load_llm():
     # Define the LLM
     llm=CTransformers(model='LLM_Model\llama-2-7b-chat.ggmlv3.q3_K_S.bin',
                      model_type='llama',
                      config={'max_new_tokens':128,
                              'temperature':0.3})
     return llm

def custom_prompt_template():
     # Define the prompt
     template = """
     You are an  Academic guide Of MIT-WPU, you will only refer to given data and will not generate you own extra data,
     if asked who are you reply "Academic guide" :
     {user_query}
     """
     prompt = PromptTemplate.from_template(template)
     return prompt

def retrival_chain(db,llm):
     qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type='stuff',
            retriever=db.as_retriever(search_kwargs={"k":3}),
            input_key='question',
     )
     return qa_chain


def Display_chat(user_query):
     # Create the prompt
     prompt = custom_prompt_template()
     # Pass query to prompt
     new_query = prompt.format(user_query=user_query)
     # Store the user prompt 
     st.session_state.messages.append({'role':'user','content': user_query})
     # send query to chain 
     responce = st.session_state.qa_chain.run(new_query)
     # Store the AI response
     st.session_state.messages.append({'role':'assistant','content': responce})
     # looping message list
     count = 0
     for message in st.session_state.messages:
          # Display the message
          st.chat_message(message['role']).markdown(message['content'])
          count += 1
          if count % 2 == 0:
                st.divider()



     
# Application entry point
def main():
     # Set the page config
     st.set_page_config(page_title="GEN AI Academic guide",
                        page_icon="static\Capstone_bot.ico"
                        )

     # Load the .env file
     load_dotenv()

     # Create the containers
     container1 = st.container(border=True)
     container2 = st.container(border=True)
     container3 = st.container(border=False)
     container4 = st.container(border=True)
     
     with container1:
          st.title("Gen-AI Academic Guide")
          st.image('static\Teacher student-cuate.png')
          

     #  Add customf session state exists
     if "messages" not in st.session_state:
               # Initialize session state variables on first run
               st.session_state.messages = []
     if "flag4" not in st.session_state:
               # Initialize session state variables on first run
               st.session_state.flag4 = False
         
     with container2:
          # create the tabs
          tab1, tab2 = st.tabs(["Knowledge Quest", "Chat History"])

     with tab1:
               if st.button("Initiate Bot ", type="primary", disabled=st.session_state.flag4, help='Load the LLM',use_container_width=True):
                    # load the vectorestore
                    db = load_db()
                    # load llm
                    llm = load_llm()
                    # create the conversation chain
                    st.session_state.qa_chain = retrival_chain(db, llm)
                    st.session_state.flag4 = True
               
               # create the chat input
               user_query = container3.chat_input("What's on your mind 👨‍🎓 ?")
               # After input is submitted by user call display function
               if user_query:
                    Display_chat(user_query)

     with tab2:
               # display the chat history
               for item in st.session_state.messages:
                    st.info(item)

     with container4:
               # create the Menu Page Button
               st.page_link("app.py", label="Menu", icon="📟", help="Return To Menu", disabled=False, use_container_width=True)
               
# Application execution
if __name__=='__main__':
    main()