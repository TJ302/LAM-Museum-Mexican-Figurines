import tensorflow as tf
import pandas as pd
import numpy as np

# --- Load and preprocess data ---
train_df = pd.read_csv("mnist_train.csv")
X_train = train_df.drop("label", axis=1).values / 255.0
y_train = train_df["label"].values

test_df = pd.read_csv("mnist_test.csv")
X_test = test_df.drop("label", axis=1).values / 255.0
y_test = test_df["label"].values

X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

# --- Build model ---
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation="relu", input_shape=(28,28,1)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation="relu"),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax")
])

model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

# --- Train ---
model.fit(X_train, y_train, epochs=3, validation_data=(X_test, y_test))

# --- Save as Keras model (.h5) ---
model.save("my_model.h5")
print("✅ Model saved to my_model.h5")
