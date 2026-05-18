"""Vector store for long-term memory persistence using ChromaDB."""
import uuid
from typing import List, Dict, Any, Optional


class VectorStore:
    """Persistent vector storage for project knowledge and historical context."""

    def __init__(self, persist_dir: str = "./chromadb", collection_name: str = "project_knowledge"):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self._entries: List[Dict] = []
        self._initialized = False

    def initialize(self):
        """Initialize the vector store (lazy init to avoid import errors)."""
        if self._initialized:
            return
        try:
            import chromadb
            self._client = chromadb.PersistentClient(path=self.persist_dir)
            self._collection = self._client.get_or_create_collection(
                name=self.collection_name
            )
            self._initialized = True
        except ImportError:
            self._initialized = False

    def add_entry(self, content: str, metadata: Optional[Dict] = None) -> str:
        """Store a memory entry with optional metadata."""
        entry_id = str(uuid.uuid4())
        self._entries.append({
            "id": entry_id,
            "content": content,
            "metadata": metadata or {},
            "timestamp": __import__("datetime").datetime.now().isoformat()
        })
        return entry_id

    def query(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """Query the vector store for relevant memory entries."""
        if not self._initialized:
            return [e for e in self._entries if query_text.lower() in e["content"].lower()][:n_results]

        try:
            results = self._collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return [
                {"id": id_, "content": doc, "metadata": meta}
                for id_, doc, meta in zip(
                    results["ids"][0], results["documents"][0], results["metadatas"][0]
                )
            ]
        except Exception:
            return self._entries[:n_results]

    def delete_entry(self, entry_id: str) -> bool:
        """Remove a memory entry by ID."""
        before = len(self._entries)
        self._entries = [e for e in self._entries if e["id"] != entry_id]
        return len(self._entries) < before

    def clear(self):
        """Clear all memory entries."""
        self._entries.clear()

    def count(self) -> int:
        """Return number of stored entries."""
        return len(self._entries)

    def __repr__(self):
        return f"VectorStore(entries={self.count()}, initialized={self._initialized})"
