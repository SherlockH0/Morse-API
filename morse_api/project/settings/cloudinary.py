import cloudinary
import cloudinary.api
import cloudinary.uploader

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,  # pyright: ignore
    api_key=CLOUDINARY_API_KEY,  # pyright: ignore
    api_secret=CLOUDINARY_API_SECRET,  # pyright: ignore
)
