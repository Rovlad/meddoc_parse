"""Image processing utilities"""

import base64
from io import BytesIO
from PIL import Image
from typing import Tuple
import logging

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


def validate_image(file_content: bytes, max_size_bytes: int, allowed_extensions: list) -> Tuple[bool, str]:
    """
    Validate image file
    
    Args:
        file_content: Binary content of the file
        max_size_bytes: Maximum allowed file size in bytes
        allowed_extensions: List of allowed file extensions
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check file size
        if len(file_content) > max_size_bytes:
            max_mb = max_size_bytes / (1024 * 1024)
            return False, f"File size exceeds maximum allowed size of {max_mb}MB"
        
        # Try to open as image
        try:
            image = Image.open(BytesIO(file_content))
            image.verify()
            return True, ""
        except Exception as e:
            # If it's not a valid image
            return False, f"Invalid image file: {str(e)}"
            
    except Exception as e:
        logger.error(f"Error validating image: {str(e)}")
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
        # Open image
        image = Image.open(BytesIO(file_content))
        
        # Convert to RGB if necessary (for PNG with transparency, etc.)
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Optimize image size if it's too large
        max_dimension = 2048
        if max(image.size) > max_dimension:
            ratio = max_dimension / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            logger.info(f"Resized image from {image.size} to {new_size}")
        
        # Save to buffer
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        
        # Encode to base64
        encoded_string = base64.b64encode(buffer.read()).decode('utf-8')
        return encoded_string
        
    except Exception as e:
        logger.error(f"Error encoding image to base64: {str(e)}")
        raise ValueError(f"Failed to encode image: {str(e)}")

