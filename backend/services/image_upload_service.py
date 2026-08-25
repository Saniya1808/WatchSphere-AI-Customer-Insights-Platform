"""
WatchSphere AI v3.0 - Image Upload Service
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from pathlib import Path
import uuid
from typing import Optional
from config.logging import logger

IMAGES_DIR = Path("assets/images")


class ImageUploadService:
    """
    Saves uploaded image file bytes to assets/images/ directory and returns asset paths.
    """

    @staticmethod
    def save_image(file_bytes: bytes, file_name: str, subfolder: str = "products") -> Optional[str]:
        """
        Saves uploaded file bytes into assets/images/<subfolder>/ and returns relative path URL.
        """
        try:
            target_dir = IMAGES_DIR / subfolder
            target_dir.mkdir(parents=True, exist_ok=True)
            
            file_ext = Path(file_name).suffix or ".png"
            unique_name = f"{uuid.uuid4().hex[:10]}{file_ext}"
            file_path = target_dir / unique_name

            with open(file_path, "wb") as f:
                f.write(file_bytes)

            relative_url = f"assets/images/{subfolder}/{unique_name}"
            logger.info(f"Image uploaded successfully: {relative_url}")
            return relative_url
        except Exception as e:
            logger.error(f"Error saving uploaded image: {str(e)}")
            return None
