"""This module builds and trains an LSTM model for text generation."""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Input
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import numpy as np
from data import get_data

def preprocess_texts(texts):
    """Remove extra spaces from texts."""
    return [re.sub(r"\s{2,}", " ", text).strip() for text in texts]

def build_and_train_model(texts):
    """Build and train the LSTM model."""
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts)
    vocab_size = len(tokenizer.word_index) + 1

    sequences = tokenizer.texts_to_sequences(texts)
    max_sequence_length = max(len(seq) for seq in sequences)
    padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)

    embedding_dim = 128  # Adjust dimensionality as needed

    model = Sequential([
        Input(shape=(max_sequence_length,), dtype='int32'),
        Embedding(vocab_size, embedding_dim),
        LSTM(128),
        Dense(vocab_size, activation="softmax")
    ])
    model.compile(loss="categorical_crossentropy", optimizer="adam")

    X = padded_sequences[:, :-1]
    y = tf.keras.utils.to_categorical(padded_sequences[:, -1], num_classes=vocab_size)

    model.fit(X, y, epochs=50, verbose=2)

    return model, tokenizer, max_sequence_length

def generate_sentence(query, model, tokenizer, max_sequence_length, num_words=10, temperature=0.9):
    """Generate a sentence based on the query using the trained model."""
    query_sequence = tokenizer.texts_to_sequences([query])
    query_sequence = pad_sequences(query_sequence, maxlen=max_sequence_length)

    generated_words = []
    for _ in range(num_words):
        predicted_probs = model.predict(query_sequence)[0]
        predicted_probs = np.log(predicted_probs) / temperature
        predicted_probs = np.exp(predicted_probs) / np.sum(np.exp(predicted_probs))

        predicted_index = np.random.choice(len(predicted_probs), size=1, p=predicted_probs)[0]
        output_word = tokenizer.index_word.get(predicted_index, '')

        generated_words.append(output_word)

        query_sequence = np.append(query_sequence, [[predicted_index]], axis=1)
        query_sequence = query_sequence[:, 1:]

    return ' '.join(generated_words)

def main():
    texts = get_data()
    texts = preprocess_texts(texts)

    model, tokenizer, max_sequence_length = build_and_train_model(texts)

    query = "Your example query here"
    generated_sentence = generate_sentence(query, model, tokenizer, max_sequence_length)
    print(f"Generated Sentence: {generated_sentence}")

if __name__ == "__main__":
    main()
