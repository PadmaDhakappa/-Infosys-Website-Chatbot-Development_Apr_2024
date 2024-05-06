from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Qdrant
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


loader = TextLoader("scraped_data.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
print(docs[0])




loader = TextLoader("scraped_data.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
print(docs[0])


model_name="BAAI/bge-large-en"
model_kwargs={'device':'cpu'}
encode_kwargs={'normalize_embeddings':False}

embeddings=HuggingFaceBgeEmbeddings(
model_name=model_name,
model_kwargs=model_kwargs,
encode_kwargs=encode_kwargs,
)
print("Embedding Model Loaded")

url="http://localhost:6333"
collection_name='infosys_db'

qdrant = Qdrant.from_documents(
    docs,
    embeddings,
    url=url,
    collection_name=collection_name,
)
print('Qdrant Index Created')


query = "How is the future being shaped at Infosys?"
found_docs = qdrant.similarity_search_with_score(query)
document, score = found_docs[0]
print("################################")
print(query)
print("----------------------")
print(' '.join(document.page_content.split()))
print("----------------------")
print(f"Score: {score}")