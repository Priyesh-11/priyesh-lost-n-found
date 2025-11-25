from fastapi import UploadFile, HTTPException
from typing import List, Optional
import cloudinary
import cloudinary.uploader
import cloudinary.api
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self):
        # Configure Cloudinary
        if settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET:
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
                secure=True
            )
            self.configured = True
            logger.info("Cloudinary configured successfully")
        else:
            self.configured = False
            logger.warning("Cloudinary not configured - image uploads will fail")

    def validate_image(self, file: UploadFile) -> bool:
        """
        Validate image file type and size
        """
        # Check file type
        allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Check file size (5MB limit)
        # Note: This is a soft limit, actual enforcement happens during upload
        return True

    async def upload_image(self, file: UploadFile, folder: str = "lost-and-found") -> str:
        """
        Upload image to Cloudinary
        
        Args:
            file: The uploaded file
            folder: Cloudinary folder to store the image in
            
        Returns:
            str: The URL of the uploaded image
        """
        if not self.configured:
            raise HTTPException(
                status_code=500,
                detail="Image upload service not configured"
            )
        
        # Validate the image
        self.validate_image(file)
        
        try:
            # Read file content
            file_content = await file.read()
            
            # Upload to Cloudinary with transformations
            upload_result = cloudinary.uploader.upload(
                file_content,
                folder=folder,
                transformation=[
                    {'width': 1200, 'height': 1200, 'crop': 'limit'},  # Max dimensions
                    {'quality': 'auto:good'},  # Auto quality optimization
                    {'fetch_format': 'auto'}  # Auto format (WebP for supported browsers)
                ],
                allowed_formats=['jpg', 'png', 'jpeg', 'webp'],
                max_file_size=5242880  # 5MB in bytes
            )
            
            # Get the secure URL
            image_url = upload_result.get('secure_url')
            
            if not image_url:
                raise HTTPException(status_code=500, detail="Failed to get image URL")
            
            logger.info(f"Image uploaded successfully: {image_url}")
            return image_url
            
        except cloudinary.exceptions.Error as e:
            logger.error(f"Cloudinary upload error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload image: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error during image upload: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred during image upload"
            )
        finally:
            # Reset file pointer
            await file.seek(0)

    async def upload_multiple_images(
        self, 
        files: List[UploadFile], 
        folder: str = "lost-and-found",
        max_images: int = 5
    ) -> List[str]:
        """
        Upload multiple images to Cloudinary
        
        Args:
            files: List of uploaded files
            folder: Cloudinary folder to store images in
            max_images: Maximum number of images allowed
            
        Returns:
            List[str]: List of URLs of uploaded images
        """
        if len(files) > max_images:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum {max_images} images allowed"
            )
        
        image_urls = []
        for file in files:
            url = await self.upload_image(file, folder)
            image_urls.append(url)
        
        return image_urls

    def delete_image(self, image_url: str) -> bool:
        """
        Delete image from Cloudinary
        
        Args:
            image_url: The URL of the image to delete
            
        Returns:
            bool: True if deletion was successful
        """
        if not self.configured:
            logger.warning("Cloudinary not configured - cannot delete image")
            return False
        
        try:
            # Extract public_id from URL
            # Cloudinary URL format: https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{public_id}.{format}
            parts = image_url.split('/')
            if len(parts) < 2:
                logger.error(f"Invalid Cloudinary URL: {image_url}")
                return False
            
            # Get public_id (folder/filename without extension)
            public_id_with_ext = '/'.join(parts[-2:])  # folder/filename.ext
            public_id = public_id_with_ext.rsplit('.', 1)[0]  # Remove extension
            
            # Delete from Cloudinary
            result = cloudinary.uploader.destroy(public_id)
            
            if result.get('result') == 'ok':
                logger.info(f"Image deleted successfully: {public_id}")
                return True
            else:
                logger.warning(f"Failed to delete image: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting image: {str(e)}")
            return False

# Singleton instance
image_service = ImageService()
