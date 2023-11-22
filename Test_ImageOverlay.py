from PIL import Image

def overlay_images(background_path, overlay_path, output_path):
    # Open the background and overlay images
    background = Image.open(background_path)
    overlay = Image.open(overlay_path)

    # Resize overlay image to match the background's size if necessary
    # Uncomment the next line if you want to resize
    # overlay = overlay.resize(background.size, Image.ANTIALIAS)

    # Overlay the images
    background.paste(overlay, (0, 0), overlay)
    # The (0, 0) is the top left corner where the overlay starts

    # Save the result
    background.save(output_path, format="PNG")

# Paths to your images
background_image_path = 'path/to/your/background.jpg'
overlay_image_path = 'path/to/your/overlay.png'
output_image_path = 'path/to/your/output.png'

# Function call
overlay_images(background_image_path, overlay_image_path, output_image_path)
