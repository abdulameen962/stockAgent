#!/usr/bin/env python3
"""
Example usage of the ImageAnalyzer class with PIL images
"""

from PIL import Image
from image_analyzer import ImageAnalyzer
import numpy as np

def create_sample_image():
    """
    Create a sample image with text for testing
    """
    # Create a white image with black text
    width, height = 400, 300
    image = Image.new('RGB', (width, height), color='white')
    
    # Add some sample text (this would normally be done with PIL's ImageDraw)
    # For demonstration, we'll create a simple pattern
    pixels = image.load()
    
    # Create a simple text-like pattern
    for y in range(height):
        for x in range(width):
            # Create some "text" patterns
            if 50 < y < 80 and 50 < x < 350:  # First line
                pixels[x, y] = (0, 0, 0) if (x + y) % 20 < 10 else (255, 255, 255)
            elif 100 < y < 130 and 50 < x < 350:  # Second line
                pixels[x, y] = (0, 0, 0) if (x + y) % 25 < 12 else (255, 255, 255)
            elif 150 < y < 180 and 50 < x < 350:  # Third line
                pixels[x, y] = (0, 0, 0) if (x + y) % 30 < 15 else (255, 255, 255)
    
    return image

def analyze_pil_image():
    """
    Demonstrate analyzing a PIL image directly
    """
    print("=== PIL Image Analysis Example ===\n")
    
    # Create analyzer instance
    analyzer = ImageAnalyzer()
    
    # Create a sample image
    print("Creating sample image...")
    sample_image = create_sample_image()
    
    # Save the sample image
    sample_image.save("sample_image.png")
    print("Sample image saved as 'sample_image.png'")
    
    # Analyze the PIL image directly
    print("\nAnalyzing PIL image...")
    description = analyzer.generate_description(sample_image)
    print(description)
    
    # Extract text using different methods
    print("\n=== Text Extraction Results ===")
    
    print("\nTesseract OCR:")
    tesseract_text = analyzer.extract_text_ocr(sample_image)
    print(tesseract_text if tesseract_text else "No text detected")
    
    print("\nEasyOCR Results:")
    easyocr_results = analyzer.extract_text_easyocr(sample_image)
    if easyocr_results:
        for (bbox, text, prob) in easyocr_results:
            print(f"Text: {text}, Confidence: {prob:.2f}")
    else:
        print("No text detected")
    
    print("\nAdvanced OCR (with preprocessing):")
    advanced_text = analyzer.extract_text_advanced(sample_image)
    print(advanced_text if advanced_text else "No text detected")
    
    # Analyze UI elements
    print("\n=== UI Element Analysis ===")
    ui_analysis = analyzer.analyze_ui_elements(sample_image)
    print(f"Total elements: {ui_analysis.get('total_elements', 0)}")
    print(f"Rectangles: {ui_analysis.get('rectangles', 0)}")
    print(f"Buttons: {ui_analysis.get('buttons', 0)}")
    print(f"Input fields: {ui_analysis.get('input_fields', 0)}")
    
    # Save processed image
    print("\nSaving processed image...")
    analyzer.save_processed_image(sample_image, "processed_sample.png")
    
    return sample_image

def analyze_existing_image(image_path):
    """
    Analyze an existing image file
    """
    try:
        # Load image with PIL
        image = Image.open(image_path)
        print(f"\n=== Analyzing existing image: {image_path} ===")
        print(f"Image size: {image.size}")
        print(f"Image mode: {image.mode}")
        
        # Create analyzer and analyze
        analyzer = ImageAnalyzer()
        description = analyzer.generate_description(image)
        print("\nDescription:")
        print(description)
        
        return image
        
    except Exception as e:
        print(f"Error analyzing image {image_path}: {e}")
        return None

if __name__ == "__main__":
    # Example 1: Create and analyze a sample image
    sample_img = analyze_pil_image()
    
    # Example 2: Analyze an existing image (uncomment if you have an image file)
    # existing_img = analyze_existing_image("C:/Users/hp/Documents/ai/stockAgent/random-image.png")
    
    print("\n=== Example completed ===")
    print("Check the generated files:")
    print("- sample_image.png (original sample)")
    print("- processed_sample.png (preprocessed version)") 