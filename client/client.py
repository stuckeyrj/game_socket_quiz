# Where we define the basic client and connect so we can play the game 
"""
- Connect to server
- Display questions & options
- Let user choose answer
- Send answer to server
- Receive score/feedback
"""
import socket
import json

HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    try:
        question_data = client.recv(1024).decode()
        if not question_data:
            break

        # Try to parse JSON for a question
        try:
            q = json.loads(question_data)
            print("\n" + q["question"])
            for i, opt in enumerate(q["options"], 1):
                print(f"{i}. {opt}")

            choice = input("Your answer: ")
            selected = q["options"][int(choice)-1]
            client.send(selected.encode())

            response = client.recv(1024).decode()
            print(response)
        except json.JSONDecodeError:
            print(question_data)
    except:
        break

client.close()
