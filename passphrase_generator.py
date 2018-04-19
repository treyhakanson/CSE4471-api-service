import random

def get_passphrase(num_words):
    word_list = map(
        lambda line: line.strip(),
        open("./deepspeech/wordlist.txt", "r").readlines())
    return " ".join([random.choice(word_list) for _ in range(num_words)])
