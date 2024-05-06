from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient,models
from qdrant_client.http.models import PointStruct
import os
import openai
import uuid
openai.api_key = "sk-proj-8pP0fhGelhxLvNFX1ayLT3BlbkFJPFBdk2I4LfCmaCiRBEQE"



connection = QdrantClient(
    url="https://187ead95-7d2a-4178-b298-248ca77123ab.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key="Y8MvNuIN34Av0MthxQLaUHAjpg2beAjExVDLAP5Ovo-MIY7q1FTa-g",
)
'''

# #create new cluster in qdrant
record=0
connection.recreate_collection(
    collection_name="Infosys_Database_On_Qdrant_Cloud",
    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
)
print("Create collection reponse:", connection)

info = connection.get_collection(collection_name="Infosys_Database_On_Qdrant_Cloud")

print("Collection info:", info)
for get_info in info:
  print(get_info)'''


def read_data_from_text():
    with open("infosys_data.txt", 'r', encoding='utf-8') as file:
        text = file.read()
    return text

#code for making text into chunks

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator=" ",
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# #code for convert chunks into embeddings
def get_embedding(text_chunks, model_id="text-embedding-ada-002"):
    points = []
    for idx, chunk in enumerate(text_chunks):
        response = openai.Embedding.create(
            input=chunk,
            model=model_id
        )
        embeddings = response['data'][0]['embedding']
        point_id = str(uuid.uuid4())  # Generate a unique ID for the point

        points.append(PointStruct(id=point_id, vector=embeddings, payload={"text": chunk}))

    return points


# # code for insert data into qdrant database

def insert_data(get_points):
    operation_info = connection.upsert(
    collection_name="Infosys_Database_On_Qdrant_Cloud",
    wait=True,
    points=get_points
)


# code for searching
def create_answer_with_context(query):
    response = openai.Embedding.create(
        input=query,

        model="text-embedding-ada-002"
    )
    embeddings = response['data'][0]['embedding']

    search_result = connection.search(
        collection_name="Infosys_Database_On_Qdrant_Cloud",
        query_vector=embeddings,
        limit=1
    )
    return search_result

def main():
  get_raw_text=read_data_from_text()
  chunks=get_text_chunks(get_raw_text)
  vectors=get_embedding(chunks)
  #print("Done creating the Database on the cloud")
  #insert_data(vectors)
  #print("Done Inserting Data on the Cloud")
  question="Who are Infosys clients?"
  answer=create_answer_with_context(question)
  print("\n_______________________________")
  print("\n",question)
  print("\n_______________________________")
  print("\n The answer extracted from the Qdrant cloud is:\n", answer)

if __name__ == '__main__':
    main()

