from langchain_core.messages import  HumanMessage, AIMessage
from ChatBot import *

def main():
    """Boucle interactive de conversation avec le chatbot"""

    print("=" * 60)
    print("BIENVENUE DANS LE CHATBOT LANGGRAPH")
    print("=" * 60)
    print("Tapez 'exit', 'quit' ou 'merci' pour terminer\n")

    # Initialiser l'historique de conversation
    conversation_history = []

    while True:
        try:
            # Recevoir l'entrée utilisateur
            user_message = input("Vous: ").strip()

            # Vérifier les commandes de sortie
            if user_message.lower() in ["exit", "quit", "merci"]:
                print("\nAu revoir! Merci d'avoir utilisé le chatbot.")
                break

            # Ignorer les messages vides
            if not user_message:
                continue

            # Ajouter le message utilisateur à l'historique
            conversation_history.append(HumanMessage(content=user_message))

            # Invoquer le chatbot
            response = chatbot.invoke({"messages": conversation_history})

            # Extraire et afficher la réponse
            ai_response = response["messages"][-1].content

            # Ajouter la réponse IA à l'historique
            conversation_history.append(AIMessage(content=ai_response))

            # Afficher la réponse
            print(f"\nChatbot: {ai_response}\n")

        except KeyboardInterrupt:
            print("\n\nChatbot arrêté par l'utilisateur.")
            break
        except Exception as e:
            print(f"\nErreur: {str(e)}\n")


# ============================================================================
# POINT D'ENTRÉE
# ============================================================================
if __name__ == "__main__":
    main()