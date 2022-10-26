import random
import json
import numpy as np
import pickle

"""
# download the necessary nltk packages for our script

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
"""

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential
from keras.layers import Dense, Input, Dropout
from keras.optimizers import SGD


lemmatizer = WordNetLemmatizer()

intents = json.loads(open("./core/intent.json").read())

words = []
ignorLetters = ["?", "!", ";", ",", "."]
classes = []
documents = []

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        wordList = word_tokenize(pattern)
        words.extend(wordList)
        documents.append((wordList, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(word.lower())
         for word in words if word not in ignorLetters]

# remove duplicate data
words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words, open("./core/words.pkl", "wb"))
pickle.dump(classes, open("./core/classes.pkl", "wb"))

training = []
outputEmpty = [0] * len(classes)

for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(
        word.lower()) for word in wordPatterns]
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)

    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append([bag, outputRow])

print(training)
print(outputEmpty)

random.shuffle(training)
training = np.array(training)

trainingX = list(training[:, 0])
trainingY = list(training[:, 1])


# build neuron network
model = Sequential()
# model.add(Dense(128, input_shape=(len(trainingX[0]),), activation="relu"))
model.add(Dense(128, activation="relu"))
model.add(Input(shape=(len(trainingX[0]))))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dense(len(trainingY[0]), activation="softmax"))

sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy",
              optimizer=sgd, metrics=["accuracy"])

hits = model.fit(np.array(trainingX), np.array(
    trainingY), epochs=200, batch_size=5, verbose=1)
model.save("./core/ZeroBot.h5", hits)


print("Done")

score = model.evaluate(trainingX, trainingY, verbose=0)
print('Test Score : ', score[0])
print('Test Accuracy : ', score[1])
