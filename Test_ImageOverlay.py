from PIL import Image

def overlay_images(background_path, overlay_path, output_path):
    # Open the background and overlay images
    background = Image.open(background_path)
    overlay = Image.open(overlay_path)

    # Resize the background image to fit within specified coordinates
    target_size = (561 - 138, 275 - 0)  # Width and height
    resized_background = background.resize(target_size, Image.Resampling.LANCZOS)

    # Create a new blank (white) image (canvas) matching the size of the overlay image
    canvas = Image.new('RGB', overlay.size, (255, 255, 255))

    # Position for the resized background image within specified coordinates
    position = (138, 0)  # Top-left corner

    # Paste the resized background onto the canvas
    canvas.paste(resized_background, position)

    # Overlay the images
    canvas.paste(overlay, (0, 0), overlay)

    # Save the result
    canvas.save(output_path, format="PNG")

# Paths to your images
background_image_path = 'Images/Test_Image.png'
overlay_image_path = 'Images/LofiGirl_NoBackground.png'
output_image_path = 'output.png'

# Function call
overlay_images(background_image_path, overlay_image_path, output_image_path)
