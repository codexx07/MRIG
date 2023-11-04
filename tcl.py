#%% 
import os
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
api_key = os.getenv("api_key")

#%%
from langchain.llms import GooglePalm
llm = GooglePalm(google_api_key=api_key,temperature=0.001)

# %%
from langchain.document_loaders.csv_loader import CSVLoader

# %%
loader = CSVLoader(file_path=r'C:\Users\Sarabjot Singh\OneDrive\Desktop\MRIG\dataset_30.csv', source_column='prompt')
data = loader.load()

# %%
from langchain.embeddings import HuggingFaceInstructEmbeddings
from InstructorEmbedding import INSTRUCTOR

# Initialize instructor embeddings using the Hugging Face model
embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
e = embeddings.embed_query("What is penumonia?")

# %%
len(e)

# %%
e[:33]

# %%
from langchain.vectorstores import FAISS

# Create a FAISS instance for vector database from 'data'
vectordb = FAISS.from_documents(documents=data, embedding=embeddings)

# Create a retriever for querying the vector database
retriever = vectordb.as_retriever(score_threshold=0.85)  


# %%
retriever= vectordb.as_retriever()
rdocs = retriever.get_relevant_documents("penmonia")
rdocs

# %%
from langchain.chains import RetrievalQA
chain = RetrievalQA.from_chain_type(llm=llm,
                            chain_type="stuff",
                            retriever=retriever,
                            input_key="query",
                            return_source_documents=True,
                        )

# %%
chain("what is pnumoia and How is it cured")

# %%
from langchain.prompts import PromptTemplate

prompt_template = """Given the following context and a question, generate an answer based on this context only.
In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

CONTEXT: {context}

QUESTION: {question}"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
chain_type_kwargs = {"prompt": PROMPT}


# %%
from langchain.chains import RetrievalQA

chain = RetrievalQA.from_chain_type(llm=llm,
                            chain_type="stuff",
                            retriever=retriever,
                            input_key="query",
                            return_source_documents=True,
                           )

#%%
def query_chain(query):
    response = chain(query)
    # If 'response' is a dictionary and has some key, say 'answer', to check:
    if 'answer' in response and not response['answer']:  # adjust the condition based on response structure
        return "I don't know."
    return response

# %%
chain("penumonia")

# %%
chain(" independence day")

# %%
chain(" what is edema ")

# %%
chain("which is the best college in india")

# %%
response = chain(" How to make butter chicken")
print(response)