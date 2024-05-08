
# importing libraries
import streamlit as st
import time
import os
import re
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from datetime import datetime

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Path for saving vectorestore , text extracted and chunks
Faiss_db_Path = "database/vectorestore/faiss_db"
extracted_db_path = "database/extracted_db/pdfdata_db.txt"
extracted_chunk_path = "database/extracted_db/chunks_db.txt"

def get_pdf_text(pdf_files):
     text = ""
     for pdf in pdf_files:
          pdf_reader = PdfReader(pdf)
          for page in pdf_reader.pages:
               text += page.extract_text()
     clean_text = preprocess(text)
     return clean_text

def preprocess(text):
     # Tokenization
     tokens = word_tokenize(text)
     # Remove Noise
     cleaned_tokens = [re.sub(r'[^\w\s]', '', token) for token in tokens]
     # Normalization (convert to lowercase)
     cleaned_tokens = [token.lower() for token in cleaned_tokens]
     # Remove Stopwords
     stop_words = set(stopwords.words('english'))
     cleaned_tokens = [token for token in cleaned_tokens if token not in stop_words]
     # Lemmatization
     lemmatizer = WordNetLemmatizer()
     cleaned_tokens = [lemmatizer.lemmatize(token) for token in cleaned_tokens]
     # Convert the cleaned tokens back to a string
     cleaned_text = ' '.join(cleaned_tokens)

     return cleaned_text

# Split text into chunks

def get_text_chunks(raw_text):
     # chunk size
     chunk_size = 512
     text_spliter = CharacterTextSplitter(
          # separate by stop line
          separator  =" ",  
          # maximum characters per chunk
          chunk_size = chunk_size , 
          # how many characters to overlap chunks
          chunk_overlap = int(chunk_size / 10), 
          # function to calculate the length of a chunk
          length_function = len    
     )
     # split the text into chunks
     chunks = text_spliter.split_text(raw_text)
     return chunks


def get_vectorstore(text_chunks):
     # Loading Huggingface Instructor model
     embeddings = HuggingFaceInstructEmbeddings(model_name ='sentence-transformers/all-MiniLM-L12-v2')
     # Create a FAISS instance
     st.session_state.vectorstore = FAISS.from_texts(texts=text_chunks,embedding=embeddings)
     # Save the FAISS instance to a local file
     st.session_state.vectorstore.save_local(Faiss_db_Path)
     # return vectorestore object
     return st.session_state.vectorstore

def main():
     # Set the page config
     st.set_page_config(page_title="GEN AI Academic guide",
                        page_icon= 'static\Capstone_bot.ico'
                        )

     # Load the .env file
     load_dotenv()

     # Initialize session state variables on first run
     if "raw_text" not in st.session_state:
               st.session_state.raw_text= None
     if "text_chunks" not in st.session_state:
               st.session_state.text_chunks= None
     if "vectorstore" not in st.session_state:
               st.session_state.vectorstore= None
     if "flag1" not in st.session_state:
               st.session_state.flag1= True

     # initialise container object      
     container1 = st.container(border=True)
     container3 = st.container(height=500,border=True)
     

     with container1:
          st.title("Gen-AI Academic Guide Admin")
          st.divider()
          
          # Making Colmuns
          col1, col2 = st.columns([2,3])
          ccol1, ccol2 = st.columns([2,2])
          with col1:
               container2 = st.container(height=450,border=True)
               with container2:
                    st.subheader("Your documents")
                    # making uploader for pdf files
                    pdf_files = st.file_uploader("Upload your PDFs",accept_multiple_files=True, type= 'pdf')
                    # making button to process the pdf files only after uploading
                    if pdf_files is not None:
                         flag1 = False
                    else:
                         flag1 = True

                    # button to start processing pdf data
                    if st.button("Process", type="secondary", disabled= flag1, use_container_width=True):
                         bar = st.progress(0, text=":red[ ]")

                         # start time
                         formatted_time1 = datetime.now().strftime("%I:%M:%S %p")

                         # to display time in container1
                         with container1:
                              ccol1.text(f"Start {formatted_time1}")
                         bar.progress(20,text=":green[Pdf_loaded]")
                         time.sleep(3)

                         # Extract text from the PDF files
                         st.session_state.raw_text = get_pdf_text(pdf_files)
                         with open(extracted_db_path, "w") as file:
                              file.write(st.session_state.raw_text)
                         bar.progress(60,text=":green[Text Extracted]")
                         time.sleep(3)

                         # making chunks
                         st.session_state.text_chunks =  get_text_chunks(st.session_state.raw_text)
                         bar.progress(80,text=":green[Chunks Created]")
                         with open(extracted_chunk_path, "w") as file:
                              for item in st.session_state.text_chunks:
                                   file.write(item)
                         time.sleep(3)

                         # create vector store
                         bar.progress(91, text=":red[Making Vectore Store...]")
                         st.session_state.vectorstore = get_vectorstore(st.session_state.text_chunks)
                         bar.progress(90,text=":green[Vectore Created]")
                         time.sleep(3)
                         bar.progress(100, text=":green[Done]")
                         
                         # end time
                         formatted_time2 = datetime.now().strftime("%I:%M:%S %p")
                         with container1:
                              ccol2.text(f"End {formatted_time2}")
                         st.session_state.flag1 = False
                         
          with col2:
               # displaying the image
               st.image("static\Admin-cuate.png", use_column_width=True)    
               st.divider()      
          st.divider()

          # making a button to go to the main page
          st.page_link("app.py", label="Menu", icon="📟", help="Return to Main Page", disabled=False, use_container_width=True)
          with container3:

                # Making Buttons for displaying the data
               row1, row2 = st.columns([2,2])
               with row1:
                    if st.button("PDF Data", type="primary", use_container_width=True, disabled= st.session_state.flag1):
                         with container3:
                              with open(extracted_db_path, "r") as file:
                                   content = file.read()
                                   st.write(content)
               with row2:
                    if st.button("Chunks", type="primary", use_container_width=True, disabled= st.session_state.flag1):
                         with container3:
                              st.write(st.session_state.text_chunks)

# Application execution
if __name__=='__main__':
    main()