
print("DEVELOPER NOTE: Page Accessed")
import os
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone # https://docs.pinecone.io/integrations/langchain#4-initialize-a-langchain-vector-store
from langchain_pinecone import PineconeVectorStore
# from openai import OpenAI
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA 
# from langchain.chains import RetrievalQAWithSourcesChain  
import streamlit as st

import pandas as pd
# import textwrap
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders.csv_loader import CSVLoader

from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.callbacks import StdOutCallbackHandler

# from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains.conversation.memory import ConversationBufferMemory
# # from langchain.prompts import (
# #     SystemMessagePromptTemplate,
# #     HumanMessagePromptTemplate,
# #     ChatPromptTemplate,
# #     MessagesPlaceholder
# # )

# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
# # from langchain.agents.agent_toolkits import create_python_agent
# # from langchain.agents.agent_types import AgentType
# from langchain_community.utilities import WikipediaAPIWrapper

print("DEVELOPER NOTE: Imports done")

# Set API keys
openai_api_key = st.secrets["api_key"]
pinecone_api_key = st.secrets["pinecone_api_key"]
os.environ['OPENAI_API_KEY'] = openai_api_key
os.environ['PINECONE_API_KEY'] = pinecone_api_key

print("DEVELOPER NOTE: API Keys Done")

# Embeddings model
st_model_name = "multi-qa-mpnet-base-cos-v1"
embeddings_model = HuggingFaceEmbeddings(model_name=st_model_name)

print("DEVELOPER NOTE: Embeddings Model Done")

# Pinecone Client
pc = Pinecone(
        api_key=pinecone_api_key)
index_name = "cma-app"
index = pc.Index(index_name)
print("Index Stats 1:")
index.describe_index_stats()

# Pinecone VectorStore
vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings_model)

print("DEVELOPER NOTE: Pinecone Initialized")

# Chat model 
# openai_llm = OpenAI(api_key= openai_api_key)
openai_llm = ChatOpenAI(model="gpt-3.5-turbo")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

print("DEVELOPER NOTE: Chat model initialized")

# Documents

## CSV
# basic_qa_csv_file_path = "/workspaces/cma_app/repository/Combined_App_Draft1_QA.csv"
basic_qa_csv_file_path = "repository/translated_responses.csv"


## PDF
# policy_data = [
#     ("Kingdom of Saudi Arabia",
#      "Saudi Labor Law",
#      "https://www.hrsd.gov.sa/sites/default/files/2017-05/LABOR%20LAW.pdf"
#      ),
#     ("Department of Migrant Workers",
#      "Direct Hiring FAQs",
#      "https://dmw.gov.ph/resources/dsms/DMW/Externals/2022/FAQ-POPS-DIRECT.pdf",
#     ),
#     ("Department of Migrant Workers",
#         "Compulsory Insurance Coverage for Agency-Hired Migrant Workers",
#         "https://dmw.gov.ph/resources/dsms/DMW/Externals/2022/FAQ-POPS-DIRECT.pdf",
#         ),
# ]

# columns = ["source", "title", "url"]

# policy_df = pd.DataFrame(policy_data, columns=columns)

# Document Chunking

def get_chunks(type, file_or_policy_path, chunk_size=2000, chunk_overlap=500):
  if type == "csv":
    df  = pd.read_csv(file_or_policy_path)
    first_row = df.iloc[0]
    first_item = first_row.iloc[1]
    second_item = first_row.iloc[2]
    column_names_qa = list(df.columns)
    print('This is the first item:', first_item)
    print('This is the second item:', second_item)
    print(column_names_qa)

    loader_qa = CSVLoader(file_path=file_or_policy_path)
    documents = loader_qa.load()
    for document in documents:
      metadata = document.metadata
      metadata["Main_Topic"] = first_item
      metadata["Sub_Topic"] = second_item

  else:
    for row in file_or_policy_path.itertuples(index=False):
      try:
        loader_qa = PyPDFLoader(row.url)
        documents = loader_qa.load()

        for document in documents:
          metadata = document.metadata
          metadata["url"] = row.url
          metadata["source"] = row.source
          metadata["title"] = row.title

        if metadata.get("page", None) is not None:
            metadata["page"] += 1

      except Exception as e:  # Consider catching specific exceptions
          print(f"Failed to process {row.url} due to: {e}")

  text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

  return text_splitter.split_documents(documents)

def explore_documents(documents):
  block_indent = "   "
  metadata = documents[0].metadata
  content = documents[0].page_content[:300] + ". . ."
  print(f"{metadata['Main_Topic']} {len(documents)} chunks")
  print("Truncated First chunk:")
  print(
      textwrap.fill(
          content,
          initial_indent=block_indent,
          subsequent_indent=block_indent,
          replace_whitespace=True,
      )
  )
  print()

def pretty_print_result(result):
  indent = "    "
  source = [document.metadata["source"] for document in result['source_documents']]
  print()
  print(f"Query: {result['query']}")
  # print(f"Sources: {source}")
  print(f"Answer:")
  indent = "    "
  print (textwrap.fill(result['result'], initial_indent=indent, subsequent_indent=indent))
chunks = []

# basic_qa_chunks = get_chunks('csv', basic_qa_csv_file_path)
# explore_documents(basic_qa_chunks)
# chunks += basic_qa_chunks

# pdf_basic_qa_chunks = get_chunks('pdf', policy_df)
# chunks += pdf_basic_qa_chunks

# vectorstore_from_docs = PineconeVectorStore.from_documents(
#         chunks,
#         index_name=index_name,
#         embedding=embeddings_model,
#         namespace="cma-app_docs"
#     ) 

# # check database size
# print("Index Stats 2:")
index.describe_index_stats()

print("DEVELOPER NOTE: Chunking Done")

handler = StdOutCallbackHandler()

metadata_field_info = [
    # AttributeInfo(
    #     name="source",
    #     description="The organization or source that created the document.",
    #     type="string or list[string]",
    # ),
    # AttributeInfo(
    #     name="title",
    #     description="The title of the document",
    #     type="string",
    # ),
    # AttributeInfo(
    #     name="url",
    #     description="The url for the document",
    #     type="string",
    # ),
    AttributeInfo(
        name="Main_Topic",
        description="Main topic",
        type="string",
    ),
    AttributeInfo(
        name="Sub_Topic",
        description="Sub-topic under main",
        type="string",
    ),
]
document_content_description = "A policy"

print("DEVELOPER NOTE: Meta Data Done")

retriever = SelfQueryRetriever.from_llm(
   openai_llm,
   vectorstore,
   document_content_description,
   metadata_field_info,
   verbose=True,
   enable_limit=True
   )

print("DEVELOPER NOTE: SelQueryRetriever Initialized")

# # Templates

# @st.cache_resource
# def wiki(prompt):
#     wiki_research = WikipediaAPIWrapper().run(prompt)
#     return wiki_research


# wiki_search_template = PromptTemplate(
#     input_variables=['level1', 'level2', 'query'],
#     template='Translate {level1}, {level2}, and {query} into English. Use their English translations going forward. The user is an Overseas Filipino Worker or family member asking about {level2} as it relates to {level1}. Summarize their question "{query}" and formulate the best term to search in Wikipedia to help answer or substantiate this query.')

# summarization_template = PromptTemplate(
#     input_variables=['level1', 'level2', 'query', 'wikipedia_research'],
#     template='The user is an Overseas Filipino Worker or family member asking about {level1} and more specifically about {level2}. Summarize their question "{query}" and substantiate it with Wikipedia research from {wikipedia_research}.')

# ### Bot receives the question ### 

# follow_up_q_template = PromptTemplate(
#     input_variables=['enriched_query'],
#     template='List the questions you would need answered in order to properly answer this question {enriched_query}. Do not ask for any personal, identifying, or sensitive information. This should be in easy to understand Tagalog.')

# user_follow_up_q_template = PromptTemplate(
#     input_variables=['additional_info', 'enriched_query'],
#     template='The user is an Overseas Filipino Worker or family member providing this additional information: {additional_info}. Combine this info with {enriched_query} to produce an answer in easy to understand Tagalog. Ensure your tone is warm and friendly.')


# wiki_term_chain = LLMChain(llm=openai_llm, prompt=wiki_search_template, verbose=True, output_key='wiki_term')
# summary_chain = LLMChain(llm=openai_llm, prompt=summarization_template, verbose=True, output_key='summary')
# follow_up_q_chain = LLMChain(llm=openai_llm, prompt=follow_up_q_template, verbose=True, output_key='followup_q')
# user_follow_up_q_chain = LLMChain(llm=openai_llm, prompt=user_follow_up_q_template, verbose=True, output_key='user_answer_followupq')

csv_file_path = 'chat_history.csv'

if not os.path.exists(csv_file_path):
   with open(csv_file_path, 'w') as f:
     f.write('Main_Topic, Sub_Topic, question,response\n')

def append_to_csv(question, response, metadata):
    metadata_values = ",".join(f'"{value}"' for value in metadata.values())
    with open(csv_file_path, 'a') as f:
        f.write(f'{metadata_values}, "{question}","{response}"\n')

print("DEVELOPER NOTE: CSV append code")

def retrieve_response(query):
  print("Retrieval Started...")
  qa = RetrievalQA.from_chain_type(
    llm=openai_llm,  
    chain_type="stuff",  
    retriever=retriever
    # chain_type_kwargs={"prompt": prompt}
    )  
  print("Retrieval Complete.")
  return qa.run(query)
  
def retrieve_response_with_sources(question):
  qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
    llm = openai_llm,
    retriever = retriever,
    return_source_documents = True,
    callbacks = [handler],
    # chain_type_kwargs={"prompt": prompt}
    )
  return qa_with_sources({"question": question})

print("DEVELOPER NOTE: Retrieval Response Complete")