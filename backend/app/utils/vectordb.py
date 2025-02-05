from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.docstore.document import Document

import os
import json
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from uuid import uuid4


def create_vector_db(id: str):
    load_dotenv()

    token = os.environ["GITHUB_TOKEN_1"]
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "text-embedding-3-large"
    base_path = os.path.dirname(__file__)
    directory = os.path.join(base_path, "..", "..", "data", id, "chroma_langchain_db")

    embeddings = OpenAIEmbeddings(
        model=model_name,
        base_url=endpoint,
        api_key=token,
    )

    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=embeddings,
        persist_directory=directory,  # Where to save data locally, remove if not necessary
    )

    # Load document
    json_path = os.path.join(base_path, "..", "..", "data", id, "result.json")
    with open(json_path, "r") as file:
        data = json.load(file)

    def split_text_into_chunks(text, chunk_size=1000):
        """
        Split text into chunks of specified size.
        """
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # Extract text content from the JSON data
    document_text = data["transcription"]
    subjects = data.get("subject", "")

    # Split subjects into chunks
    subject_chunks = split_text_into_chunks(subjects)

    documents = [Document(page_content=document_text)] + [Document(page_content=chunk) for chunk in subject_chunks]

    # Split the text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    chunks = text_splitter.split_documents(documents)

    uuids = [str(uuid4()) for _ in range(len(chunks))]

    vector_store.add_documents(documents=chunks, ids=uuids)

#     results = vector_store.similarity_search(
#         "what does the meeting say about Community perceptions of tourism",
#         k=6,
#     )
#     for res in results:
#         print(f"* {res.page_content} [{res.metadata}]")

# create_vector_db("9")