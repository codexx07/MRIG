import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
from tensorflow.keras.models import load_model


# Assuming that '/content/drive/MyDrive/final_cnn_model.h5' is the path to your trained model
model_path = 'static/final_cnn_model.h5'
model = load_model(model_path)
# Define the function to draw a single speedometer gauge
def draw_speedometer(percentage, ax, label):
    # Define the range of the speedometer
    start_angle = 180
    end_angle = 0
    range_angles = [start_angle, 144, 108, 72, 36, end_angle]  # Divide the gauge into sections
    colors = ["#008000", "#9ACD32", "#FFFF00", "#FFA500", "#FF0000"]  # Define the colors

    # Draw the colored sections of the gauge
    for i, color in enumerate(colors):
        ang1, ang2 = range_angles[i], range_angles[i+1]
        ax.add_patch(Wedge(center=(0.5, 0.5), r=0.3, theta1=ang2, theta2=ang1, color=color))

    # Draw the needle
    value_angle = start_angle - (percentage / 100.0) * 180
    x = 0.5 + 0.3 * np.cos(np.radians(value_angle))
    y = 0.5 + 0.3 * np.sin(np.radians(value_angle))
    ax.plot([0.5, x], [0.5, y], color='black', lw=2)  # Needle

    # Set the title of the gauge as the label
    ax.set_title(label, y=1.1)

    # Remove the axes
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

def generate(sample_image_path):
    sample_image = cv2.imread(sample_image_path)
    sample_image = cv2.cvtColor(sample_image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    sample_image = cv2.resize(sample_image, (224, 224))  # Assuming your model expects 224x224 input
    sample_image = sample_image / 255.0  # Normalize pixel values to [0, 1]
    sample_image = np.expand_dims(sample_image, axis=0)  # Add batch dimension

    # Make predictions using the model
    # Replace 'model' with your actual model and 'all_labels' with the actual labels
    predictions = model.predict(sample_image)[0]

    # Visualize the predictions as speedometer gauges
    fig, axs = plt.subplots(3, 5, figsize=(15, 9))  # Adjust the layout as needed
    axs = axs.flatten()  # Flatten the 2D array of axes
    all_labels = ["Atelectasis", "Cardiomegaly", "Consolidation", "Edema", "Effusion", "Emphysema",
                "Fibrosis", "Infiltration", "Mass", "Nodule", "Pleural Thickening", "Pneumonia",
                "Pneumothorax"]
    # Draw a speedometer gauge for each prediction and label
    for ax, label, probability in zip(axs, all_labels, predictions):
        draw_speedometer(probability * 100, ax, label)

    plt.tight_layout()
    plt.savefig("static/outputs/speedometers.png")