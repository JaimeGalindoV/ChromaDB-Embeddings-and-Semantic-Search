import json
import requests
import argparse


from urllib.parse import urljoin

BASE_URL = "http://localhost:8000"
KNOWLEDGE_ENDPOINT = "knowledge"
QUERY_ENDPOINT = "query"

# Create a new collection(s) in ChromaDB
def upload_documents(file_path):
    endpoint = urljoin(BASE_URL, KNOWLEDGE_ENDPOINT)
    try:
        contents = []
        metadatas = []
        data = {}
        # Read the JSON file and extract the contents and metadata
        with open(file_path, 'r') as file:
            documents = json.load(file)
            for doc in documents:
                contents.append(doc["content"])
                metadatas.append(doc["metadata"])
            data["contents"] = contents
            data["metadata"] = metadatas
            # data = json.dumps(data)
            # Send the data to the API
            response = requests.post(endpoint, json=data)
        if response.status_code == 200:
            print("Document uploaded successfully.")
        else:
            print(f"Failed to upload documents:\nStatus code: {response.status_code}\n Details: {response.json()}")
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")

# Chat with the bot using a query (not necessary to obtain the top 4 matching documents from the collection, but useful and kul)
def chat_query(query):
    endpoint = urljoin(BASE_URL, QUERY_ENDPOINT)
    # Send the query to the API
    response = requests.post(endpoint, json={'query': query})
    # Check the response status code
    if response.status_code == 200:
        answer = response.json().get('answer')
        documents = response.json().get('documents')
        documents = "\n".join(documents)
        # If the response is successful, print the bot answer and documents
        print(f"Documents/Context:\n{documents}")
        print(f"\nChatbot response:\n {answer}")
    else:
        print(f"Failed to get chat response.\nStatus code: {response.status_code}\n Details: {response.json()}")
 
def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="API Interaction Script")    
    subparsers = parser.add_subparsers(dest='action', required=True, help="Action to perform")

    # Subparser for upload action
    upload_parser = subparsers.add_parser('upload', help="Upload a document")
    upload_parser.add_argument('--path', required=True, help="Path of the document to upload")

    # Subparser for chat query action
    query_parser = subparsers.add_parser('query', help="Chat query")
    query_parser.add_argument('--query', required=True, help="Query string for the chat")

    args = parser.parse_args()

    if args.action == 'upload':
        upload_documents(args.path)
    elif args.action == 'query':
        chat_query(args.query)

    else:
        print("Invalid action. Please use 'upload', 'get', or 'query'.")


if __name__ == "__main__":
    main()