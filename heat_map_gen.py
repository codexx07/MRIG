import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input

def preprocess_image(image_path, target_size=(224, 224)):
    img = image.load_img(image_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array
# Assuming that '/content/drive/MyDrive/final_cnn_model.h5' is the path to your trained model
model_path = 'static/final_cnn_model.h5'
model = load_model(model_path)

# Define the path to your image
def generate(image_path):

    # Define a function to load and preprocess the image

    # Load and preprocess the image
    img_array = preprocess_image(image_path)

    # Make a prediction
    predictions = model.predict(img_array)

    # Get the weights of the output layer
    output_weights = model.layers[-1].get_weights()[0]

    # Assuming 'model' is your pre-trained model
    # Extract the vgg16 part from your model
    vgg16_model = model.get_layer('vgg16')

    # The actual last conv layer name in the standard VGG16 model is 'block5_conv3'
    # We will use this to get the last conv layer from the vgg16 part
    last_conv_layer = vgg16_model.get_layer('block5_conv3')

    # Now, let's create a new model that outputs the last_conv_layer's activations
    last_conv_layer_model = tf.keras.Model(inputs=vgg16_model.input, outputs=last_conv_layer.output)

    # Now we create the CAM for the last conv layer's output
    last_conv_output = last_conv_layer_model.predict(img_array)
    last_conv_output = last_conv_output[0]  # Remove batch dimension

    # Assuming the dense layer after flattening is named 'dense_3' and it's the output layer
    # Get the weights for the class index from the final dense layer (output layer)
    weights = model.get_layer('dense_3').get_weights()[0]

    # Generate the CAM as before
    class_idx = np.argmax(predictions[0])  # Index of the predicted class
    cam = np.dot(last_conv_output, weights[:, class_idx])
    cam = cv2.resize(cam, (224, 224))
    cam = np.maximum(cam, 0)
    cam = cam / cam.max()

    # ... (rest of the CAM visualization code remains the same)


    # We use the 'block5_conv3' layer for VGG16
    last_conv_output = last_conv_layer_model.predict(img_array)
    last_conv_output = last_conv_output[0]

    # Create the class activation map
    cam = np.dot(last_conv_output, output_weights[:, class_idx])

    # Resize the CAM to 224x224
    cam = cv2.resize(cam, (224, 224))

    # ReLU activation to get the positive influence on the class prediction
    cam = np.maximum(cam, 0)

    # Normalize the CAM
    cam /= np.max(cam)

    # Convert to uint8 and apply colormap
    cam = np.uint8(255 * cam)
    heatmap = cv2.applyColorMap(cam, cv2.COLORMAP_JET)

    # Superimpose the heatmap onto the original image
    original_img = cv2.imread(image_path)
    original_img = cv2.resize(original_img, (224, 224))
    superimposed_img = heatmap * 0.5 + original_img * 0.5
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)

    # Display the original image and the CAM
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB))
    plt.title('Class Activation Map')
    plt.axis('off')
    plt.savefig('static/outputs/heatmap.png')