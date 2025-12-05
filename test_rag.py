#!/usr/bin/env python3
"""
Script de test rapide pour vérifier que le RAG fonctionne
"""

import os
import sys


def test_imports():
    """Test des imports de base"""
    print("🧪 Test 1: Vérification des imports...")

    try:
        import anthropic
        print("  ✅ anthropic installé")
    except ImportError:
        print("  ❌ anthropic manquant - installez avec: pip install anthropic")
        return False

    # Optionnel
    try:
        import chromadb
        print("  ✅ chromadb installé (optionnel pour RAG avancé)")
    except ImportError:
        print("  ⚠️  chromadb non installé (optionnel)")

    return True


def test_api_key():
    """Test de la clé API"""
    print("\n🧪 Test 2: Vérification de la clé API...")

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("  ❌ ANTHROPIC_API_KEY non définie")
        print("\n  Pour la définir :")
        print("    export ANTHROPIC_API_KEY='votre-clé'")
        return False

    if not api_key.startswith("sk-ant-"):
        print("  ⚠️  Format de clé API suspect")

    print(f"  ✅ Clé API définie (longueur: {len(api_key)})")
    return True


def test_simple_rag():
    """Test du RAG simple"""
    print("\n🧪 Test 3: Test du RAG simple...")

    try:
        from rag_example import SimpleRAG

        rag = SimpleRAG()
        print("  ✅ SimpleRAG initialisé")

        # Ajouter des documents de test
        docs = [
            "Python est un langage de programmation",
            "BFS est un algorithme de parcours de graphe"
        ]
        rag.add_documents(docs)
        print(f"  ✅ {len(docs)} documents ajoutés")

        # Test de retrieval
        results = rag.retrieve("Python")
        print(f"  ✅ Retrieval fonctionne ({len(results)} résultats)")

        return True

    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False


def test_aoc_assistant():
    """Test de l'assistant AoC"""
    print("\n🧪 Test 4: Test de l'assistant AoC...")

    try:
        from rag_aoc_assistant import AoCRAGAssistant

        assistant = AoCRAGAssistant()
        print("  ✅ AoCRAGAssistant initialisé")

        # Charger les solutions
        count = assistant.load_solutions()
        print(f"  ✅ {count} fichiers chargés")

        if count > 0:
            stats = assistant.stats()
            print(f"  ✅ Stats : {stats['total_documents']} docs, jours {stats['days']}")

        return True

    except ValueError as e:
        print(f"  ⚠️  {e}")
        return False
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False


def test_full_query():
    """Test d'une requête complète (nécessite API key)"""
    print("\n🧪 Test 5: Test d'une requête complète...")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("  ⏭️  Sauté (pas de clé API)")
        return None

    try:
        from rag_example import SimpleRAG

        rag = SimpleRAG()
        rag.add_documents([
            "Day 1: Problème de tri de listes",
            "Day 2: Analyse de séquences"
        ])

        result = rag.query("Quel jour parlait de tri ?")
        print("  ✅ Requête réussie")
        print(f"  📝 Réponse (extrait): {result[:100]}...")

        return True

    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False


def main():
    """Exécute tous les tests"""
    print("=" * 60)
    print("🎄 Tests du système RAG pour Advent of Code 🎄")
    print("=" * 60)

    results = {
        "imports": test_imports(),
        "api_key": test_api_key(),
        "simple_rag": test_simple_rag(),
        "aoc_assistant": test_aoc_assistant(),
        "full_query": test_full_query()
    }

    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)

    for test_name, result in results.items():
        status = "✅" if result else ("❌" if result is False else "⏭️ ")
        print(f"{status} {test_name}")

    print(f"\nTotal: {passed} réussis, {failed} échoués, {skipped} sautés")

    if failed == 0:
        print("\n🎉 Tout fonctionne ! Vous pouvez utiliser le RAG.")
        print("\nPour commencer :")
        print("  python rag_aoc_assistant.py")
    else:
        print("\n⚠️  Certains tests ont échoué. Consultez les erreurs ci-dessus.")

        if not results["api_key"]:
            print("\n💡 N'oubliez pas de définir votre clé API !")
            print("   export ANTHROPIC_API_KEY='votre-clé'")


if __name__ == "__main__":
    main()
