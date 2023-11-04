import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

model_path = 'final_cnn_model.h5'
model = load_model(model_path)
# Generate predictions for a sample image (you can replace this with your own image)
sample_image_path = 'static/uploads/input.jpg'
sample_image = cv2.imread(sample_image_path)
sample_image = cv2.resize(sample_image, (224, 224))
sample_image = sample_image / 255.0  # Normalize pixel values to [0, 1]
sample_image = np.expand_dims(sample_image, axis=0)  # Add batch dimension
predictions = model.predict(sample_image)

all_labels = ["Atelectasis", "Cardiomegaly", "Consolidation", "Edema", "Effusion", "Emphysema",
              "Fibrosis", "Infiltration", "Mass", "Nodule", "Pleural Thickening", "Pneumonia",
              "Pneumothorax"]

with open("static/output.json", "w") as f:

op = {}
for label, probability in zip(all_labels, predictions[0]):
    op[f'{label}'] = probability*100
    
# Display the class labels and their probabilities for the sample image
