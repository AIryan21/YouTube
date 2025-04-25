from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_glowing_text(text, font_path, font_size, color, glow_color, blur_radius=6, glow_strength=9):
    font = ImageFont.truetype(font_path, font_size)
    text_bbox = font.getbbox(text)  # Replace getsize with getbbox
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Rest of the code remains the same...

    # Create a transparent image slightly larger to accommodate the glow
    image_width = text_width + 2 * blur_radius * glow_strength
    image_height = text_height + 2 * blur_radius * glow_strength
    image = Image.new("RGBA", (int(image_width), int(image_height)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw the glow layers
    for i in range(glow_strength):
        glow_blur = blur_radius * (glow_strength - i)
        glow_image = Image.new("RGBA", (int(image_width), int(image_height)), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_image)
        glow_draw.text((image_width / 2 - text_width / 2, image_height / 2 - text_height / 2), text, font=font, fill=glow_color)
        glow_image = glow_image.filter(ImageFilter.GaussianBlur(radius=glow_blur))
        image.paste(glow_image, (0, 0), glow_image) # Paste with transparency mask

    # Draw the main text
    draw.text((image_width / 2 - text_width / 2, image_height / 2 - text_height / 2), text, font=font, fill=color)

    return image

# Example usage:
font_path = "./Tillana-Bold.ttf" # Replace with the actual path
glowing_text = create_glowing_text("नमस्ते, आप कैसे हैं", font_path, 48, (255, 255, 255), (255, 255, 0)) # White text, yellow glow

glowing_text.save("glowing_text.png")