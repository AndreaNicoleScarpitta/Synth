import chromadb
from chromadb.config import Settings
import uuid
from typing import List, Dict, Any, Optional
import os
import tempfile

class VectorStore:
    """ChromaDB-based vector store for literature and document storage"""
    
    def __init__(self, collection_name: str = "literature_documents"):
        # Use persistent storage in a temporary directory
        self.persist_directory = os.path.join(tempfile.gettempdir(), "ehr_generator_chroma")
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        self.collection_name = collection_name
        self.collection = None
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize or get the collection"""
        try:
            # Try to get existing collection
            self.collection = self.client.get_collection(name=self.collection_name)
        except Exception:
            # Create new collection if it doesn't exist
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Literature documents for RAG"}
            )
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Add documents to the vector store
        
        Args:
            documents: List of dictionaries with 'content' and 'metadata' keys
        """
        if not documents:
            return
        
        try:
            # Prepare data for ChromaDB
            ids = []
            contents = []
            metadatas = []
            
            for doc in documents:
                # Generate unique ID if not provided
                doc_id = doc.get('id', str(uuid.uuid4()))
                ids.append(doc_id)
                contents.append(doc['content'])
                
                # Ensure metadata is JSON serializable
                metadata = doc.get('metadata', {})
                # Convert any datetime objects to strings
                for key, value in metadata.items():
                    if hasattr(value, 'isoformat'):
                        metadata[key] = value.isoformat()
                    elif value is None:
                        metadata[key] = ""
                
                metadatas.append(metadata)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=contents,
                metadatas=metadatas
            )
            
            print(f"Added {len(documents)} documents to vector store")
            
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            raise
    
    def similarity_search(self, query: str, top_k: int = 5, 
                         filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Perform similarity search on the vector store
        
        Args:
            query: Search query text
            top_k: Number of top results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of search results with content and metadata
        """
        try:
            # Perform query
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    result = {
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None,
                        'id': results['ids'][0][i] if results['ids'] else None
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            print(f"Error performing similarity search: {e}")
            return []
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID"""
        try:
            results = self.collection.get(ids=[doc_id])
            
            if results['documents']:
                return {
                    'id': doc_id,
                    'content': results['documents'][0],
                    'metadata': results['metadatas'][0] if results['metadatas'] else {}
                }
            
            return None
            
        except Exception as e:
            print(f"Error getting document {doc_id}: {e}")
            return None
    
    def update_document(self, doc_id: str, content: str, metadata: Dict[str, Any]):
        """Update an existing document"""
        try:
            # Ensure metadata is JSON serializable
            for key, value in metadata.items():
                if hasattr(value, 'isoformat'):
                    metadata[key] = value.isoformat()
                elif value is None:
                    metadata[key] = ""
            
            self.collection.update(
                ids=[doc_id],
                documents=[content],
                metadatas=[metadata]
            )
            
        except Exception as e:
            print(f"Error updating document {doc_id}: {e}")
            raise
    
    def delete_document(self, doc_id: str):
        """Delete a document by ID"""
        try:
            self.collection.delete(ids=[doc_id])
        except Exception as e:
            print(f"Error deleting document {doc_id}: {e}")
            raise
    
    def delete_documents_by_metadata(self, filter_metadata: Dict[str, Any]):
        """Delete documents matching metadata filter"""
        try:
            self.collection.delete(where=filter_metadata)
        except Exception as e:
            print(f"Error deleting documents by metadata: {e}")
            raise
    
    def get_collection_size(self) -> int:
        """Get the number of documents in the collection"""
        try:
            return self.collection.count()
        except Exception as e:
            print(f"Error getting collection size: {e}")
            return 0
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        try:
            # Delete the collection and recreate it
            self.client.delete_collection(name=self.collection_name)
            self._initialize_collection()
            print("Collection cleared successfully")
        except Exception as e:
            print(f"Error clearing collection: {e}")
    
    def list_collections(self) -> List[str]:
        """List all available collections"""
        try:
            collections = self.client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            print(f"Error listing collections: {e}")
            return []
    
    def get_documents_by_source(self, source: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get documents by source (e.g., 'pubmed', 'biorxiv')"""
        try:
            results = self.collection.get(
                where={"source": source},
                limit=limit
            )
            
            documents = []
            if results['documents']:
                for i in range(len(results['documents'])):
                    doc = {
                        'id': results['ids'][i],
                        'content': results['documents'][i],
                        'metadata': results['metadatas'][i] if results['metadatas'] else {}
                    }
                    documents.append(doc)
            
            return documents
            
        except Exception as e:
            print(f"Error getting documents by source: {e}")
            return []
    
    def search_by_author(self, author_name: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Search for documents by author name"""
        try:
            # Use text search on author field
            results = self.collection.query(
                query_texts=[author_name],
                n_results=top_k,
                where={"authors": {"$contains": author_name}}
            )
            
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    result = {
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None,
                        'id': results['ids'][0][i] if results['ids'] else None
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            print(f"Error searching by author: {e}")
            # Fallback to general similarity search
            return self.similarity_search(author_name, top_k)
    
    def get_recent_documents(self, days: int = 30, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recently added documents"""
        try:
            from datetime import datetime, timedelta
            
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            results = self.collection.get(
                where={"publication_date": {"$gte": cutoff_date}},
                limit=limit
            )
            
            documents = []
            if results['documents']:
                for i in range(len(results['documents'])):
                    doc = {
                        'id': results['ids'][i],
                        'content': results['documents'][i],
                        'metadata': results['metadatas'][i] if results['metadatas'] else {}
                    }
                    documents.append(doc)
            
            return documents
            
        except Exception as e:
            print(f"Error getting recent documents: {e}")
            return []
    
    def backup_collection(self, backup_path: str):
        """Backup the collection to a file"""
        try:
            # Get all documents
            results = self.collection.get()
            
            backup_data = {
                'collection_name': self.collection_name,
                'documents': [],
                'backup_timestamp': datetime.now().isoformat()
            }
            
            if results['documents']:
                for i in range(len(results['documents'])):
                    doc = {
                        'id': results['ids'][i],
                        'content': results['documents'][i],
                        'metadata': results['metadatas'][i] if results['metadatas'] else {}
                    }
                    backup_data['documents'].append(doc)
            
            # Save to file
            import json
            with open(backup_path, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            print(f"Collection backed up to {backup_path}")
            
        except Exception as e:
            print(f"Error backing up collection: {e}")
            raise
    
    def restore_collection(self, backup_path: str):
        """Restore collection from a backup file"""
        try:
            import json
            
            with open(backup_path, 'r') as f:
                backup_data = json.load(f)
            
            # Clear existing collection
            self.clear_collection()
            
            # Add backed up documents
            if backup_data.get('documents'):
                self.add_documents(backup_data['documents'])
            
            print(f"Collection restored from {backup_path}")
            
        except Exception as e:
            print(f"Error restoring collection: {e}")
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            total_docs = self.get_collection_size()
            
            # Get documents by source
            sources = {}
            try:
                all_docs = self.collection.get()
                if all_docs['metadatas']:
                    for metadata in all_docs['metadatas']:
                        source = metadata.get('source', 'unknown')
                        sources[source] = sources.get(source, 0) + 1
            except Exception:
                sources = {"unknown": total_docs}
            
            return {
                'total_documents': total_docs,
                'sources': sources,
                'collection_name': self.collection_name,
                'persist_directory': self.persist_directory
            }
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                'total_documents': 0,
                'sources': {},
                'collection_name': self.collection_name,
                'persist_directory': self.persist_directory,
                'error': str(e)
            }
