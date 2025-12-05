# 🤖 RAG en Python avec Claude - Guide de démarrage rapide

## 🚀 Démarrage en 3 étapes

### 1️⃣ Installation

```bash
# Minimum (RAG simple)
pip install anthropic

# Complet (RAG avec embeddings)
pip install anthropic chromadb sentence-transformers
```

### 2️⃣ Configuration

```bash
# Définir votre clé API Anthropic
export ANTHROPIC_API_KEY='votre-clé-api'
```

Obtenez votre clé sur : https://console.anthropic.com/

### 3️⃣ Lancement

```bash
# Tester l'installation
python test_rag.py

# Utiliser l'assistant interactif
python rag_aoc_assistant.py

# Mode démo
python rag_aoc_assistant.py --demo
```

## 📁 Fichiers créés

| Fichier | Description |
|---------|-------------|
| `rag_example.py` | RAG simple avec recherche par mots-clés |
| `rag_advanced.py` | RAG avancé avec ChromaDB et embeddings |
| `rag_aoc_assistant.py` | ✨ Assistant interactif pour vos solutions AoC |
| `test_rag.py` | Script de test de l'installation |
| `RAG_GUIDE.md` | 📚 Guide complet et détaillé |
| `requirements_rag.txt` | Dépendances Python |

## ⚡ Exemples rapides

### RAG Simple

```python
from rag_example import SimpleRAG

rag = SimpleRAG()
rag.add_documents([
    "BFS parcourt en largeur",
    "DFS parcourt en profondeur"
])

answer = rag.query("Quel algorithme pour explorer un graphe ?")
print(answer)
```

### RAG Avancé (avec embeddings)

```python
from rag_advanced import AdvancedRAG

rag = AdvancedRAG()
rag.add_documents([
    "La programmation dynamique optimise les sous-problèmes",
    "Dijkstra trouve le plus court chemin"
])

result = rag.query("Comment optimiser un algorithme ?")
print(result['answer'])
```

### Assistant pour vos solutions AoC

```python
from rag_aoc_assistant import AoCRAGAssistant

assistant = AoCRAGAssistant()
assistant.load_solutions()  # Charge day*_2025.md et day*_2025.py

result = assistant.ask("Quels algorithmes j'ai utilisés ?")
print(result['answer'])
```

## 🎯 Cas d'usage

- 💡 Interroger vos solutions passées
- 🔍 Trouver des patterns réutilisables
- 📊 Analyser vos approches
- 🚀 Générer des idées pour nouveaux problèmes
- 📚 Créer une base de connaissances personnelle

## 🆘 Dépannage

### Erreur : "No module named 'anthropic'"
```bash
pip install anthropic
```

### Erreur : "Invalid API key"
```bash
export ANTHROPIC_API_KEY='votre-clé'
```

### Aucune solution trouvée
Assurez-vous d'avoir des fichiers `day*_2025.md` ou `day*_2025.py` dans le répertoire.

## 📖 Pour aller plus loin

Consultez **RAG_GUIDE.md** pour :
- Architecture détaillée d'un RAG
- Comparaison des différentes approches
- Intégration avec LangChain
- Bases vectorielles alternatives
- Bonnes pratiques
- Exercices pratiques

## 💡 Questions fréquentes

**Q: Quelle différence entre rag_example.py et rag_advanced.py ?**

A:
- `rag_example.py` : Simple, rapide, recherche par mots-clés
- `rag_advanced.py` : Précis, recherche sémantique avec embeddings

**Q: Combien coûte l'utilisation de Claude ?**

A: Environ 0.003$/1K tokens pour Sonnet. Une requête typique = ~500-2000 tokens = $0.001-0.006

**Q: Puis-je utiliser un autre LLM que Claude ?**

A: Oui ! Vous pouvez adapter le code pour OpenAI GPT, Mistral, ou des modèles locaux (Ollama).

**Q: Le RAG fonctionne-t-il hors ligne ?**

A: La partie retrieval (ChromaDB + embeddings locaux) oui. La génération (Claude) nécessite internet.

## 🎓 Tutoriel interactif

```bash
# Lancez l'assistant interactif
python rag_aoc_assistant.py

# Questions suggérées :
# - Quels algorithmes j'ai utilisés ?
# - Comment j'ai géré les grilles ?
# - Quels jours ont utilisé BFS/DFS ?
# - Résume la solution du jour X
```

## 📚 Ressources

- [Documentation Claude](https://docs.anthropic.com)
- [Guide Anthropic RAG](https://docs.anthropic.com/en/docs/build-with-claude/rag)
- [ChromaDB Docs](https://docs.trychroma.com)
- [LangChain Python](https://python.langchain.com)

---

**Créé pour Advent of Code 2025** 🎄

Pour toute question, consultez le guide complet dans `RAG_GUIDE.md`
