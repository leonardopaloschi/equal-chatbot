
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Input

import re

import numpy as np

from data import get_data

def train_model():
    texts = get_data()

    for i in texts:
        texts[texts.index(i)] = re.sub(r"\s{2,}", " ", i).lstrip().rstrip()  

    print(texts)
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts)
    vocab_size = len(tokenizer.word_index) + 1

    sequences = tokenizer.texts_to_sequences(texts)
    max_sequence_length = max(len(seq) for seq in sequences)
    padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)

    embedding_dim = 128  # Adjust the dimensionality according to your requirements

    model = Sequential()
    model.add(Input(shape=(max_sequence_length,), dtype='int32'))
    model.add(Embedding(vocab_size, embedding_dim))
    model.add(LSTM(128))
    model.add(Dense(vocab_size, activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="adam")

    # Treinamento do modelo
    X = padded_sequences[:]
    y = tf.keras.utils.to_categorical(padded_sequences[:, -1], num_classes=vocab_size)

    model.fit(X, y, epochs=50, verbose=2)

    return model, tokenizer, max_sequence_length

# Função para gerar uma frase com base em um termo
def generate_sentence(query, model, tokenizer, max_sequence_length, num_words=10, temperature=0.9):
    query_sequence = tokenizer.texts_to_sequences([query])
    query_sequence = pad_sequences(query_sequence, maxlen=max_sequence_length)
    
    generated_words = []
    for _ in range(num_words):
        predicted_probs = model.predict(query_sequence)[0]
        predicted_probs = np.log(predicted_probs) / temperature
        predicted_probs = np.exp(predicted_probs) / np.sum(np.exp(predicted_probs))

        predicted_index = np.random.choice(len(predicted_probs), size=1, p=predicted_probs)[0]
        try:
            output_word = tokenizer.index_word[predicted_index]
        except:
            output_word = ''
        
        generated_words.append(output_word)

        query_sequence = np.append(query_sequence, [[predicted_index]], axis=1)
        query_sequence = query_sequence[:, 1:]
    
    generated_sentence = ' '.join(generated_words)
    return generated_sentence