#!/usr/bin/env python3
"""
Assistant RAG pour Advent of Code 2025

Ce script charge automatiquement toutes vos solutions AoC et vous permet
de les interroger avec des questions en langage naturel.

Usage:
    python rag_aoc_assistant.py

    Puis posez des questions comme :
    - "Quels algorithmes j'ai utilisés jusqu'à présent ?"
    - "Comment j'ai géré les grilles ?"
    - "Quel jour était le plus difficile ?"
"""

import os
import sys
import glob
from typing import List, Dict, Tuple
import anthropic


class AoCRAGAssistant:
    """
    Assistant RAG spécialisé pour Advent of Code
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Clé API manquante. Définissez ANTHROPIC_API_KEY dans l'environnement "
                "ou passez-la en paramètre."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.knowledge_base = []

    def load_solutions(self, pattern: str = "day*_2025.md") -> int:
        """
        Charge toutes les solutions depuis les fichiers markdown

        Args:
            pattern: Pattern glob pour trouver les fichiers

        Returns:
            Nombre de fichiers chargés
        """
        files = sorted(glob.glob(pattern))
        count = 0

        for filepath in files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Extraire le numéro du jour
                    day_num = self._extract_day_number(filepath)

                    # Ajouter à la base de connaissances
                    self.knowledge_base.append({
                        "day": day_num,
                        "source": filepath,
                        "content": content,
                        "type": "markdown"
                    })
                    count += 1
                    print(f"✓ Chargé : {filepath}")

            except Exception as e:
                print(f"✗ Erreur avec {filepath}: {e}")

        # Charger aussi les fichiers Python
        py_files = sorted(glob.glob("day*_2025.py"))
        for filepath in py_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                    day_num = self._extract_day_number(filepath)

                    self.knowledge_base.append({
                        "day": day_num,
                        "source": filepath,
                        "content": content,
                        "type": "python"
                    })
                    count += 1
                    print(f"✓ Chargé : {filepath}")

            except Exception as e:
                print(f"✗ Erreur avec {filepath}: {e}")

        return count

    def _extract_day_number(self, filepath: str) -> int:
        """Extrait le numéro du jour depuis le nom de fichier"""
        try:
            # day4_2025.md -> 4
            basename = os.path.basename(filepath)
            day_str = basename.split('_')[0].replace('day', '')
            return int(day_str)
        except:
            return 0

    def retrieve_relevant_docs(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Récupère les documents les plus pertinents

        Cette version simple utilise la correspondance de mots-clés.
        Pour une version plus avancée, voir rag_advanced.py
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())

        # Scorer chaque document
        scored_docs = []
        for doc in self.knowledge_base:
            content_lower = doc['content'].lower()

            # Score basé sur :
            # 1. Nombre de mots de la requête présents
            # 2. Mentions directes dans le contenu
            score = 0

            # Compter les mots communs
            doc_words = set(content_lower.split())
            common_words = query_words & doc_words
            score += len(common_words) * 2

            # Bonus pour mentions explicites
            if "day " + str(doc['day']) in query_lower:
                score += 20

            # Bonus pour type de fichier demandé
            if "code" in query_lower or "python" in query_lower:
                if doc['type'] == 'python':
                    score += 10
            if "explication" in query_lower or "description" in query_lower:
                if doc['type'] == 'markdown':
                    score += 10

            if score > 0:
                scored_docs.append((score, doc))

        # Trier et retourner top_k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in scored_docs[:top_k]]

    def ask(
        self,
        question: str,
        top_k: int = 4,
        model: str = "claude-3-5-sonnet-20241022",
        verbose: bool = True
    ) -> Dict:
        """
        Pose une question sur vos solutions AoC

        Args:
            question: Votre question
            top_k: Nombre de documents à considérer
            model: Modèle Claude à utiliser
            verbose: Afficher les sources utilisées

        Returns:
            Dict avec 'answer' et 'sources'
        """
        if not self.knowledge_base:
            return {
                "answer": "⚠️  Base de connaissances vide. Chargez d'abord vos solutions avec load_solutions().",
                "sources": []
            }

        # Récupérer les documents pertinents
        relevant_docs = self.retrieve_relevant_docs(question, top_k)

        if not relevant_docs:
            return {
                "answer": "❌ Aucun document pertinent trouvé. Essayez de reformuler votre question.",
                "sources": []
            }

        if verbose:
            print(f"\n🔍 Documents trouvés : {[f"Day {d['day']} ({d['type']})" for d in relevant_docs]}")

        # Construire le contexte
        context_parts = []
        for i, doc in enumerate(relevant_docs):
            context_parts.append(
                f"=== Document {i+1}: Day {doc['day']} ({doc['source']}) ===\n{doc['content']}\n"
            )
        context = "\n".join(context_parts)

        # Créer le prompt
        system_prompt = """Tu es un assistant expert en Advent of Code qui aide les développeurs
à comprendre et améliorer leurs solutions. Tu analyses le code Python et les explications fournies
pour répondre aux questions de manière précise et utile."""

        user_prompt = f"""Voici des solutions d'Advent of Code 2025 :

{context}

Question : {question}

Instructions :
- Réponds en te basant UNIQUEMENT sur les documents fournis
- Cite les jours (Day X) quand tu références une solution
- Si la réponse n'est pas dans les documents, dis-le clairement
- Sois précis et donne des exemples de code si pertinent
- Réponds en français"""

        # Appeler Claude
        try:
            message = self.client.messages.create(
                model=model,
                max_tokens=2048,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            answer = message.content[0].text

            # Informations d'usage
            usage_info = f"\n\n💰 Tokens: {message.usage.input_tokens} in / {message.usage.output_tokens} out"

            return {
                "answer": answer,
                "sources": relevant_docs,
                "usage": message.usage,
                "model": model
            }

        except Exception as e:
            return {
                "answer": f"❌ Erreur lors de l'appel à Claude : {e}",
                "sources": relevant_docs
            }

    def stats(self) -> Dict:
        """Retourne des statistiques sur la base de connaissances"""
        days = set(doc['day'] for doc in self.knowledge_base)
        types = {}
        for doc in self.knowledge_base:
            types[doc['type']] = types.get(doc['type'], 0) + 1

        return {
            "total_documents": len(self.knowledge_base),
            "unique_days": len(days),
            "days": sorted(days),
            "by_type": types
        }


def interactive_mode():
    """Mode interactif pour poser des questions"""
    print("=" * 60)
    print("🎄 Assistant RAG pour Advent of Code 2025 🎄")
    print("=" * 60)

    # Initialiser
    try:
        assistant = AoCRAGAssistant()
    except ValueError as e:
        print(f"\n❌ Erreur : {e}")
        print("\nPour définir votre clé API :")
        print("  export ANTHROPIC_API_KEY='votre-clé'")
        return

    # Charger les solutions
    print("\n📚 Chargement des solutions...\n")
    count = assistant.load_solutions()

    if count == 0:
        print("\n⚠️  Aucune solution trouvée (day*_2025.md ou day*_2025.py)")
        print("Créez d'abord des fichiers de solutions !")
        return

    # Afficher les stats
    stats = assistant.stats()
    print(f"\n✅ {stats['total_documents']} documents chargés")
    print(f"   - Jours : {stats['days']}")
    print(f"   - Types : {stats['by_type']}")

    # Suggestions de questions
    print("\n💡 Questions suggérées :")
    suggestions = [
        "Quels algorithmes j'ai utilisés ?",
        "Quels jours ont utilisé des graphes ?",
        "Comment j'ai optimisé mes solutions ?",
        "Quelles structures de données j'ai le plus utilisées ?",
        "Résume les solutions du jour X"
    ]
    for i, sugg in enumerate(suggestions, 1):
        print(f"   {i}. {sugg}")

    print("\n" + "=" * 60)
    print("Posez vos questions (tapez 'quit' pour quitter)")
    print("=" * 60)

    # Boucle interactive
    while True:
        try:
            question = input("\n❓ Question : ").strip()

            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Au revoir !")
                break

            if not question:
                continue

            if question.isdigit() and 1 <= int(question) <= len(suggestions):
                question = suggestions[int(question) - 1]
                print(f"   → {question}")

            # Obtenir la réponse
            result = assistant.ask(question, verbose=True)

            print(f"\n💬 Réponse :\n")
            print(result['answer'])

            if 'usage' in result:
                print(f"\n💰 Tokens utilisés : {result['usage'].input_tokens} in / {result['usage'].output_tokens} out")

        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"\n❌ Erreur : {e}")


def demo_mode():
    """Mode démo avec questions prédéfinies"""
    print("=" * 60)
    print("🎄 Mode Démo - Assistant RAG AoC 2025 🎄")
    print("=" * 60)

    assistant = AoCRAGAssistant()

    print("\n📚 Chargement des solutions...\n")
    count = assistant.load_solutions()

    if count == 0:
        print("⚠️  Aucune solution trouvée pour la démo")
        return

    stats = assistant.stats()
    print(f"\n✅ {stats['total_documents']} documents chargés")

    # Questions de démo
    demo_questions = [
        "Fais un résumé des solutions disponibles",
        "Quels sont les algorithmes et techniques utilisés ?",
        "Y a-t-il des patterns récurrents ?"
    ]

    for i, question in enumerate(demo_questions, 1):
        print(f"\n{'='*60}")
        print(f"Question {i}/{len(demo_questions)} : {question}")
        print('='*60)

        result = assistant.ask(question, verbose=True)
        print(f"\n{result['answer']}\n")

        if 'usage' in result:
            print(f"💰 Tokens : {result['usage'].input_tokens} in / {result['usage'].output_tokens} out")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_mode()
    else:
        interactive_mode()
