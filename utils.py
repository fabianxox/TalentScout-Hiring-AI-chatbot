#helper functions 

# utils.py
def check_exit_words(text):
    return text.strip().lower() in ["exit", "bye", "quit", "thank you"]
