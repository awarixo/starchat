#%%
import os
import pickle
import tiktoken
import re
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA, ConversationalRetrievalChain, LLMChain
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain

from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory,ConversationSummaryBufferMemory, ConversationSummaryMemory
from langchain.chains.question_answering import load_qa_chain
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
celebrity = "elon_musk"

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)
limited_memory = ConversationBufferWindowMemory(memory_key='chat_history', k=2, return_messages=True)
summary_memory = ConversationSummaryBufferMemory(llm=llm, memory_key="chat_history", return_messages=True, max_token_limit=1000)
memory = ConversationSummaryMemory(llm=llm,memory_key="chat_history",return_messages=True)


def create_db_from_docs(doc_url):
    loader = TextLoader(doc_url, encoding="utf8")
    loaded_docs = loader.load()
    for doc in loaded_docs:
        doc.page_content = doc.page_content.replace("\n", "")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=0, separators=['#'])
    pages = text_splitter.split_documents(loaded_docs)
    page1 = str(pages[0])
    print(len(page1), pages[0])
    if os.path.exists(f"FAISS_INDEX/{celebrity}.pkl"):
        with open(f"FAISS_INDEX/{celebrity}.pkl", "rb") as f:
            vector_db = pickle.load(f)
    else: 
        vector_db = FAISS.from_documents(pages, OpenAIEmbeddings())
        with open(f"FAISS_INDEX/{celebrity}.pkl","wb") as f:
            pickle.dump(vector_db, f)
    return vector_db


# def stuff_page (doc): # Get the page number from the doc attribute 
#     page_number = doc.page_number # Get the section title from the doc attribute 
#     section_title = doc.section_title # Format the header with the page number and the section title 
#     header = f"Page {page_number}: {section_title}\n" # Format the footer with the page number 
#     footer = f"\nPage {page_number}" # Return the stuffed document as a string 
#     return header + doc.page_content + footer


def memory_improved_question(question,vector_db):
    print(f"simple question: {question}")
    #standalone question is generated.
    # stuff_docs_chain = StuffDocumentsChain(pages, stuff_page)


    summary_template = (
    """Combine the chat history and follow up question into "
    a standalone question. Do not answer the question just combine into a standalone. If there is no relevant history, return the exact human question
    Chat History: {chat_history}
    Follow up question: {question}"""
    )
    combination_prompt = PromptTemplate.from_template(summary_template)
    retriever=vector_db.as_retriever(search_kwargs={"k": 4})
    question_generator_chain = LLMChain(llm=llm, prompt=combination_prompt)

    system1 = f"Play the role of {celebrity},"
    system2 = ''' here are extracts from some of his interviews: {context}
            Dont use everything from the extract, select the most relevant parts of the extract to create an answer
            similar to what'''
    
    system3 = '''would say to answer the question asked. speak in the first person 
    Question: {question}
            '''
    system = system1 + system2 + " " + celebrity + " " + system3 + " " + celebrity + ":"
    QA_CHAIN_PROMPT = PromptTemplate.from_template(system)

    qa_memory_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=limited_memory,
        condense_question_prompt =combination_prompt,
        verbose=True,
        combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
        # question_generator= question_generator_chain,
    )

    with get_openai_callback() as cb:
        improved_question = qa_memory_chain({"question": question})
        print(f"Token Count: {cb}")
        print(improved_question)
    return improved_question["answer"]



# def get_response_from_query(vector_db, improved_question, k=2):
#     """
#     1. Perform similarity search to get relevant documents
#     2. Define chatbot template
#     """

#     docs = vector_db.similarity_search(question, k=k)
#     for i,doc in enumerate(docs, start=1):
#         doclen = str(doc)
#         print(f"DOCUMENT {i}. {len(doclen)}{doc}")
#     docs_page_content = " ".join([d.page_content for d in docs])
#     # combine_docs_chain = load_qa_chain(llm=llm, template=CONDENSE_QUESTION_PROMPT)


#     # Template for system message  {context}
#     system = '''
#             You are a helpful assistant providing step by step guidance on how to solve issues for Universiti teknologi Petronas 
#             students and staff based on the utp knowledge base content: {extract}
            
#             Use the following pieces of context to answer the users question.
#             If you don't know the answer, just say that you don't know, don't try to make up an answer.

#             your answers should be verbose and detailed, include all the relevant links and emails in your answer, and include a link to the article you got the information from  

#             Question: {question}
            
#             Assistant:
#             '''
    
#     QA_CHAIN_PROMPT = PromptTemplate.from_template(system)
#     retrievalChain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=vector_db.as_retriever(),
#         chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
#     )

#     #Call Openai for response
#     with get_openai_callback() as cb:
#         try:
#             response = retrievalChain({"query": improved_question})
#             print(cb)
#             result = response["result"]
#             return result
#         except Exception as e:
#             print(e)
    
    # with get_openai_callback() as cb:
    #     result = qa_memory_chain({"query": question})
    #     print(f"    memory: {memory}")
    #     print(f"Token count: {cb}")
    #     return result["result"]

#%% 

doc_url = f"personality_bank/{celebrity}.txt"
with open(doc_url, 'r')as doc:
    document = doc.read()
    # document = document.replace('##Q:', '#Q:')
    document = document.replace(r'(?<!#)Q:', '#Q:')
with open(doc_url, "w") as doc:
    doc.write(document)
vector_db = create_db_from_docs(doc_url)
# vector_db = FAISS.load_local("FAISS_INDEX",OpenAIEmbeddings())
while True:

    
    question = input("What is your issue?: ")
    improved_question = memory_improved_question(question, vector_db)
    print(f"response: {improved_question}")

# %%
