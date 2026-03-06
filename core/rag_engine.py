import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

class RAGEngine:
    def __init__(self, db_dir="chroma_db", embedding_model="nomic-embed-text"):
        """Initialize the RAG engine with ChromaDB and Ollama embeddings."""
        self.db_dir = db_dir
        self.embedding_model = embedding_model
        
        # Initialize Ollama embeddings
        self.embeddings = OllamaEmbeddings(model=self.embedding_model)
        
        # Initialize or load ChromaDB
        self.vector_store = Chroma(
            collection_name="joy_knowledge_base",
            embedding_function=self.embeddings,
            persist_directory=self.db_dir
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )

    def load_and_index_document(self, file_path):
        """Loads a document (PDF or TXT), splits it, and adds it to the vector store."""
        try:
            if not os.path.exists(file_path):
                return False, f"File not found: {file_path}"

            # 1. Load document
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension in ['.txt', '.md', '.csv']:
                loader = TextLoader(file_path, encoding='utf-8')
            else:
                return False, f"Unsupported file type: {file_extension}. Only PDF and TXT are supported."
                
            documents = loader.load()

            # 2. Split text
            chunks = self.text_splitter.split_documents(documents)
            
            # Add source metadata just in case
            for chunk in chunks:
                chunk.metadata['source'] = os.path.basename(file_path)

            # 3. Add to vector store
            if chunks:
                self.vector_store.add_documents(chunks)
                return True, f"Successfully indexed {len(chunks)} chunks from {os.path.basename(file_path)}."
            else:
                return False, "No valid text found in the document to index."
                
        except Exception as e:
            print(f"Error indexing document {file_path}: {e}")
            return False, f"Error indexing document: {str(e)}"

    def retrieve_context(self, query, k=3):
        """Retrieves relevant contexts for a given query."""
        try:
            # Check if we have any documents
            if self.vector_store._collection.count() == 0:
                print("Vector store is empty.")
                return ""
                
            docs = self.vector_store.similarity_search(query, k=k)
            
            if not docs:
                return ""
                
            # Combine the texts
            context = "\n---\n".join([f"[출처: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}" for doc in docs])
            return context
            
        except Exception as e:
            print(f"Error during retrieval: {e}")
            return ""

    def clear_database(self):
        """Clears the entire knowledge base."""
        try:
            # ChromaDB doesn't have a direct clear method, so we delete and recreate
            self.vector_store.delete_collection()
            
            # Recreate with same config
            self.vector_store = Chroma(
                collection_name="joy_knowledge_base",
                embedding_function=self.embeddings,
                persist_directory=self.db_dir
            )
            return True, "Knowledge base cleared successfully."
        except Exception as e:
            return False, f"Error clearing knowledge base: {str(e)}"
