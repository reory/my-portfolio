import os
import shutil
from PIL import Image
from loguru import logger


def sync_images():
    """Moves images from root /images to docs/images before optimisation."""

    src = "images"
    dest = "docs/images"
    if os.path.exists(src):
        if not os.path.exists(dest):
            os.makedirs(dest)
        for f in os.listdir(src):
            shutil.copy(os.path.join(src, f), os.path.join(dest, f))
        logger.success("✅ Raw images synced to docs/images")


def optimise_images():
    """Convert portfolio images to optimised WebP (resize + compress)"""

    # Ensure the images directory exists before processing anything.
    source_dir = "docs/images"
    if not os.path.exists(source_dir):
        return

    # Scan source directory for images and prepare .webp output paths for
    # each one.
    for filename in os.listdir(source_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            old_path = os.path.join(source_dir, filename)
            base_name = os.path.splitext(filename)[0]
            new_path = os.path.join(source_dir, f"{base_name}.webp")

            try:
                with Image.open(old_path) as img:

                    # Resize images if too big for Portfolio page.
                    max_width = 800
                    if img.width > max_width:
                        w_percent = max_width / float(img.width)
                        h_size = int((float(img.height) * float(w_percent)))

                        # Resize images
                        img = img.resize(
                            (max_width, h_size), Image.Resampling.LANCZOS
                        )
                        logger.debug(f" Resized {filename} to 600px wide.")

                    # Save as webp
                    img.save(new_path, "WEBP", quality=80)

                # Clean up old file if it was removed as png/jpg
                if old_path != new_path:
                    os.remove(old_path)

            except Exception as e:
                logger.error(f"Failed to optimise {filename}: {e}")
