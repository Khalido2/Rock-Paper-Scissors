import tensorflow as tf
import pandas as pd
import glob
import numpy

#Build CNN model
def build_model(input_shape):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Conv2D(6, 5, activation='relu', input_shape=input_shape))
    model.add(tf.keras.layers.MaxPool2D(pool_size=(2, 2),strides=(1, 1), padding='valid'))
    model.add(tf.keras.layers.Conv2D(6, 5, activation='relu'))
    model.add(tf.keras.layers.MaxPool2D(pool_size=(2, 2),strides=(1, 1), padding='valid'))
   # model.add(tf.keras.layers.Conv2D(100, 3, activation='relu'))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(84, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.4))
    model.add(tf.keras.layers.Dense(3, activation='softmax'))

    return model

#Extracts all grids in excel files in this directory and returns as a list
def get_dataset_from_csv(path, pattern):
    grids = []
    for filename in glob.glob(path + pattern):
        df = pd.read_csv(filename, header=None) #get dataframe from excel
        df = df.apply(pd.to_numeric, errors='coerce')
        grids.append(df.values.tolist())

    return grids

#Extracts the data for training/test/validation set and returns as a shuffled tensorflow dataset
def get_processed_set(root_directory, set, file_patten):
    paper_set = get_dataset_from_csv(root_directory + set + '/Paper/', file_patten)
    rock_set = get_dataset_from_csv(root_directory + set + '/Rock/', file_patten)
    scissors_set = get_dataset_from_csv(root_directory + set + '/Scissors/', file_patten)
    full_set = []
    full_set.extend(paper_set)
    full_set.extend(rock_set)
    full_set.extend(scissors_set)

    labels = [0] * len(paper_set) #create labels
    labels.extend([1] * len(rock_set))
    labels.extend([2] * len(scissors_set))

    data_set = tf.data.Dataset.from_tensor_slices(([full_set], [labels])) #convert to tf dataset
    data_set = data_set.shuffle(len(full_set))

    return data_set


GRID_SIZE = 100
BATCH_SIZE = 10
input_shape = (GRID_SIZE, GRID_SIZE, 1)
data_set_path = 'Datasets/'
dataset_file_type_pattern = '*.csv'

print('Building Datasets')
training_set = get_processed_set(data_set_path, 'train', dataset_file_type_pattern)
validation_set = get_processed_set(data_set_path, 'val', dataset_file_type_pattern)
test_set = get_processed_set(data_set_path, 'test', dataset_file_type_pattern)

print('Building Models')
model = build_model(input_shape)
callback = tf.keras.callbacks.EarlyStopping(monitor='accuracy', patience=5)
model.compile(optimizer='Adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

print('Training')
res = model.fit(training_set, validation_data=validation_set, batch_size=BATCH_SIZE, epochs = 15, shuffle=True, callbacks=[callback])
lastAccuracy = res.history['accuracy'][-1]
lastValAccuracy = res.history['val_accuracy'][-1]
print('Accuracy', lastAccuracy, 'Val Accuracy', lastValAccuracy)

model.save('rps_model') #save the model

print("Evaluate on test data")
results = model.evaluate(test_set, batch_size=BATCH_SIZE)
print("test loss, test acc:", results)