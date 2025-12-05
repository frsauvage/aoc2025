"""
Exemple de système RAG simple en Python avec Claude (Anthropic)
"""

import os
from typing import List, Dict
import anthropic


class SimpleRAG:
    """
    Système RAG basique utilisant:
    - Recherche simple par mots-clés (peut être amélioré avec des embeddings)
    - Claude pour la génération de réponses
    """

    def __init__(self, api_key: str = None):
        """
        Initialise le système RAG

        Args:
            api_key: Clé API Anthropic (si None, utilise ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.documents: List[Dict[str, str]] = []

    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """
        Ajoute des documents à la base de connaissances

        Args:
            documents: Liste de textes à indexer
            metadata: Métadonnées optionnelles pour chaque document
        """
        for i, doc in enumerate(documents):
            self.documents.append({
                "id": i,
                "content": doc,
                "metadata": metadata[i] if metadata and i < len(metadata) else {}
            })

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Récupère les documents les plus pertinents

        Cette implémentation simple utilise la correspondance de mots-clés.
        Pour un système plus avancé, utilisez des embeddings vectoriels.

        Args:
            query: Question de l'utilisateur
            top_k: Nombre de documents à retourner

        Returns:
            Liste des documents les plus pertinents
        """
        query_words = set(query.lower().split())

        # Score simple basé sur le nombre de mots communs
        scored_docs = []
        for doc in self.documents:
            doc_words = set(doc["content"].lower().split())
            score = len(query_words & doc_words)
            if score > 0:
                scored_docs.append((score, doc))

        # Trier par score décroissant et retourner top_k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in scored_docs[:top_k]]

    def query(self, question: str, top_k: int = 3, model: str = "claude-3-5-sonnet-20241022") -> str:
        """
        Pose une question et obtient une réponse générée par Claude

        Args:
            question: Question de l'utilisateur
            top_k: Nombre de documents à récupérer
            model: Modèle Claude à utiliser

        Returns:
            Réponse générée par Claude
        """
        # Récupération des documents pertinents
        relevant_docs = self.retrieve(question, top_k)

        if not relevant_docs:
            return "Aucun document pertinent trouvé dans la base de connaissances."

        # Construction du contexte
        context = "\n\n".join([
            f"Document {i+1}:\n{doc['content']}"
            for i, doc in enumerate(relevant_docs)
        ])

        # Construction du prompt pour Claude
        prompt = f"""Voici des documents pertinents pour répondre à la question:

{context}

Question: {question}

Réponds à la question en te basant uniquement sur les documents fournis ci-dessus.
Si l'information n'est pas dans les documents, dis-le clairement."""

        # Appel à Claude
        message = self.client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text


# Exemple d'utilisation avec les défis Advent of Code
def example_aoc_rag():
    """
    Exemple d'utilisation du RAG pour Advent of Code
    """
    # Initialiser le RAG
    rag = SimpleRAG()

    # Ajouter des documents (par exemple, des solutions de jours précédents)
    documents = [
        "Day 1 2025: Le problème consistait à comparer deux listes de nombres. "
        "La solution impliquait de trier les listes et calculer les différences.",

        "Day 2 2025: Il fallait analyser des rapports de niveaux. "
        "Chaque rapport est sûr si les niveaux sont soit tous croissants soit tous décroissants, "
        "avec des différences entre 1 et 3.",

        "Day 4 2025: Un problème de recherche de chemins dans une grille. "
        "Utilisation de BFS ou DFS pour trouver tous les chemins possibles.",

        "Python tips: Pour lire un fichier input, utilisez 'with open(filename) as f: lines = f.read().strip().split(\\n)'. "
        "Pour les grilles, utilisez des listes de listes ou numpy arrays."
    ]

    rag.add_documents(documents)

    # Poser des questions
    questions = [
        "Comment lire un fichier d'input en Python ?",
        "Quel était le problème du jour 2 ?",
        "Quels algorithmes sont utiles pour les grilles ?"
    ]

    print("=== Exemple RAG pour Advent of Code ===\n")

    for question in questions:
        print(f"Q: {question}")
        try:
            answer = rag.query(question)
            print(f"R: {answer}\n")
        except Exception as e:
            print(f"Erreur: {e}\n")


def example_with_embeddings():
    """
    Pour un RAG plus avancé avec embeddings vectoriels
    """
    print("\n=== RAG Avancé avec Embeddings ===\n")
    print("Pour un système plus performant, vous pouvez utiliser:")
    print("1. Voyage AI ou OpenAI pour les embeddings")
    print("2. ChromaDB, Pinecone ou FAISS pour la base vectorielle")
    print("3. LangChain pour simplifier l'orchestration")
    print("\nExemple avec LangChain:")
    print("""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import VoyageEmbeddings
from langchain_anthropic import ChatAnthropic

# Découper les documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# Créer la base vectorielle
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=VoyageEmbeddings()
)

# Créer le retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Utiliser Claude pour la génération
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
""")


if __name__ == "__main__":
    print("Pour utiliser ce script, assurez-vous d'avoir:")
    print("1. Installé la bibliothèque: pip install anthropic")
    print("2. Défini votre clé API: export ANTHROPIC_API_KEY='your-key'")
    print("\n")

    # Décommenter pour tester (nécessite une clé API)
    # example_aoc_rag()

    example_with_embeddings()
