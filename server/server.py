# where will apply the code to the server 
"""
- Load questions
- Accept client connections
- Send questions
- Handle answer checking & scoring
"""
import socket
import threading
import json
import os

HOST = '127.0.0.1'
PORT = 5555

clients = []
questions = []

# Load questions



current_dir = os.path.dirname(os.path.abspath(__file__))
question_file_path = os.path.join(current_dir, "../data/question.json")

with open(question_file_path, 'r') as f:
    questions = json.load(f)

def broadcast(message):
    for client in clients:
        client.send(message.encode())

def handle_client(client, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    score = 0

    for q in questions:
        try:
            question_data = json.dumps(q)
            client.send(question_data.encode())
            answer = client.recv(1024).decode().strip()

            if answer.lower() == q["answer"].lower():
                score += 1
                client.send("Correct!\n".encode())
            else:
                client.send(f"Wrong! The correct answer was: {q['answer']}\n".encode())
        except:
            break

    client.send(f"Game over! Your score: {score}/{len(questions)}\n".encode())
    client.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    while True:
        client, addr = server.accept()
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

print("[STARTING] Server is starting...")
start()

