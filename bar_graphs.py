import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow.keras.models import load_model

# Load your trained model
model_path = 'static/final_cnn_model.h5'
model = load_model(model_path)

# Define your class labels
all_labels = [
    'Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion',
    'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass', 'No Finding',
    'Nodule', 'Pleural Thickening', 'Pneumonia', 'Pneumothorax'
]

# Load and preprocess the image
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    return img

def generate(img_path):
    img = preprocess_image(img_path)
    img_array = np.expand_dims(img, axis=0)  # Add batch dimension

    # Generate predictions for the sample image
    predictions = model.predict(img_array)[0] * 100  # Convert predictions to percentages

    # Mock higher global average percentages for each condition (replace these with actual data)
    global_averages = np.array([
        10, 8, 6, 7, 15, 6, 4, 3, 18, 5, 50, 8, 7, 5, 4
    ])

    # Create a DataFrame for the predictions and global averages
    data = pd.DataFrame({
        'Condition': all_labels,
        'Predicted Probability': predictions,
        'Global Average': global_averages
    })

    # Plotting side-by-side bar graph with a light purple background
    fig, ax = plt.subplots(figsize=(15, 10))
    fig.patch.set_facecolor('#F2E1F7')  # Set the background color of the figure to light purple
    ax.set_facecolor('#F2E1F7')  # Set the background color of the axes to light purple

    # Set position of bar on X axis
    bar_width = 0.35
    r1 = np.arange(len(data['Condition']))
    r2 = [x + bar_width for x in r1]

    # Make the plot
    ax.bar(r1, data['Predicted Probability'], color='#89CFF0', width=bar_width, edgecolor='grey', label='Predicted')  # Soft blue
    ax.bar(r2, data['Global Average'], color='#F4C2C2', width=bar_width, edgecolor='grey', label='Global Average')  # Soft pink

    # Add labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Condition', fontweight='bold', fontsize=15)
    ax.set_ylabel('Percentage', fontweight='bold', fontsize=15)
    ax.set_title('Predicted Probabilities vs Global Averages', fontweight='bold', fontsize=16)
    ax.set_xticks([r + bar_width for r in range(len(r1))])
    ax.set_xticklabels(data['Condition'], rotation=45, ha='right')
    ax.legend()

    # Create labels on top of the bars
    def add_value_labels(ax, spacing=5):
        for rect in ax.patches:
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2
            space = spacing
            va = 'bottom'
            if y_value < 0:
                space *= -1
                va = 'top'
            label = "{:.1f}%".format(y_value)
            ax.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center', va=va, color='darkslateblue')

    # Call functions to implement the function calls
    add_value_labels(ax)

    plt.tight_layout()
    plt.savefig('static/outputs/bar_graph.png')