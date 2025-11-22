#!/usr/bin/env python3
"""
Image Analyzer - A comprehensive tool for analyzing PIL images and extracting text
Similar to the system that interpreted notification settings images
"""

import cv2
import pytesseract
from PIL import Image
import numpy as np
# import easyocr
import re
from typing import List, Dict, Tuple, Union
import argparse
import os

class ImageAnalyzer:
    def __init__(self):
        """Initialize the image analyzer with OCR engines"""
        # self.reader = easyocr.Reader(['en'])
        
        # Configure pytesseract path (adjust for your system)
        # On Windows, you might need to set the path to tesseract.exe
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
    def extract_text_ocr(self, image: Image.Image) -> str:
        """
        Extract text using Tesseract OCR
        Good for clean, high-contrast text
        """
        try:
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"Tesseract OCR error: {e}")
            return ""
    
    def extract_text_easyocr(self, image: Image.Image) -> List[Tuple]:
        """
        Extract text using EasyOCR
        Better for complex layouts and various text styles
        """
        # try:
        #     # Convert PIL image to numpy array for EasyOCR
        #     image_array = np.array(image)
        #     results = self.reader.readtext(image_array)
        #     return results
        # except Exception as e:
        #     print(f"EasyOCR error: {e}")
        #     return []
        
        return []
        
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess PIL image for better OCR results
        """
        try:
            # Convert PIL image to numpy array
            image_array = np.array(image)
            
            # Convert to grayscale if it's RGB
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_array
            
            # Apply thresholding to get binary image
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Noise removal
            kernel = np.ones((1, 1), np.uint8)
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            return binary
        except Exception as e:
            print(f"Preprocessing error: {e}")
            return np.array(image)
    
    def extract_text_advanced(self, image: Image.Image) -> str:
        """
        Advanced text extraction with preprocessing
        """
        try:
            # Preprocess image
            processed = self.preprocess_image(image)
            
            # Convert numpy array back to PIL Image for Tesseract
            processed_pil = Image.fromarray(processed)
            
            # Extract text from processed image
            text = pytesseract.image_to_string(processed_pil)
            return text.strip()
        except Exception as e:
            print(f"Advanced OCR error: {e}")
            return ""
    
    def analyze_ui_elements(self, image: Image.Image) -> Dict:
        """
        Analyze UI elements in the PIL image
        Useful for identifying forms, buttons, dropdowns, etc.
        """
        try:
            # Convert PIL image to numpy array
            image_array = np.array(image)
            
            # Convert to grayscale if it's RGB
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_array
            
            # Detect edges
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analyze contours for UI elements
            ui_elements = {
                'rectangles': 0,
                'buttons': 0,
                'input_fields': 0,
                'total_elements': len(contours)
            }
            
            for contour in contours:
                # Approximate contour to polygon
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Count rectangles (likely UI elements)
                if len(approx) == 4:
                    ui_elements['rectangles'] += 1
                    
                    # Estimate size to determine if it's a button or input field
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    if 2 < aspect_ratio < 8:  # Wide rectangles are likely input fields
                        ui_elements['input_fields'] += 1
                    elif 0.5 < aspect_ratio < 2:  # Square-ish rectangles are likely buttons
                        ui_elements['buttons'] += 1
            
            return ui_elements
            
        except Exception as e:
            print(f"UI analysis error: {e}")
            return {}
    
    def generate_description(self, image: Image.Image) -> str:
        """
        Generate a comprehensive description of the PIL image
        Similar to what the system provided for your notification images
        """
        description_parts = []
        
        # Extract text using multiple methods
        tesseract_text = self.extract_text_ocr(image)
        easyocr_results = self.extract_text_easyocr(image)
        advanced_text = self.extract_text_advanced(image)
        
        # Analyze UI elements
        ui_analysis = self.analyze_ui_elements(image)
        
        # Combine text results (prioritize the best one)
        best_text = advanced_text if advanced_text else tesseract_text
        
        if best_text:
            # Clean and format the text
            lines = [line.strip() for line in best_text.split('\n') if line.strip()]
            
            if lines:
                description_parts.append(f"The image displays a list of {len(lines)} text options:")
                for i, line in enumerate(lines, 1):
                    description_parts.append(f"{i}. {line}")
        
        # Add UI analysis
        if ui_analysis:
            description_parts.append(f"\nUI Elements detected:")
            description_parts.append(f"- Total elements: {ui_analysis['total_elements']}")
            description_parts.append(f"- Rectangles: {ui_analysis['rectangles']}")
            description_parts.append(f"- Buttons: {ui_analysis['buttons']}")
            description_parts.append(f"- Input fields: {ui_analysis['input_fields']}")
        
        return '\n'.join(description_parts)
    
    def save_processed_image(self, image: Image.Image, output_path: str):
        """
        Save the preprocessed PIL image for debugging
        """
        try:
            processed = self.preprocess_image(image)
            processed_pil = Image.fromarray(processed)
            processed_pil.save(output_path)
            print(f"Processed image saved to: {output_path}")
        except Exception as e:
            print(f"Error saving processed image: {e}")
    
    def analyze_from_file(self, image_path: str) -> Image.Image:
        """
        Load image from file and return PIL Image object
        Helper method for command line usage
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        return Image.open(image_path)

# def main():
#     parser = argparse.ArgumentParser(description='Analyze PIL images and extract text')
#     parser.add_argument('image_path', help='Path to the image file')
#     parser.add_argument('--output', '-o', help='Output path for processed image')
#     parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
#     args = parser.parse_args()
    
#     analyzer = ImageAnalyzer()
    
#     try:
#         # Load image from file
#         image = analyzer.analyze_from_file(args.image_path)
        
#         print("=== Image Analysis Results ===\n")
        
#         # Generate comprehensive description
#         description = analyzer.generate_description(image)
#         print(description)
        
#         # Save processed image if requested
#         if args.output:
#             analyzer.save_processed_image(image, args.output)
        
#         if args.verbose:
#             print("\n=== Detailed Analysis ===")
            
#             # OCR results
#             print("\nTesseract OCR:")
#             print(analyzer.extract_text_ocr(image))
            
#             print("\nEasyOCR Results:")
#             easyocr_results = analyzer.extract_text_easyocr(image)
#             for (bbox, text, prob) in easyocr_results:
#                 print(f"Text: {text}, Confidence: {prob:.2f}")
            
#             print("\nAdvanced OCR (with preprocessing):")
#             print(analyzer.extract_text_advanced(image))
            
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     main() 