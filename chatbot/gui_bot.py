import tkinter as tk
from tkinter import scrolledtext
from chatbot import chatbot_response
class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chatbot")
        self.chat_frame = tk.Frame(self.master)
        self.chat_frame.pack(pady=10)

        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, state='disabled', wrap='word', width=50, height=20)
        self.chat_area.pack(padx=10)

        self.user_input = tk.Entry(self.master, width=50)
        self.user_input.pack(padx=10, pady=10)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.lower() == 'quit':
            self.master.quit()
        else:
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, f"You: {user_message}\n")
            response = chatbot_response(user_message)  # Using the existing chatbot response function
            self.chat_area.insert(tk.END, f"ChatBot: {response}\n")
            self.chat_area.config(state='disabled')
            self.user_input.delete(0, tk.END)
            self.chat_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
