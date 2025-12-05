"""
Système RAG avancé avec embeddings vectoriels
"""

import os
from typing import List, Dict, Optional
import anthropic


# Exemple avec ChromaDB (base vectorielle locale)
try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("ChromaDB non disponible. Installez avec: pip install chromadb")


class AdvancedRAG:
    """
    RAG avancé avec embeddings vectoriels et ChromaDB
    """

    def __init__(
        self,
        api_key: str = None,
        collection_name: str = "aoc_knowledge",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialise le système RAG avancé

        Args:
            api_key: Clé API Anthropic
            collection_name: Nom de la collection ChromaDB
            embedding_model: Modèle d'embedding à utiliser
        """
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB requis. Installez avec: pip install chromadb")

        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=self.api_key)

        # Initialiser ChromaDB
        self.chroma_client = chromadb.Client()

        # Fonction d'embedding (utilise SentenceTransformers)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )

        # Créer ou récupérer la collection
        try:
            self.collection = self.chroma_client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
        except:
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )

    def add_documents(
        self,
        documents: List[str],
        metadata: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ):
        """
        Ajoute des documents à la base vectorielle

        Args:
            documents: Liste de textes à indexer
            metadata: Métadonnées optionnelles pour chaque document
            ids: IDs optionnels pour chaque document
        """
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]

        if metadata is None:
            metadata = [{} for _ in documents]

        self.collection.add(
            documents=documents,
            metadatas=metadata,
            ids=ids
        )

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Récupère les documents les plus pertinents via recherche vectorielle

        Args:
            query: Question de l'utilisateur
            top_k: Nombre de documents à retourner

        Returns:
            Liste des documents les plus pertinents
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        # Formater les résultats
        documents = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                documents.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                })

        return documents

    def query(
        self,
        question: str,
        top_k: int = 3,
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.7
    ) -> Dict[str, any]:
        """
        Pose une question et obtient une réponse générée par Claude

        Args:
            question: Question de l'utilisateur
            top_k: Nombre de documents à récupérer
            model: Modèle Claude à utiliser
            temperature: Température pour la génération

        Returns:
            Dictionnaire contenant la réponse et les documents sources
        """
        # Récupération des documents pertinents
        relevant_docs = self.retrieve(question, top_k)

        if not relevant_docs:
            return {
                "answer": "Aucun document pertinent trouvé dans la base de connaissances.",
                "sources": [],
                "confidence": "low"
            }

        # Construction du contexte
        context = "\n\n".join([
            f"Document {i+1} (similarité: {1-doc.get('distance', 0):.2f}):\n{doc['content']}"
            for i, doc in enumerate(relevant_docs)
        ])

        # Construction du prompt pour Claude
        prompt = f"""Tu es un assistant expert qui répond aux questions en te basant sur des documents fournis.

Documents de référence:
{context}

Question: {question}

Instructions:
1. Réponds uniquement en te basant sur les documents fournis
2. Si l'information n'est pas dans les documents, dis-le clairement
3. Cite les numéros de documents utilisés dans ta réponse
4. Sois précis et concis"""

        # Appel à Claude
        message = self.client.messages.create(
            model=model,
            max_tokens=2048,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return {
            "answer": message.content[0].text,
            "sources": relevant_docs,
            "model": model,
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens
            }
        }

    def clear_collection(self):
        """Supprime tous les documents de la collection"""
        self.chroma_client.delete_collection(name=self.collection.name)
        self.collection = self.chroma_client.create_collection(
            name=self.collection.name,
            embedding_function=self.embedding_function
        )


# Exemple d'utilisation
def load_aoc_solutions():
    """
    Charge les solutions d'Advent of Code du répertoire actuel
    """
    import glob

    documents = []
    metadata = []

    # Lire tous les fichiers markdown
    for md_file in glob.glob("day*_2025.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                documents.append(content)
                metadata.append({
                    "source": md_file,
                    "type": "solution"
                })
        except Exception as e:
            print(f"Erreur lecture {md_file}: {e}")

    return documents, metadata


def example_usage():
    """
    Exemple d'utilisation du RAG avancé
    """
    if not CHROMADB_AVAILABLE:
        print("ChromaDB non installé. Installez avec: pip install chromadb")
        return

    print("=== RAG Avancé avec Embeddings Vectoriels ===\n")

    # Initialiser le RAG
    rag = AdvancedRAG(collection_name="aoc_2025")

    # Charger les solutions AoC existantes
    print("Chargement des solutions Advent of Code...")
    documents, metadata = load_aoc_solutions()

    if documents:
        rag.add_documents(documents, metadata)
        print(f"✓ {len(documents)} documents indexés\n")

        # Poser des questions
        questions = [
            "Quels algorithmes ont été utilisés pour résoudre les problèmes ?",
            "Comment gérer les grilles en Python ?",
            "Quelle est la complexité des solutions proposées ?"
        ]

        for question in questions:
            print(f"Q: {question}")
            try:
                result = rag.query(question, top_k=2)
                print(f"R: {result['answer']}")
                print(f"Sources: {[s['metadata'].get('source', 'unknown') for s in result['sources']]}")
                print(f"Tokens: {result['usage']}\n")
            except Exception as e:
                print(f"Erreur: {e}\n")
    else:
        print("Aucune solution trouvée. Ajoutez des fichiers day*_2025.md")

        # Exemple avec des documents fictifs
        print("\nUtilisation de documents d'exemple...\n")

        sample_docs = [
            "Python dispose de nombreuses structures de données: listes, tuples, dictionnaires, sets. "
            "Les listes sont mutables, les tuples immutables.",

            "Pour Advent of Code, les algorithmes classiques sont utiles: BFS, DFS, Dijkstra, "
            "programmation dynamique, backtracking.",

            "Les compréhensions de listes en Python sont très efficaces: "
            "[x*2 for x in range(10) if x % 2 == 0]"
        ]

        rag.add_documents(sample_docs)

        result = rag.query("Quelles structures de données Python dois-je connaître ?")
        print(f"R: {result['answer']}\n")


if __name__ == "__main__":
    example_usage()
