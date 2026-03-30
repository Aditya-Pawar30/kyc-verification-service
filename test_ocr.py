"""Test script to verify OCR is working correctly"""
import io
from PIL import Image
import pytesseract

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def create_test_image():
    """Create a test image with text similar to a PAN card"""
    from PIL import Image, ImageDraw, ImageFont
    
    # Create image
    img = Image.new('RGB', (800, 500), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use default font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Add text similar to PAN card
    text_color = (0, 0, 0)
    draw.text((50, 50), "INCOME TAX DEPARTMENT", fill=text_color, font=font)
    draw.text((50, 120), "Permanent Account Number", fill=text_color, font=font)
    draw.text((50, 180), "Name: JOHN DOE", fill=text_color, font=font)
    draw.text((50, 250), "Father's Name: ROBERT DOE", fill=text_color, font=font)
    draw.text((50, 320), "Date of Birth: 15/08/1990", fill=text_color, font=font)
    draw.text((50, 390), "ABCDE1234F", fill=text_color, font=font)
    
    return img

def test_tesseract():
    """Test Tesseract OCR on a test image"""
    print("Creating test image...")
    img = create_test_image()
    
    # Save test image
    img.save("test_pan.png")
    print("Test image saved as test_pan.png")
    
    # Extract text
    print("\nExtracting text with Tesseract...")
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, lang='eng', config=custom_config)
    
    print(f"\nExtracted text:\n{text}")
    
    # Check for expected values
    print("\n--- Validation ---")
    print(f"Contains 'JOHN DOE': {'JOHN DOE' in text.upper()}")
    print(f"Contains 'ABCDE1234F': {'ABCDE1234F' in text.upper()}")
    print(f"Contains DOB: {'15/08/1990' in text}")

if __name__ == "__main__":
    test_tesseract()