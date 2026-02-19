%%writefile language_translator.py
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import re
import random
from sklearn.model_selection import train_test_split

# --------------------------
# SIMPLE TOKENIZER
# --------------------------
def tokenize(text):
    return text.lower().split()

# --------------------------
# LOAD DATA
# --------------------------
def load_data(path):
    df = pd.read_csv(path)
    df.dropna(inplace=True)
    return df["lambadi"].tolist(), df["english"].tolist()

# --------------------------
# BUILD VOCAB
# --------------------------
def build_vocab(sentences):
    vocab = {"<PAD>":0, "<SOS>":1, "<EOS>":2, "<UNK>":3}
    idx = 4
    for s in sentences:
        for w in tokenize(s):
            if w not in vocab:
                vocab[w] = idx
                idx += 1
    return vocab

# --------------------------
# CONVERT SENTENCE → TENSOR
# --------------------------
def sentence_to_tensor(sentence, vocab, max_len=20):
    tokens = tokenize(sentence)
    ids = [vocab.get(w, vocab["<UNK>"]) for w in tokens]
    ids = [vocab["<SOS>"]] + ids + [vocab["<EOS>"]]
    ids = ids[:max_len]
    ids += [vocab["<PAD>"]] * (max_len - len(ids))
    return torch.tensor(ids)

# --------------------------
# SIMPLE SEQ2SEQ MODEL
# --------------------------
class SimpleTranslator(nn.Module):
    def __init__(self, vocab_in, vocab_out, emb=64, hidden=128):
        super().__init__()
        self.encoder = nn.Embedding(vocab_in, emb)
        self.decoder = nn.Embedding(vocab_out, emb)
        self.rnn = nn.GRU(emb, hidden, batch_first=True)
        self.fc = nn.Linear(hidden, vocab_out)

    def forward(self, src):
        emb = self.encoder(src)
        out, hidden = self.rnn(emb)
        decoded = self.fc(out)
        return decoded

# --------------------------
# TRAIN FUNCTION
# --------------------------
def train_model(data_path):
    lambadi, english = load_data(data_path)

    vocab_l = build_vocab(lambadi)
    vocab_e = build_vocab(english)

    X = [sentence_to_tensor(s, vocab_l) for s in lambadi]
    Y = [sentence_to_tensor(s, vocab_e) for s in english]

    X = torch.stack(X)
    Y = torch.stack(Y)

    model = SimpleTranslator(len(vocab_l), len(vocab_e))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(200):
        optimizer.zero_grad()
        out = model(X)
        loss = loss_fn(out.view(-1, out.size(-1)), Y.view(-1))
        loss.backward()
        optimizer.step()

        if epoch % 50 == 0:
            print("Epoch:", epoch, "Loss:", loss.item())

    torch.save(model.state_dict(), "translator_model.pth")
    np.save("vocab_l.npy", vocab_l)
    np.save("vocab_e.npy", vocab_e)

    print("Training completed.")
    print("Model & vocabulary saved.")

# --------------------------
# TRANSLATE FUNCTION
# --------------------------
def translate(sentence):
    vocab_l = np.load("vocab_l.npy", allow_pickle=True).item()
    vocab_e = np.load("vocab_e.npy", allow_pickle=True).item()

    id2word = {i:w for w,i in vocab_e.items()}

    model = SimpleTranslator(len(vocab_l), len(vocab_e))
    model.load_state_dict(torch.load("translator_model.pth"))
    model.eval()

    src = sentence_to_tensor(sentence, vocab_l).unsqueeze(0)

    with torch.no_grad():
        out = model(src)[0]

    ids = out.argmax(dim=1).tolist()
    words = [id2word.get(i, "") for i in ids]

    return " ".join(words).replace("<PAD>","").replace("<SOS>","").replace("<EOS>","").strip()

# --------------------------
# COMMAND LINE
# --------------------------
import sys
if __name__ == "__main__":
    if "--train" in sys.argv:
        path = sys.argv[sys.argv.index("--train")+1]
        train_model(path)

    if "--translate" in sys.argv:
        sentence = sys.argv[sys.argv.index("--translate")+1]
        print(translate(sentence))
