
import json
import falcon.asgi
import hashlib


from chromadb import Client
from chromadb.config import Settings 
from sentence_transformers import SentenceTransformer
from transformers import pipeline



# Initialize ChromaDB
client = Client(Settings())
collection = client.create_collection("JaimeGalindo_collection")

# Initialize Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load the model once at the application start
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")


def generate_id(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

class KnowledgeResource:
    async def on_post(self, req, resp):
        """
        Handle POST requests to upload new documents
        """
        try:
            raw_json = await req.bounded_stream.read()

            request_data = json.loads(raw_json)

            # # Extraer contents y metadatas
            documents = request_data["contents"]
            metadatas = request_data["metadata"]

            if len(documents) != len(metadatas):
                raise ValueError("Contents and metadata must have the same length.")

            doc_ids = []
            to_remove_idx = []


            # Generate document ids, check for duplication
            for i in range(len(documents)):
                doc_id = generate_id(documents[i])
                results = collection.get(ids=[doc_id])
                if not results or len(results["documents"]) == 0:
                    doc_ids.append(doc_id)
                else:
                    print(f"Document already exists, ignoring doc id:{doc_id}")
                    to_remove_idx.append(i)

            # Remove indexes of documents that already exist to avoid duplication
            for idx in sorted(to_remove_idx, reverse=True):
                del documents[idx]
                del metadatas[idx]
    
            # Upload documents
            if len(documents) > 0:
                embeddings = model.encode(documents)
                collection.add(ids=doc_ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_400

    async def on_get(self, req, resp):
        """
        Handle GET requests for a all documents
        """
        try:
            response = []
            knowledge = collection.get()
            # Return the documents
            ids  = knowledge["ids"]
            contents = knowledge["documents"]
            metadatas = knowledge["metadatas"]
            for i in range(len(ids)):
                response.append({
                    "id": ids[i],
                    "content": contents[i],
                    "metadata": metadatas[i]
                })

            resp.media = response
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_400

class QueryResource:
    async def on_post(self, req, resp):
        """
        Handle POST requests to answer queries
        """
        try:
            raw_json = await req.bounded_stream.read()
            request_data = json.loads(raw_json)

            # Extract query
            query = request_data.get("query", "")
            if not query:
                raise ValueError("Query cannot be empty.")

            # Generate query embedding
            query_embedding = model.encode(query)

            # Retrieve relevant documents from ChromaDB
            results = collection.query(query_embeddings=[query_embedding], n_results=4)

            # Extract documents
            documents = results["documents"][0]

            # Combine documents into a context
            context = " ".join(documents)

             # Validate context before passing to the QA pipeline
            if not context.strip():
                raise ValueError("No relevant information found.")

            # Generate response using QA pipeline
            response = qa_pipeline(question=query, context=context)

            # Extract the generated answer
            generated_response = response.get("answer", "No answer generated.")

            # Return the response
            resp.media = {
                "query": query,
                "documents": documents,
                "context": context,
                "answer": generated_response,
            }
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_400



# Initialize Falcon app
app = falcon.asgi.App()
app.add_route("/query", QueryResource())
app.add_route("/knowledge", KnowledgeResource())
