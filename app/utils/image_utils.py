"""Image processing utilities"""

import base64
from io import BytesIO
from PIL import Image
from typing import Tuple, Optional
import logging
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


def get_file_extension(filename: str) -> str:
    """
    Extract file extension from filename
    
    Args:
        filename: Name of the file
        
    Returns:
        File extension in lowercase without dot
    """
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''


def pdf_to_image(pdf_content: bytes, dpi: int = 150) -> Image.Image:
    """
    Convert PDF to PIL Image (first page only)
    
    Args:
        pdf_content: Binary content of the PDF file
        dpi: Resolution for rendering (default 150)
        
    Returns:
        PIL Image object of the first page
    """
    try:
        # Open PDF from bytes
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        
        if pdf_document.page_count == 0:
            raise ValueError("PDF has no pages")
        
        # Get first page
        page = pdf_document[0]
        
        # Render page to pixmap
        # zoom factor: 1.0 = 72 DPI, so dpi/72 gives us the desired DPI
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert pixmap to PIL Image
        img_data = pix.tobytes("png")
        image = Image.open(BytesIO(img_data))
        
        # Close PDF
        pdf_document.close()
        
        logger.info(f"Converted PDF to image: size={image.size}, mode={image.mode}")
        return image
        
    except Exception as e:
        logger.error(f"Error converting PDF to image: {str(e)}")
        raise ValueError(f"Failed to convert PDF to image: {str(e)}")


def validate_image(file_content: bytes, max_size_bytes: int, allowed_extensions: list) -> Tuple[bool, str]:
    """
    Validate image or PDF file
    
    Args:
        file_content: Binary content of the file
        max_size_bytes: Maximum allowed file size in bytes
        allowed_extensions: List of allowed file extensions
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check if file is empty
        if not file_content or len(file_content) == 0:
            return False, "File is empty or contains no data"
        
        # Check file size
        if len(file_content) > max_size_bytes:
            max_mb = max_size_bytes / (1024 * 1024)
            return False, f"File size exceeds maximum allowed size of {max_mb}MB"
        
        # Log file info for debugging
        logger.info(f"Validating file: size={len(file_content)} bytes, first 10 bytes={file_content[:10].hex()}")
        
        # Check if it's a PDF file (PDF files start with %PDF)
        is_pdf = file_content[:4] == b'%PDF'
        
        if is_pdf:
            logger.info("Detected PDF file")
            try:
                # Try to convert PDF to image to validate it
                image = pdf_to_image(file_content)
                logger.info(f"PDF validated successfully: size={image.size}")
                return True, ""
            except Exception as e:
                logger.error(f"Failed to validate PDF: {str(e)}")
                return False, f"Invalid PDF file: {str(e)}. Please ensure you're uploading a valid PDF file."
        else:
            # Try to open as regular image
            try:
                image_stream = BytesIO(file_content)
                image = Image.open(image_stream)
                # Get image format and size before verify
                img_format = image.format
                img_size = image.size
                logger.info(f"Image opened successfully: format={img_format}, size={img_size}")
                
                # Verify image integrity
                # Note: verify() consumes the image, so we do this last
                image_stream.seek(0)  # Reset stream position
                image = Image.open(image_stream)  # Re-open for verify
                image.verify()
                
                return True, ""
            except Exception as e:
                # If it's not a valid image
                logger.error(f"Failed to open image: {str(e)}, file size: {len(file_content)} bytes")
                return False, f"Invalid image file: {str(e)}. Please ensure you're uploading a valid image file (JPG, PNG, or PDF)."
            
    except Exception as e:
        logger.error(f"Error validating file: {str(e)}")
        return False, f"Error validating file: {str(e)}"


def encode_image_to_base64(file_content: bytes, filename: str = "") -> str:
    """
    Encode image to base64 string
    
    Args:
        file_content: Binary content of the image
        filename: Optional filename to determine format
        
    Returns:
        Base64 encoded string
    """
    try:
        # Check if file content is empty
        if not file_content or len(file_content) == 0:
            raise ValueError("File content is empty")
        
        # Check if it's a PDF file
        is_pdf = file_content[:4] == b'%PDF'
        
        if is_pdf:
            # Convert PDF to image first
            logger.info("Detected PDF file, converting to image")
            image = pdf_to_image(file_content)
        else:
            # Open image
            logger.info(f"Encoding image to base64: size={len(file_content)} bytes")
            image_stream = BytesIO(file_content)
            image = Image.open(image_stream)
        
        # Get original format and size
        original_format = image.format
        original_size = image.size
        logger.info(f"Opened image: format={original_format}, size={original_size}, mode={image.mode}")
        
        # Convert to RGB if necessary (for PNG with transparency, etc.)
        if image.mode in ('RGBA', 'LA', 'P'):
            logger.info(f"Converting image from {image.mode} to RGB")
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        elif image.mode != 'RGB':
            logger.info(f"Converting image from {image.mode} to RGB")
            image = image.convert('RGB')
        
        # Optimize image size if it's too large
        max_dimension = 2048
        if max(image.size) > max_dimension:
            ratio = max_dimension / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            logger.info(f"Resized image from {original_size} to {new_size}")
        
        # Save to buffer
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        
        # Encode to base64
        encoded_bytes = buffer.read()
        logger.info(f"JPEG buffer size: {len(encoded_bytes)} bytes")
        encoded_string = base64.b64encode(encoded_bytes).decode('utf-8')
        logger.info(f"Base64 encoded string length: {len(encoded_string)}")
        
        return encoded_string
        
    except Exception as e:
        logger.error(f"Error encoding image to base64: {str(e)}", exc_info=True)
        raise ValueError(f"Failed to encode image: {str(e)}")

