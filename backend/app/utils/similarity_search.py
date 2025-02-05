import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

def perform_similarity_search(query: str, id: str):
    load_dotenv()

    token = os.environ["GITHUB_TOKEN_3"]
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

    # Perform similarity search
    results = vector_store.similarity_search(query, k=6)
    return results

# Example usage
# if __name__ == "__main__":
#     query = "What does the meeting say about Community perceptions of tourism?"
#     results = perform_similarity_search(query, "10004")
#     for res in results:
#         print(f"* {res.page_content} [{res.metadata}]")