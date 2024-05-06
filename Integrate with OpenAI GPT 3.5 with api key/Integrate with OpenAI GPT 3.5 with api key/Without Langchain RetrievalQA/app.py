#Working Perfect without using Langchain

from qdrant_client import QdrantClient
from langchain.text_splitter import CharacterTextSplitter
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
import os
import openai
import uuid
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
 

openai.api_key = "sk-proj-8pP0fhGelhxLvNFX1ayLT3BlbkFJPFBdk2I4LfCmaCiRBEQE"

# initialising the client
client = QdrantClient(url="http://localhost:6333")

def create_collection():
    client.create_collection(
        collection_name="Infosys_db",
        vectors_config=VectorParams(size=1536, distance=Distance.DOT),
    )

#code to read from text file
def read_data_from_text():
    with open("infosys_data.txt", 'r', encoding='utf-8') as file:
        text = file.read()
    return text

#code for making text into chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator=" ",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

#code for convert chunks into embeddings
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

def add_vectors(embeddings):
    operation_info = client.upsert(
    collection_name="Infosys_db",
    wait=True,
    points=embeddings
)
    
def create_answer_with_context(query):
    response = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )
    embeddings = response['data'][0]['embedding']

    search_result = client.search(
        collection_name="Infosys_db",
        query_vector=embeddings,
        limit=1
    )

    if search_result == "":
        return ("I don't know.")
    else:
        prompt = "Context:\n"
        for result in search_result:
            prompt += result.payload['text'] + "\n---\n"
        prompt += "Question:" + query + "\n---\n" + "Answer:"

    
    
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
            )

        return completion.choices[0].message.content


def main():
  
  get_raw_text=read_data_from_text()
  chunks=get_text_chunks(get_raw_text)
  vectors=get_embedding(chunks)
  #create_collection()
  #print("Done creating Collection")
  #add_vectors(vectors)
  #print("Done Inserting Data")
  print("_______________________________")
  print("Welcome to Infosys Chatbot. Type quit to exit.")
  print("_______________________________")
  while True:
    question = input("Human: ")
    if question.lower() == "quit":
        break
    answer = create_answer_with_context(question)
    print("\nAI: ", answer)
    print("\n_______________________________")

if __name__ == '__main__':
    main()