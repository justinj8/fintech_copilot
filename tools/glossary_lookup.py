
import json
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

with open("data/fintech_glossary.json") as f:
    glossary = json.load(f)

texts = [f"{k}: {v}" for k,v in glossary.items()]
embedding_model = OpenAIEmbeddings()

def build_glossary_index():
    return FAISS.from_texts(texts, embedding_model)

def search_term(term):
    if not hasattr(search_term, "index"):
        search_term.index = build_glossary_index()
    index = search_term.index
    results = index.similarity_search(term, k=1)
    return results[0].page_content if results else "No glossary match found."
