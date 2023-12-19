import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import pandas as pd
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

# Import CSV File
df = pd.read_csv("../data_pp_engine/output.csv", encoding="utf-8", on_bad_lines="skip")
# Remove bad lines
df = df.dropna()
# Seperate phish and real data for down sampling
df_phish = df[df['is_phish'] == 1]
df_real = df[df['is_phish'] == 0]
# do downsampling
df_phish_downsampled = df_phish.sample(df_real.shape[0])
df_balanced = pd.concat([df_phish_downsampled, df_real])
# build training and test data set
X_train, X_test, y_train, y_test = train_test_split(
        df_balanced['text'],
        df_balanced['is_phish'],
        stratify=df_balanced['is_phish'])
# build model
bert_preprocess = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")
# bert layers
text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name="text")
preprocessed_text = bert_preprocess(text_input)
outputs = bert_encoder(preprocessed_text)
# NN layers
l = tf.keras.layers.Dropout(0.1, name="droput")(outputs['pooled_output'])
l = tf.keras.layers.Dense(1, activation='sigmoid', name="output")(l)
# use inputs and outputs to construct the final model
model = tf.keras.Model(inputs=[text_input], outputs = [l])
METRICS = [
        tf.keras.metrics.BinaryAccuracy(name="accuracy"),
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall")
]
model.compile(optimizer="adam",
              loss="binary_crossentropy",
              metrics=METRICS)
model.fit(X_train, y_train, epochs=10)

model.save("./my_model.keras")

y_predicted = model.predict(X_test)
y_predicted = y_predicted.flatten()
print(y_predicted)
