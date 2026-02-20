import streamlit as st
from graph import create_graph

st.set_page_config(
    page_title="Chatbot LangGraph + Groq",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Chatbot LangGraph + Groq")
st.caption("Modèle : openai/gpt-oss-120b via ChatGroq")

# Initialisation de l'état de session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "graph" not in st.session_state:
    st.session_state.graph = create_graph()

# Affichage de l'historique des messages
for message in st.session_state.messages:
    role = message["role"]
    with st.chat_message(role):
        st.markdown(message["content"])

# Zone de saisie utilisateur
if prompt := st.chat_input("Écrivez votre message..."):
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Invocation du graph LangGraph
    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            state = {
                "messages": st.session_state.messages[:]
            }
            result = st.session_state.graph.invoke(state)
            response = result["messages"][-1]["content"]
        st.markdown(response)

    # Sauvegarde de la réponse
    st.session_state.messages.append({"role": "assistant", "content": response})

# Bouton pour effacer la conversation
if st.session_state.messages:
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()