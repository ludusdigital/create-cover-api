from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

app = Flask(__name__)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    text = data.get('text', 'Default Text')
    
    # Load template image
    template_image = Image.open('template.jpeg')
    draw = ImageDraw.Draw(template_image)
    
    # Define font and size (make sure the font file is available in your directory)
    font = ImageFont.truetype('PlusJakartaSans.ttf', 60)

    # Define the maximum width of the text box
    max_width = 700  # Prilagodite širinu prema veličini vaše slike

    # Wrap the text
    lines = textwrap.wrap(text, width=30)  # Prilagodite širinu prema potrebi
    
    # Position where the text will be added (adjust as needed)
    position = (60, 60)
    line_spacing = 20  # Dodajte razmak između redova (u pikselima)
    
    # Add text to image
    y_text = position[1]
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        draw.text((position[0], y_text), line, font=font, fill='white')
        y_text += height + line_spacing  # Dodajte razmak između redova
    
    # Save image to a bytes buffer
    img_io = io.BytesIO()
    template_image.save(img_io, 'JPEG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)

