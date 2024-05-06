import openai
from langchain_community.document_loaders.text import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain import hub

# Set your OpenAI API key
openai.api_key = "sk-proj-8pP0fhGelhxLvNFX1ayLT3BlbkFJPFBdk2I4LfCmaCiRBEQE"

# Loads the latest version
prompt = hub.pull("rlm/rag-prompt", api_url="https://api.hub.langchain.com")



raw_documents = TextLoader(r"C:\Users\dhaka\Desktop\QA\infosys_data.txt", encoding='utf-8').load()
text_splitter = CharacterTextSplitter(separator=" ", chunk_size=1000, chunk_overlap=200)
documents = text_splitter.split_documents(raw_documents)

# Store splits
vectorstore = Qdrant.from_documents(documents=documents, embedding=OpenAIEmbeddings(openai_api_key="sk-proj-8pP0fhGelhxLvNFX1ayLT3BlbkFJPFBdk2I4LfCmaCiRBEQE"))

#LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0,openai_api_key="sk-proj-8pP0fhGelhxLvNFX1ayLT3BlbkFJPFBdk2I4LfCmaCiRBEQE")

# RetrievalQA
qa_chain = RetrievalQA.from_chain_type(
    llm, retriever=vectorstore.as_retriever(), chain_type_kwargs={"prompt": prompt}
)

print("_______________________________")
print("Welcome to Infosys Chatbot. Type quit to exit.")
print("_______________________________")
while True:
    question = input("Human: ")
    if question.lower() == "quit":
        break
    result = qa_chain.invoke({"query": question})
    if result["result"] == "":
        print("\nAI: I don't know.")
    else:
        print("\nAI: ", result["result"])
    
    print("\n_______________________________")
    