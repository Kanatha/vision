import requests
import json
import os

def interact_with_chatbot(user_input, output_file):
    """
    Interact with a chatbot API by sending user input and receiving responses.
    
    Args:
        user_input (str): The text submitted by the user.
        output_file (str): The path to the output JSON file.
    
    Returns:
        tuple: A tuple containing the original data and the latest chatbot response.
    """
    # Define the chatbot API endpoint URL
    chatbot_api_url = "http://localhost:11434/api/chat"

    # Headers for the POST request
    headers = {
        "Content-Type": "application/json"
    }

    # Initialize original data
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            original_data = json.load(f)
    else:
        original_data = {
            "model": "llama3",
            "messages": [{
                "role": "user",
                "content": "Hello, chatbot!"
            }],
            "stream": False,
            "keep_alive": -1
        }

    # Construct the message payload
    payload = {
        "model": "llama3",
        "messages": original_data["messages"] + [{"role": "user", "content": user_input}],
        "stream": False,
        "keep_alive": -1
    }

    # Make the POST request to the chatbot API
    response = requests.post(chatbot_api_url, data=json.dumps(payload), headers=headers)

    # Handle the response
    if response.status_code == 200:
        try:
            returned_json = response.json()
            message = returned_json.get("message", {})
            content = message.get("content", "")
            # Append user input and chatbot response to original_data
            original_data["messages"].append({"role": "user", "content": user_input})
            original_data["messages"].append({"role": "assistant", "content": content})

            # Write the updated JSON data to the output file
            with open(output_file, "w") as f:
                json.dump(original_data, f, indent=4)
        except json.JSONDecodeError as e:
            print("Error decoding JSON response:", str(e))
    else:
        print("Error:", response.status_code, response.text)
    
    return original_data, content
