import os
import asyncio
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Ensure the API key is loaded from environment variables
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables")

# Initialize OpenAIEmbeddings with specific parameters
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",  # Use the latest model
    openai_api_key=api_key,
    chunk_size=1000,  # Process 1000 texts at a time
    max_retries=3,  # Retry API calls up to 3 times
    request_timeout=30,  # Set a 30-second timeout for API requests
    show_progress_bar=True,  # Show progress for large batches
    embedding_ctx_length=8191,  # Maximum context length
    disallowed_special=(),  # Allow all special tokens
)

def create_vector_db_from_doc(url:str) -> FAISS:
    """
    Create a FAISS vector database from a PDF document.

    :param doc_url: URL or file path to the PDF document.
    :return: FAISS vector database or None if an error occurs.
    """
    try:
        loader = PyPDFLoader(url or '/Users/pravin/Desktop/0.2024/0.anish.internship/rbfs/rbfs-user-guides.pdf')
    except Exception as e:
        print(f"Error loading document: {e}")
        return None

    try:
        pages = loader.load_and_split()
        print(pages)
        #text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        #docs = text_splitter.split_documents(transcript)
        db = FAISS.from_documents(pages, embeddings)
        print(db)
        return db
    except Exception as e:
        print(f"Error creating vector database: {e}")
        return None

async def generate_response_to_query(db: FAISS, query: str, k: int = 4) -> str:
    """
    Generate a response to a query using a FAISS vector database.

    :param db: FAISS vector database.
    :param query: Query string.
    :param k: Number of similar documents to retrieve.
    :return: Response string or None if an error occurs.
    """
    try:
        docs = db.similarity_search(query, k=k)
        print(query)
        docs_page_content = " ".join([d.page_content for d in docs])
        #llm = OpenAI(model_name="gpt-3.5-turbo")
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

        system_message = SystemMessage(content="""
            You are Rtbrick's IQ AI assistant that can answer questions about Rtbrick's Technology from Documentation.
            Only use the factual information from the provided document to answer the question.
            If you feel like you don't have enough information to answer the question, say "I don't have enough data to provide the information".
            Your answers should be verbose and detailed.
        """)

        human_message = HumanMessage(content=f"""
            Answer the following question: {query}
            By searching the following document: {docs_page_content}
        """)
        response = await llm.agenerate([[system_message, human_message]])
        return response.generations[0][0].text.strip(), docs
    except Exception as e:
        print(f"Error generating response: {e}")
        return None
    '''  prompt = PromptTemplate(
            input_variables=["query", "docs"],
            template="""
            You are Rtbrick's IQ AI assistant that can answer questions about Rtbrick's Technology from Documentation.
            Answer the following question: {query}
            By searching the following document: {docs}
            Only use the factual information from the document to answer the question.
            If you feel like you don't have enough information to answer the question, say "I don't have enough data to provide the information".
            Your answers should be verbose and detailed.
            """,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        response = await chain.invoke({"query": query, "docs": docs_page_content})
        return response['text'].replace("\n", ""), docs
    except Exception as e:
        print(f"Error generating response: {e}")
        return None
        '''