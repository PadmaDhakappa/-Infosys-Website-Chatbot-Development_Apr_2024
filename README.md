# -Infosys-Website-Chatbot-Development_Apr_2024

## Overview

The Infosys Chatbot Development Project is designed to enhance user engagement by providing immediate and accurate responses to inquiries about Infosys services and offerings. This document provides a comprehensive overview of the project's structure, technologies employed, and the deployment methodology.

## Project Structure

Task 1: Web Scrapping The project began with the scrapping of the Infosys website using Beautiful Soup to extract data one level deep. This initial phase focused on capturing relevant content that could later be processed and utilized by the chatbot. The extracted data underwent thorough cleaning to ensure quality and relevance. Subsequently, the refined data was stored in a structured text file, ready for further processing.

Task 2: Insert and Retrieve Data from Qdrant (Data Vectorization and Storage) In the second phase, Qdrant vector database was used. The clean text data was converted into vectors using openai embedding method and then inserted into a Qdrant vector space. I explored multiple approaches for this task:
1.Using Qdrant Cloud with OpenAI.
2.Using Qdrant Image in Docker using Open AI.
3.Using sentence transformers to generate embeddings and qdrant server.
For each method, I implemented cosine similarity to fetch the most relevant text chunks from our vector database in response to user queries.

Task 3: Integration with Open AI GPT 3.5 (Response Generation) The retrieved text data served as input for the next layer of our system, where it was enhanced and converted into polished responses using the GPT-3.5 model. I tried this task in two distinct ways:
1.Using LangChain.
2.Without using LangChain.

Task 4: Interactive Streamlit User Interface The final component of our project was developing a user-friendly and interactive UI using Streamlit. This interface allows users to interact with the chatbot in a simple and effective manner, posing questions and receiving responses directly.

## Technologies Used
Beautiful Soup: For web scraping and data extraction.
Qdrant: Employed as a vector database to handle large-scale data with efficient retrieval capabilities.
OpenAI GPT-3.5: For generating intelligent and contextually appropriate responses.
Streamlit: Used to create an engaging and interactive user interface.
Docker: For containerization and simplifying the deployment process.
LangChain: To facilitate the integration of language models with application-specific logic.

## Conclusion
The Infosys Chatbot Development Project represents a significant advancement in automating customer service and information dissemination. By leveraging cutting-edge technologies and innovative approaches, we have developed a system that not only understands user inquiries but also provides insightful and accurate responses. This initiative not only improves user satisfaction but also sets a new standard in digital customer interaction for Infosys.
