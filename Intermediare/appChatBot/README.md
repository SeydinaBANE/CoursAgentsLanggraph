# 🤖 Chatbot LangGraph + Groq

Chatbot conversationnel avec LangGraph pour la logique et Streamlit pour l'interface.

## Stack
- **LangGraph** : orchestration du flux conversationnel
- **ChatGroq** : provider LLM (modèle `openai/gpt-oss-120b`)
- **Streamlit** : interface utilisateur

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Créez un fichier `.env` ou exportez votre clé API Groq :

```bash
export GROQ_API_KEY="votre_clé_api_groq"
```

Vous pouvez obtenir une clé gratuite sur [console.groq.com](https://console.groq.com).

## Lancement

```bash
streamlit run app.py
```

## Structure du projet

```
chatbot_app/
├── app.py          # Interface Streamlit
├── graph.py        # Graph LangGraph + logique LLM
├── requirements.txt
└── README.md
```

## Architecture LangGraph

```
[START] → [chatbot_node] → [END]
```

Le graph peut être étendu facilement avec des nœuds supplémentaires (mémoire, outils, RAG, etc.).
