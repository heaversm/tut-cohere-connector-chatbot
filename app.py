
import cohere
from cohere import ChatConnector
import uuid
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

cohere_client_api_key = os.getenv('COHERE_CLIENT_API_KEY')
cohere_connector_id = os.getenv('COHERE_CONNECTOR_ID')

co = cohere.Client(cohere_client_api_key)

class Chatbot:
    def __init__(self, connectors: List[str]):
        """
        Initializes an instance of the Chatbot class.

        """
        self.conversation_id = str(uuid.uuid4())
        self.connectors = [ChatConnector(id=connector) for connector in connectors]

    def run(self):
        """
        Runs the chatbot application.

        """
        while True:
            # Get the user message
            message = input("User: ")

            # Typing "quit" ends the conversation
            if message.lower() == "quit":
                print("Ending chat.")
                break
            else:                       # If using Google Colab, remove this line to avoid printing the same thing twice
              print(f"User: {message}") # If using Google Colab, remove this line to avoid printing the same thing twice

            # Generate response
            response = co.chat_stream(
                    message=message,
                    model="command-r-plus",
                    conversation_id=self.conversation_id,
                    connectors=self.connectors,
            )

            # Print the chatbot response, citations, and documents
            print("\nChatbot:")
            citations = []
            cited_documents = []

            # Display response
            for event in response:
                if event.event_type == "text-generation":
                    print(event.text, end="")
                elif event.event_type == "citation-generation":
                    citations.extend(event.citations)
                elif event.event_type == "stream-end":
                    cited_documents = event.response.documents

            # Display citations and source documents
            if citations:
              print("\n\nCITATIONS:")
              for citation in citations:
                print(citation)

              print("\nDOCUMENTS:")
              for document in cited_documents:
                print({'id': document['id'],
                        'text': document['text'][:50] + '...'})

            print(f"\n{'-'*100}\n")

# Define the connector
connectors = [cohere_connector_id]

# Initialize the chatbot
chatbot = Chatbot(connectors)

# Run the chatbot
chatbot.run()