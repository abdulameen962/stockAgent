from smolagents import tool
from PIL import Image
from typing import List, Dict, Any
from .image_analyzer import ImageAnalyzer
import asyncio
import copy


async def get_image_result(image: Image.Image):
    """
    Asynchronously analyze a PIL image and extract text using multiple OCR methods.
    
    Args:
        image (Image.Image): PIL Image object to analyze
        
    Returns:
        Dict[str, str]: Dictionary containing text extraction results from different OCR methods
    """
    # Create a deep copy of the image to avoid thread safety issues
    image_copy = image.copy()
    
    analyzer = ImageAnalyzer()
    
    async def run_tesseract_ocr():
        """Run Tesseract OCR in a separate thread"""
        try:
            return await asyncio.to_thread(analyzer.extract_text_ocr, image_copy)
        except Exception as e:
            print(f"Tesseract OCR error: {e}")
            return ""
    
    # async def run_easyocr():
    #     """Run EasyOCR in a separate thread"""
    #     try:
    #         return await asyncio.to_thread(analyzer.extract_text_easyocr, image_copy)
    #     except Exception as e:
    #         print(f"EasyOCR error: {e}")
    #         return []
    
    async def run_advanced_ocr():
        """Run Advanced OCR in a separate thread"""
        try:
            return await asyncio.to_thread(analyzer.extract_text_advanced, image_copy)
        except Exception as e:
            print(f"Advanced OCR error: {e}")
            return ""
    
    # Run OCR operations concurrently with proper error handling
    tesseract_text, advanced_text = await asyncio.gather(
        run_tesseract_ocr(),
        # run_easyocr(),
        run_advanced_ocr(),
        return_exceptions=True
    )
    
    # Handle any exceptions that occurred during processing
    if isinstance(tesseract_text, Exception):
        print(f"Tesseract OCR failed: {tesseract_text}")
        tesseract_text = ""
    
    # if isinstance(easyocr_results, Exception):
    #     print(f"EasyOCR failed: {easyocr_results}")
    #     easyocr_results = []
    
    if isinstance(advanced_text, Exception):
        print(f"Advanced OCR failed: {advanced_text}")
        advanced_text = ""
    
    # Process EasyOCR results
    # easyocr_text = ""
    # if easyocr_results and isinstance(easyocr_results, list):
    #     for (bbox, text, prob) in easyocr_results:
    #         easyocr_text = f"{easyocr_text} \n {text}"

    print("Gotten info for ",image)
    
    result = {
        "text_ocr": tesseract_text,
        # "text_easyocr": easyocr_text,
        "text_advanced": advanced_text
    }

    return result


async def read_images_async(images: List[Image.Image]) -> List[Dict[str, Any]]:
    """
    Asynchronously analyze PIL images and returns the text content of each image in a list of 3 categories each
    
    Args:
        images (List[Image.Image]): List of PIL images from corporate disclosures
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing the text content of each image in 
        3 categories namely text_ocr, text_easyocr, text_advanced   
        For Example:
        [
            {
                "text_ocr": "This is a test",
                "text_advanced": "This is a test"
            }
        ]
    """

    if not images:
        return {"error": "No images provided for analysis"}
    
    # Process images with proper error handling and concurrency limits
    semaphore = asyncio.Semaphore(3)  # Limit concurrent processing to avoid memory issues
    
    async def process_image_with_semaphore(image):
        async with semaphore:
            try:
                return await get_image_result(image)
            except Exception as e:
                print(f"Error processing image: {e}")
                return {
                    "text_ocr": f"Error: {str(e)}",
                    "text_advanced": f"Error: {str(e)}"
                }
    
    # Create tasks for all images to process them concurrently
    tasks = [process_image_with_semaphore(image) for image in images]
    
    # Wait for all image analysis tasks to complete
    all_analysis = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out any exceptions and return valid results
    valid_results = []
    for result in all_analysis:
        if isinstance(result, Exception):
            print(f"Image processing failed: {result}")
            valid_results.append({
                "text_ocr": f"Error: {str(result)}",
                # "text_easyocr": f"Error: {str(result)}",
                "text_advanced": f"Error: {str(result)}"
            })
        else:
            valid_results.append(result)
    
    return valid_results


@tool
def read_images(images: List[Image.Image]) -> List[Dict[str, Any]]:
    """
    Analyze PIL images and returns the text content of each image in a list of 3 categories each
    
    Args:
        images (List[Image.Image]): List of PIL images from corporate disclosures
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing the text content of each image in 
        3 categories namely text_ocr, text_easyocr, text_advanced   
        For Example:
        [
            {
                "text_ocr": "This is a test",
                # "text_easyocr": "This is a test",
                "text_advanced": "This is a test"
            }
        ]
    """
    return asyncio.run(read_images_async(images))