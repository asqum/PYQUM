import os
import numpy as np
import cv2

def readfile(path, label):
    # label is the boolean variable representing whether needs to return y's values
    image_dir1 = sorted(os.listdir(path))
    length = 0
    for i, file in enumerate(image_dir1):
      image_dir2 = sorted(os.listdir(os.path.join(path, "{}".format(i))))
      length += len(image_dir2)
    x = np.zeros((length, 28, 28, 3), dtype=np.uint8)
    y = np.zeros(length, dtype=np.uint8)
    index = 0
    for i, file in enumerate(image_dir1):
      image_dir2 = sorted(os.listdir(os.path.join(path, "{}".format(i))))
      for _, file in enumerate(image_dir2):
        img = cv2.imread(os.path.join(path, "{}".format(i), file))
        x[index, :, :] = cv2.resize(img,(28, 28))
        if label:
          y[index] = i
        index += 1
    if label:
      return x, y
    else:
      return x

# This function spilts data into training set and validation set
def _train_dev_split(X, Y, dev_ratio = 0.25):
    train_size = int(len(X) * (1 - dev_ratio))
    return X[:train_size], Y[:train_size], X[train_size:], Y[train_size:]

def _shuffle(X, Y):
    # This function shuffles two equal-length list/array, X and Y, together.
    randomize = np.arange(len(X))
    np.random.shuffle(randomize)
    return (X[randomize], Y[randomize])