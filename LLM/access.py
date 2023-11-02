import requests

# Define the base URL of the API
base_url = "http://localhost:8000"  # Change this URL if your API is hosted elsewhere

# Function to send a chat request to the API
def send_chat_request(query):
    endpoint = "/chat"
    data = {"query": query}
    response = requests.post(base_url + endpoint, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.text)
        return None

# Function to get the chat history from the API
def get_chat_history():
    endpoint = "/chat-history"
    response = requests.get(base_url + endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.text)
        return None

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input == "exit":
            break
 
        chat_response = send_chat_request(user_input)
        if chat_response:
            print("Bot:", chat_response["answer"])

    chat_history = get_chat_history()
    print("Chat History:")
    for entry in chat_history:
        print("User:", entry[0])
        print("Bot:", entry[1])