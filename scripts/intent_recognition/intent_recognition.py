
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class IntentRecognition:
    def __init__(self):
        self.vocab_size = 5000 # params
        self.oov_tok = '<OOV>'
        self.max_length = 50 # params
        self.trunc_type = 'post'
        self.padding_type = 'post'
        self.lr = 1e-2
        self.model_location = "models/intent_classification"
        self.model = None
        self.train_data_path = "../data/train.csv"
        self.test_data_path = "../data/test.csv"

    def train(self):
        df_train = pd.read_csv(self.train_data_path)
        df_test = pd.read_csv(self.test_data_path)

        df_train = df_train.sample(frac = 1)
        train_data = df_train['text'].to_numpy()
        test_data = df_test['text'].to_numpy()

        self.tokenizer = Tokenizer(num_words = self.vocab_size, oov_token=self.oov_tok)
        self.tokenizer.fit_on_texts(train_data)

        train_sequences = self.tokenizer.texts_to_sequences(train_data)
        test_sequences = self.tokenizer.texts_to_sequences(test_data)

        x_train = pad_sequences(train_sequences, maxlen=self.max_length, padding=self.padding_type, truncating=self.trunc_type)
        x_test = pad_sequences(test_sequences, maxlen=self.max_length, padding=self.padding_type, truncating=self.trunc_type)

        train_labels = pd.Categorical(df_train['category']).codes
        test_labels = pd.Categorical(df_test['category']).codes

        y_train = train_labels.reshape((10003,1))
        y_test = test_labels.reshape((3080,1))

        # partial_x_train = x_train[:9000]
        # partial_y_train = y_train[:9000]

        # x_val = x_train[9000:]
        # y_val = y_train[9000:]

        embedding_dim = 64

        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(self.vocab_size, embedding_dim),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(embedding_dim)),
            tf.keras.layers.Dense(embedding_dim, activation='relu'),
            tf.keras.layers.Dense(77, activation='softmax')
        ])

        self.model.summary()

        opt = tf.optimizers.Adam(learning_rate=self.lr)
        self.model.compile(loss='sparse_categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

        callbacks = []

        early_stop = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            min_delta=0,
            patience=10,
            verbose=0,
            mode='auto',
            baseline=None,
            restore_best_weights=True,
            start_from_epoch=0
        )
        callbacks.append(early_stop)

        lr_callback = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.1,
            patience=3,
            verbose=0,
            mode='auto',
            min_delta=0.0001,
            cooldown=0,
            min_lr=0.0,
        )
        callbacks.append(lr_callback)

        num_epochs = 100

        history = self.model.fit(x_train, y_train, epochs=num_epochs, validation_data=(x_test, y_test), verbose=1, callbacks=callbacks)

        df_train['category_codes'] = pd.Categorical(df_train['category']).codes
        self.df_ref = df_train[["category", "category_codes"]]
        self.df_ref = self.df_ref.drop_duplicates()
        self.df_ref = self.df_ref.reset_index(drop=True)

        # self.model.save(self.model_location)
    
    def predict(self, input_str: str):

        # if self.model is None:
        #     self.model = tf.keras.models.load_model(self.model_location)

        input_text_arr = np.array([input_str])
        input_text_sequences = self.tokenizer.texts_to_sequences(input_text_arr)
        input_text_padded = pad_sequences(input_text_sequences, maxlen=self.max_length, padding=self.padding_type, truncating=self.trunc_type)

        predictions = self.model.predict(input_text_padded)
        predicted_classes = np.argmax(predictions,axis=1)

        predicted_categories = []

        for x in predicted_classes:
            target_code = x
            category = self.df_ref[self.df_ref["category_codes"] == target_code]["category"].values[0]
            predicted_categories.append(category)

        return predicted_categories[0]


# input_str = "I am still waiting for my card, when will it arrive?"
# ic = IntentRecognition()
# ic.train()
# print(ic.predict(input_str))