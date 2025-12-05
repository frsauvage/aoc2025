# Guide : Créer un RAG en Python avec Claude

## 📚 Qu'est-ce qu'un RAG ?

Un **RAG (Retrieval-Augmented Generation)** est un système qui combine :
- 🔍 **Recherche** de documents pertinents dans une base de connaissances
- 🤖 **Génération** de réponses avec Claude basées sur ces documents

## 🎯 Cas d'usage pour Advent of Code

- Interroger vos solutions passées
- Trouver des patterns et algorithmes réutilisables
- Générer des solutions basées sur vos approches précédentes
- Créer une base de connaissances de vos techniques

## 🚀 Installation

### Option 1 : RAG Simple (sans embeddings)

```bash
pip install anthropic
```

### Option 2 : RAG Avancé (avec embeddings vectoriels)

```bash
pip install anthropic chromadb sentence-transformers
```

### Configuration de la clé API

```bash
export ANTHROPIC_API_KEY='votre-clé-api-anthropic'
```

Ou dans un fichier `.env` :
```
ANTHROPIC_API_KEY=votre-clé-api-anthropic
```

## 📝 Exemples d'utilisation

### 1. RAG Simple (rag_example.py)

```python
from rag_example import SimpleRAG

# Initialiser
rag = SimpleRAG()

# Ajouter des documents
documents = [
    "Day 1 : Tri et comparaison de listes",
    "Day 2 : Validation de séquences",
    "Python tip : Utilisez collections.Counter pour compter"
]
rag.add_documents(documents)

# Poser une question
answer = rag.query("Comment compter des éléments en Python ?")
print(answer)
```

**Avantages** :
- ✅ Simple et rapide à mettre en place
- ✅ Pas de dépendances lourdes
- ✅ Bon pour petites bases de connaissances

**Inconvénients** :
- ❌ Recherche basique par mots-clés
- ❌ Moins précis pour documents similaires

### 2. RAG Avancé avec ChromaDB (rag_advanced.py)

```python
from rag_advanced import AdvancedRAG

# Initialiser avec embeddings
rag = AdvancedRAG(collection_name="mes_solutions")

# Ajouter des documents avec métadonnées
documents = [
    "La recherche en largeur (BFS) est idéale pour trouver le plus court chemin",
    "La programmation dynamique optimise les problèmes avec sous-structures"
]
metadata = [
    {"type": "algorithme", "difficulté": "medium"},
    {"type": "technique", "difficulté": "hard"}
]
rag.add_documents(documents, metadata)

# Requête avec sources
result = rag.query("Quel algorithme pour un plus court chemin ?", top_k=2)
print(f"Réponse : {result['answer']}")
print(f"Sources : {result['sources']}")
print(f"Tokens utilisés : {result['usage']}")
```

**Avantages** :
- ✅ Recherche sémantique (comprend le sens)
- ✅ Très précis même avec grandes bases
- ✅ Persistance des données
- ✅ Métadonnées et filtrage

**Inconvénients** :
- ❌ Dépendances supplémentaires
- ❌ Plus lent à initialiser

### 3. Utiliser vos solutions AoC existantes

```python
from rag_advanced import AdvancedRAG
import glob

rag = AdvancedRAG(collection_name="aoc_2025")

# Charger tous vos fichiers markdown
documents = []
metadata = []

for md_file in glob.glob("day*_2025.md"):
    with open(md_file, 'r') as f:
        content = f.read()
        documents.append(content)
        metadata.append({"source": md_file, "day": md_file.split('_')[0][3:]})

rag.add_documents(documents, metadata)

# Interroger vos solutions
result = rag.query("Quels jours ont utilisé BFS ou DFS ?")
print(result['answer'])
```

## 🏗️ Architecture d'un RAG

```
┌─────────────────────────────────────────────────────┐
│                   Votre Question                     │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              1. RETRIEVAL (Recherche)               │
│  ┌──────────────────────────────────────────────┐   │
│  │  Question → Embedding → Recherche vectorielle│   │
│  │  → Top K documents les plus similaires       │   │
│  └──────────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│         2. AUGMENTATION (Enrichissement)            │
│  ┌──────────────────────────────────────────────┐   │
│  │  Prompt = Question + Documents récupérés     │   │
│  └──────────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│           3. GENERATION (avec Claude)               │
│  ┌──────────────────────────────────────────────┐   │
│  │  Claude analyse le contexte et génère        │   │
│  │  une réponse basée sur vos documents         │   │
│  └──────────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
              Réponse finale
```

## 🔧 Personnalisation

### Changer le modèle d'embedding

```python
# Modèles locaux (gratuits)
rag = AdvancedRAG(embedding_model="all-mpnet-base-v2")  # Plus précis
rag = AdvancedRAG(embedding_model="all-MiniLM-L6-v2")   # Plus rapide

# Pour le français
rag = AdvancedRAG(embedding_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
```

### Changer le modèle Claude

```python
# Claude Sonnet (bon équilibre)
result = rag.query(question, model="claude-3-5-sonnet-20241022")

# Claude Opus (plus intelligent)
result = rag.query(question, model="claude-3-opus-20240229")

# Claude Haiku (plus rapide et économique)
result = rag.query(question, model="claude-3-5-haiku-20241022")
```

### Ajuster le nombre de documents

```python
# Plus de contexte (mais plus de tokens)
result = rag.query(question, top_k=5)

# Moins de contexte (plus rapide, moins cher)
result = rag.query(question, top_k=2)
```

## 💡 Bonnes pratiques

### 1. Découpage des documents

Pour de longs documents, découpez-les en chunks :

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Découpe un texte en morceaux avec chevauchement"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# Utilisation
long_doc = "..." # votre texte long
chunks = chunk_text(long_doc)
rag.add_documents(chunks, [{"source": "long_doc", "chunk": i} for i in range(len(chunks))])
```

### 2. Métadonnées utiles

```python
metadata = {
    "source": "day5_2025.py",
    "day": 5,
    "year": 2025,
    "difficulty": "medium",
    "algorithms": ["bfs", "graph"],
    "solved": True,
    "execution_time_ms": 45
}
```

### 3. Filtrage par métadonnées

```python
# Avec ChromaDB
results = rag.collection.query(
    query_texts=["algorithme de graphe"],
    n_results=3,
    where={"difficulty": "medium", "solved": True}
)
```

## 🚀 Aller plus loin

### Utiliser LangChain

```bash
pip install langchain langchain-anthropic langchain-community
```

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain.chains import RetrievalQA

# Setup
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(embedding_function=embeddings)
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Créer la chaîne RAG
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Utiliser
result = qa_chain({"query": "Comment résoudre un problème de graphe ?"})
```

### Bases vectorielles alternatives

- **FAISS** : Très rapide, développé par Meta
- **Pinecone** : Cloud, scalable (payant)
- **Weaviate** : Open source, features avancées
- **Qdrant** : Rust, très performant

### Embeddings alternatives

- **OpenAI** : Excellents mais payants
- **Voyage AI** : Spécialisés pour RAG
- **Cohere** : Bons pour multilingue
- **Local** : Sentence Transformers (gratuit)

## 📊 Comparaison des approches

| Critère | RAG Simple | RAG ChromaDB | LangChain |
|---------|-----------|--------------|-----------|
| Facilité | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Précision | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Performance | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Scalabilité | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Features | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🐛 Dépannage

### Erreur : "No such file or directory"

Vérifiez que vous êtes dans le bon répertoire :
```bash
cd /home/user/aoc2025
```

### Erreur : "Invalid API key"

Vérifiez votre clé API :
```bash
echo $ANTHROPIC_API_KEY
```

### ChromaDB ne trouve pas les documents

Supprimez et recréez la collection :
```python
rag.clear_collection()
rag.add_documents(documents)
```

### Résultats non pertinents

- Augmentez `top_k`
- Améliorez vos métadonnées
- Utilisez un meilleur modèle d'embedding
- Découpez mieux vos documents

## 📚 Ressources

- [Documentation Claude](https://docs.anthropic.com)
- [ChromaDB Docs](https://docs.trychroma.com)
- [LangChain Docs](https://python.langchain.com)
- [Sentence Transformers](https://www.sbert.net)

## 🎓 Exercices pratiques

1. **Basique** : Créez un RAG de vos solutions AoC 2025
2. **Intermédiaire** : Ajoutez des métadonnées (difficulté, algorithmes)
3. **Avancé** : Créez un système qui suggère des solutions basées sur l'énoncé
4. **Expert** : Intégrez avec un chatbot web (Streamlit/Gradio)

Bon apprentissage ! 🚀
