import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

# to run the code arguments are filename and optional place to save the file to


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # data dir is only a path
    # inside there are directories that are named after each catteory
    # inside each file would be img files

    # list to hold the required data to return
    images = list()
    labels = list()
    # iterate through all subfolders in the parent folder
    for root, dirs, files in os.walk(data_dir):
        for subfolder in dirs:
            subfolder_path = os.path.join(root, subfolder)
            # iterate through files in the subfolder
            for file in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file)
                # check if the file is correct
                if file.lower().endswith(".ppm"):
                    # restriction parameters
                    new_width = IMG_WIDTH
                    new_heigt = IMG_HEIGHT
                    # open the image
                    image = cv2.imread(file_path)
                    # resize the image
                    resized_image = cv2.resize(image, (new_width, new_heigt))
                    # add it to the main list images
                    images.append(resized_image)
                    # add the image location to the list labels
                    labels.append(subfolder)
    # return the two listss as a tuple
    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
