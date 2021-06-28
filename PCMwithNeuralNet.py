import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
from sklearn.decomposition import PCA
from keras.models import Sequential
from keras.layers import Dense, Dropout, Input
from keras.optimizers import SGD
from tensorflow.python.keras.backend import dropout

# Load data
files = glob("data/dataframes/622592_*")
dataframes = []
for f in files:
    df = pd.read_csv(f)
    dataframes.append(df)
df = pd.concat(dataframes)

# Adjust columns
df.rename(columns = {'Unnamed: 0':'time'}, inplace = True)
df['time'] = pd.DatetimeIndex(df['time'])
df.set_index('time', inplace=True)

# Discard columns without relevance
df.drop(['orientation', 'string_id'], axis=1, inplace=True)

# Shuffle the items of our dataframe
df_this = df.sample(frac=1)

# Extract the training data from sourec
Y_train = df_this['defect'].astype('float32').to_numpy()
X_train = df_this.drop(["defect"], axis=1).astype('float32').to_numpy()

# Calculate the PCA and take the first thre componets 
pca = PCA(3)
pca.fit(X_train)
# Print the explained variance of the first three elements
print(pca.explained_variance_ratio_)

# Transform the training data
X_train = pca.transform(X_train)

# Plot the 
fig = plt.figure()
ax = plt.axes(projection='3d')#
ax.scatter3D(X_train[:,0], X_train[:,1], X_train[:,2], c=Y_train)
plt.show()

# Build a neural network 
model = Sequential()
model.add(Input(shape=(3,)))
model.add(Dense(454, kernel_initializer='he_uniform', bias_initializer='zeros', name="layer1"))
model.add(Dropout(0.4))
model.add(Dense(2245, kernel_initializer='he_uniform', bias_initializer='zeros', name="layer2"))
model.add(Dropout(0.4))
model.add(Dense(224, kernel_initializer='he_uniform', bias_initializer='zeros', name="layer3"))
model.add(Dropout(0.4))
model.add(Dense(32, kernel_initializer='he_uniform', bias_initializer='zeros', name="layer4"))
model.add(Dense(1, activation="sigmoid", name="output"))

# Print a summary of the build neural network
model.summary()

# Use stochastic gradient descent optimizer
opt = SGD(learning_rate=0.0001)
model.compile(loss = 'binary_crossentropy', optimizer = opt, metrics="acc")
history = model.fit(x=X_train, y=Y_train, epochs=40, batch_size=100, validation_split=0.3)

# Plot the accurancy and loss plot
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Trainingsdaten', 'Validierungsdaten'], loc='upper left')
plt.show()

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Accurancy')
plt.ylabel('Accurancy')
plt.xlabel('Epoch')
plt.legend(['Trainingsdaten', 'Validierungsdaten'], loc='lower right')
plt.show()