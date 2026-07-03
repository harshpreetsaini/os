#!/usr/bin/env python3
"""Luna OS Image Server - MPC (Model Context Protocol) Server for Image Operations."""

import io
import os
from PIL import Image
from flask import Flask, jsonify, send_file, Response, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Directory paths
UPLOAD_DIR = "/tmp/luna-image-server/uploads"
STATIC_DIR = "/tmp/luna-image-server/static"

# Create directories if they don't exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Default image path
DEFAULT_IMAGE_PATH = "/workspaces/os/IMG_8347.png"


def get_image_info(file_path):
    """Get image information and metadata from a file."""
    if not os.path.exists(file_path):
        return None

    try:
        with Image.open(file_path) as img:
            return {
                "filename": os.path.basename(file_path),
                "path": file_path,
                "format": img.format,
                "mode": img.mode,
                "width": img.width,
                "height": img.height,
                "size_bytes": os.path.getsize(file_path),
                "has_transparency": "transparency" in img.info,
            }
    except Exception:
        return None


@app.route('/api/image/info', methods=['GET'])
def get_image_metadata():
    """Get metadata for the default image."""
    return jsonify(get_image_info(DEFAULT_IMAGE_PATH))


@app.route('/api/image/view', methods=['GET'])
def view_image():
    """View the full-size default image."""
    return send_file(DEFAULT_IMAGE_PATH, mimetype='image/png')


@app.route('/api/image', methods=['GET'])
def api_image():
    """Get a thumbnail of the default image."""
    if not os.path.exists(DEFAULT_IMAGE_PATH):
        return jsonify({"error": "Image not found"}), 404

    try:
        with Image.open(DEFAULT_IMAGE_PATH) as img:
            img.thumbnail((300, 300))

            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)

            return Response(
                img_buffer.getvalue(),
                mimetype='image/png',
                headers={
                    'Content-Disposition': 'inline; filename=luna-thumbnail.png'
                }
            )
    except Exception as e:
        return jsonify({"error": f"Failed to generate thumbnail: {str(e)}"}), 500


@app.route('/api/image/info/<filename>', methods=['GET'])
def get_image_metadata_filename(filename):
    """Get metadata for a specific uploaded image."""
    file_path = os.path.join(STATIC_DIR, filename)
    return jsonify(get_image_info(file_path))


@app.route('/api/images', methods=['GET'])
def list_images():
    """List all images in the static directory."""
    try:
        images = []
        for filename in os.listdir(STATIC_DIR):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')):
                file_path = os.path.join(STATIC_DIR, filename)
                info = get_image_info(file_path)
                if info:
                    images.append(info)

        return jsonify({
            "total_images": len(images),
            "images": images
        })
    except Exception:
        return jsonify({"error": "Failed to list images"}), 500


@app.route('/api/image/upload', methods=['POST'])
def upload_image():
    """Upload an image file."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')):
        return jsonify({"error": "Unsupported file format"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(STATIC_DIR, filename)
    file.save(file_path)

    return jsonify({
        "message": "File uploaded successfully",
        "filename": filename,
        "path": file_path
    })


@app.route('/api/process/image', methods=['POST'])
def process_image():
    """Process an image with various operations."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        operation = data.get('operation')
        if not operation:
            return jsonify({"error": "No operation specified"}), 400

        image_path = data.get('image_path')
        if not image_path:
            image_path = DEFAULT_IMAGE_PATH

        if not os.path.exists(image_path):
            return jsonify({"error": "Image not found"}), 404

        with Image.open(image_path) as img:
            if operation in ['grayscale', 'blur', 'sharpen', 'edges'] and img.mode != 'RGB':
                img = img.convert('RGB')

            if operation == 'grayscale':
                img = img.convert('L')

            elif operation == 'resize':
                width = data.get('width', 200)
                height = data.get('height', 200)
                img = img.resize((width, height))

            elif operation == 'crop':
                left = data.get('left', 0)
                top = data.get('top', 0)
                right = data.get('right', img.width)
                bottom = data.get('bottom', img.height)
                img = img.crop((left, top, right, bottom))

            elif operation == 'rotate':
                angle = data.get('angle', 90)
                img = img.rotate(angle, expand=True)

            elif operation == 'blur':
                from PIL import ImageFilter
                radius = data.get('radius', 2)
                img = img.filter(ImageFilter.GaussianBlur(radius=radius))

            elif operation == 'sharpen':
                from PIL import ImageFilter
                img = img.filter(ImageFilter.SHARPEN)

            elif operation == 'edges':
                from PIL import ImageFilter
                img = img.filter(ImageFilter.FIND_EDGES)

            elif operation == 'contrast':
                from PIL import ImageEnhance
                enhancer = ImageEnhance.Contrast(img)
                factor = data.get('factor', 1.5)
                img = enhancer.enhance(factor)

            elif operation == 'brightness':
                from PIL import ImageEnhance
                enhancer = ImageEnhance.Brightness(img)
                factor = data.get('factor', 1.5)
                img = enhancer.enhance(factor)

            elif operation == 'colorize':
                from PIL import ImageEnhance
                enhancer = ImageEnhance.Color(img)
                factor = data.get('factor', 1.5)
                img = enhancer.enhance(factor)

            elif operation == 'sepia':
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                sepia_filter = Image.new('RGB', img.size)
                pixels = sepia_filter.load()

                for py in range(img.height):
                    for px in range(img.width):
                        r, g, b = img.getpixel((px, py))
                        tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                        tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                        tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                        tr = min(tr, 255)
                        tg = min(tg, 255)
                        tb = min(tb, 255)

                        pixels[px, py] = (tr, tg, tb)
                img = sepia_filter

            elif operation == 'invert':
                if img.mode == 'RGB':
                    r, g, b = img.split()
                    r = r.point(lambda x: 255 - x)
                    g = g.point(lambda x: 255 - x)
                    b = b.point(lambda x: 255 - x)
                    img = Image.merge('RGB', (r, g, b))
                elif img.mode == 'L':
                    img = img.point(lambda x: 255 - x)
                elif img.mode == 'RGBA':
                    r, g, b, a = img.split()
                    r = r.point(lambda x: 255 - x)
                    g = g.point(lambda x: 255 - x)
                    b = b.point(lambda x: 255 - x)
                    img = Image.merge('RGBA', (r, g, b, a))

            else:
                return jsonify({"error": f"Unsupported operation: {operation}"}), 400

            output_buffer = io.BytesIO()
            img.save(output_buffer, format='PNG')
            output_buffer.seek(0)

            return Response(
                output_buffer.getvalue(),
                mimetype='image/png',
                headers={
                    'Content-Disposition': f'inline; filename=processed-{operation}.png'
                }
            )

    except Exception as e:
        return jsonify({"error": f"Image processing failed: {str(e)}"}), 500


@app.route('/api/search/images', methods=['GET'])
def search_images():
    """Search images by filename, format, or properties."""
    try:
        filename_pattern = request.args.get('filename_pattern', '')
        min_width = request.args.get('min_width', type=int)
        max_width = request.args.get('max_width', type=int)
        min_height = request.args.get('min_height', type=int)
        max_height = request.args.get('max_height', type=int)
        min_size = request.args.get('min_size', type=int)
        max_size = request.args.get('max_size', type=int)
        has_transparency = request.args.get('has_transparency', type=bool)
        format_type = request.args.get('format')

        images = []
        for filename in os.listdir(STATIC_DIR):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')):
                file_path = os.path.join(STATIC_DIR, filename)
                info = get_image_info(file_path)
                if info:
                    if filename_pattern and filename_pattern not in filename:
                        continue
                    if format_type and info['format'].upper() != format_type.upper():
                        continue
                    if min_width and info['width'] < min_width:
                        continue
                    if max_width and info['width'] > max_width:
                        continue
                    if min_height and info['height'] < min_height:
                        continue
                    if max_height and info['height'] > max_height:
                        continue
                    if min_size and info['size_bytes'] < min_size:
                        continue
                    if max_size and info['size_bytes'] > max_size:
                        continue
                    if has_transparency is not None and info['has_transparency'] != has_transparency:
                        continue

                    images.append(info)

        return jsonify({
            "total_images": len(images),
            "query_params": {
                "filename_pattern": filename_pattern,
                "min_width": min_width,
                "max_width": max_width,
                "min_height": min_height,
                "max_height": max_height,
                "min_size": min_size,
                "max_size": max_size,
                "has_transparency": has_transparency,
                "format": format_type,
            },
            "images": images
        })
    except Exception:
        return jsonify({"error": "Failed to search images"}), 500


@app.route('/api/compare/images', methods=['POST'])
def compare_images():
    """Compare two images and return similarity metrics."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        image_path1 = data.get('image_path1')
        image_path2 = data.get('image_path2')

        if not image_path1 or not os.path.exists(image_path1):
            return jsonify({"error": "First image not found"}), 404

        if not image_path2 or not os.path.exists(image_path2):
            return jsonify({"error": "Second image not found"}), 404

        with Image.open(image_path1) as img1, Image.open(image_path2) as img2:
            if img1.mode in ('RGBA', 'LA'):
                img1 = img1.convert('RGB')
            if img2.mode in ('RGBA', 'LA'):
                img2 = img2.convert('RGB')

            max_size = (100, 100)
            img1.thumbnail(max_size)
            img2.thumbnail(max_size)

            if img1.mode != 'L':
                img1 = img1.convert('L')
            if img2.mode != 'L':
                img2 = img2.convert('L')

            if img1.size != img2.size:
                final_size = (max(img1.width, img2.width), max(img1.height, img2.height))
                new_img1 = Image.new('L', final_size, 0)
                new_img2 = Image.new('L', final_size, 0)

                new_img1.paste(img1, (0, 0))
                new_img2.paste(img2, (0, 0))
                img1, img2 = new_img1, new_img2

            pixels1 = list(img1.getdata())
            pixels2 = list(img2.getdata())

            if len(pixels1) != len(pixels2):
                return jsonify({"error": "Images have different number of pixels"}), 400

            mse = sum((p1 - p2) ** 2 for p1, p2 in zip(pixels1, pixels2)) / len(pixels1)
            max_mse = 255 ** 2
            similarity = max(0, 1 - (mse / max_mse))

            return jsonify({
                "image1_info": get_image_info(image_path1),
                "image2_info": get_image_info(image_path2),
                "similarity_score": round(similarity, 4),
                "metrics": {
                    "mean_squared_error": round(mse, 2),
                    "pixel_difference_count": sum(1 for p1, p2 in zip(pixels1, pixels2) if p1 != p2),
                    "identical_pixels": sum(1 for p1, p2 in zip(pixels1, pixels2) if p1 == p2)
                }
            })

    except Exception as e:
        return jsonify({"error": f"Image comparison failed: {str(e)}"}), 500


@app.route('/', methods=['GET'])
def index():
    """Root endpoint - return server information."""
    return jsonify({
        "service": "Luna OS Image Server",
        "version": "2.0.0",
        "protocol": "MPC (Model Context Protocol)",
        "host": "127.0.0.1:5252",
        "description": "Full-featured image processing and management server",
        "status": "running",
        "endpoints": [
            "GET /api/image/info - Get metadata for default image",
            "GET /api/image/view - View full-size default image",
            "GET /api/image - Get thumbnail of default image",
            "GET /api/image/info/<filename> - Get metadata for uploaded image",
            "GET /api/images - List all uploaded images",
            "POST /api/image/upload - Upload an image",
            "POST /api/process/image - Process an image",
            "GET /api/search/images - Search images",
            "POST /api/compare/images - Compare two images"
        ]
    })


if __name__ == '__main__':
    print("Starting Luna OS Image Server on http://127.0.0.1:5252")
    app.run(host="127.0.0.1", port=5252)
