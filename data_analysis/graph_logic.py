from PIL import Image
import base64
import numpy as np

def save_image(matrix, image_path):
    # Normalize the matrix values to range between 0 and 255
    normalized_matrix = (matrix * 255).astype(np.uint8)
    
    # Create an image object from the normalized matrix
    img = Image.fromarray(normalized_matrix, mode='L')
    img = img.resize((300, 300), Image.NEAREST)
    
    # Save the image
    img.save(f'data_analysis/assets/{image_path}')
    return f'data_analysis/assets/{image_path}'




def encode_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


