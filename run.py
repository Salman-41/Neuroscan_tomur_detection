import io
import os
import uuid
import cv2
import numpy as np
import logging
from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from src.preprocessing import normalization, noise_reduction, skull_stripping, artifact_removal
from src.augmentation import rotation, translation, scaling, flipping, elastic_deformation, intensity_adjustment, noise_injection, shearing, random_cropping
from ultralytics import YOLO
from pathlib import Path
import time
from typing import Optional, Union

#==============================================================================
# CONFIGURATION AND INITIALIZATION
#==============================================================================
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='web_interface', template_folder='web_interface')
CORS(app)

# Allowed image file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif' 'webp'}

#==============================================================================
# IMAGE STORAGE MANAGEMENT
#==============================================================================
class ImageStore:
    """Persistent cache for storing images with expiration times"""
    def __init__(self):
        self.store = {}
        
    def set(self, key: str, image: np.ndarray, timeout: int = 3600) -> None:
        """Store image with expiration time"""
        self.store[key] = {
            'image': image,
            'expires': time.time() + timeout
        }
        
    def get(self, key: str) -> Optional[np.ndarray]:
        """Get image if it exists and hasn't expired"""
        item = self.store.get(key)
        if item is None:
            return None
            
        if time.time() > item['expires']:
            del self.store[key]
            return None
            
        return item['image']

# Initialize image store
image_store = ImageStore()

#==============================================================================
# MODEL INITIALIZATION
#==============================================================================
try:
    logger.info("Loading YOLOv8 model...")
    model = YOLO('./runs/detect 70_30/train/weights/best.pt')
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading YOLOv8 model: {e}")
    model = None

#==============================================================================
# UTILITY FUNCTIONS
#==============================================================================
def allowed_file(filename: str) -> bool:
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_to_memory(file) -> Union[str, None]:
    """Save uploaded file to memory store with UUID filename"""
    if not (file and allowed_file(file.filename)):
        return None
    
    try:
        unique_filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Store in image_store with 1 hour expiration
        image_store.set(unique_filename, image, timeout=3600)
        return unique_filename
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {e}")
        return None

def convert_to_grayscale(image):
    """Convert RGB image to grayscale if needed"""
    if len(image.shape) == 3:  # If the image has 3 channels (RGB)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

#==============================================================================
# CORE PROCESSING FUNCTIONS
#==============================================================================
def detect_tumor(image_data: np.ndarray) -> tuple:
    """Detect tumors in image using YOLOv8 model"""
    try:
        original_image = image_data.copy()
        rgb_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        results = model(rgb_image)
        
        tumor_detected = False
        detection_info = []
        
        for result in results:
            boxes = getattr(result, 'boxes', None)
            if not boxes:
                continue
                
            tumor_detected = True
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                tumor_label = result.names[class_id]
                
                detection_info.append({
                    'location': f"({x1}, {y1}) to ({x2}, {y2})",
                    'type': tumor_label,
                    'confidence': f"{confidence:.2f}"
                })
                
                # Only draw the bounding box without labels
                cv2.rectangle(original_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        return original_image, tumor_detected, detection_info
        
    except Exception as e:
        logger.error(f"Error during tumor detection: {e}")
        return None, False, []

def handle_processing(process_type, image_data):
    """Handle different types of image preprocessing"""
    # Convert to grayscale for processes that require it
    # if process_type in ['skull_stripping']:
    #     image_data = convert_to_grayscale(image_data)

    processing_map = {
        'normalization': normalization.normalize_image,
        'noise_reduction': noise_reduction.reduce_noise,
        'skull_stripping': skull_stripping.skull_strip,
        'artifact_removal': artifact_removal.remove_artifacts,
    }

    process_func = processing_map.get(process_type)
    if process_func:
        processed_image = process_func(image_data)
        return processed_image
    return None

def handle_augmentation(augment_type, image):
    """Handle different types of image augmentation"""
    augment_map = {
        'rotation': lambda img: rotation.rotate_image(img, 90),
        'translation': lambda img: translation.translate_image(img, 20, 20),
        'scaling': lambda img: scaling.scale_image(img, 3, 3),
        'flipping': lambda img: flipping.flip_image(img, 1),
        'elastic_deformation': lambda img: elastic_deformation.elastic_transform(img, alpha=3),
        'intensity_adjustment': lambda img: intensity_adjustment.adjust_intensity(img, alpha=1.9, beta=20),
        'noise_injection': lambda img: noise_injection.inject_noise(img / 255.0) * 255,
        'shearing': lambda img: shearing.shear_image(img, shear_factor=0.3),
        'random_cropping': lambda img: random_cropping.random_crop(img, crop_size=(100, 100)),
    }

    augment_func = augment_map.get(augment_type)
    if augment_func:
        augmented_image = augment_func(image)
        return augmented_image
    return None

#==============================================================================
# FLASK ROUTES
#==============================================================================
#------------------------------------------------------------------------------
# Main Routes
#------------------------------------------------------------------------------
@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

#------------------------------------------------------------------------------
# Upload Routes
#------------------------------------------------------------------------------
@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload requests"""
    if 'images' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    saved_files = []
    for file in request.files.getlist('images'):
        if filename := save_to_memory(file):
            saved_files.append(filename)

    if not saved_files:
        return jsonify({'error': 'No valid files uploaded'}), 400

    return jsonify({'image_urls': [f'/uploads/{f}' for f in saved_files]}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve stored images"""
    try:
        image = image_store.get(filename)
        if image is None:
            logger.error(f"Image not found in store: {filename}")
            return jsonify({'error': 'File not found'}), 404

        # Convert grayscale to BGR if needed
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        _, buffer = cv2.imencode('.jpg', image)
        io_buf = io.BytesIO(buffer)
        io_buf.seek(0)
        
        return send_file(io_buf, mimetype='image/jpeg')
    except Exception as e:
        logger.error(f"Error serving file {filename}: {e}")
        return jsonify({'error': str(e)}), 500

#------------------------------------------------------------------------------
# Processing Routes
#------------------------------------------------------------------------------
@app.route('/process', methods=['POST'])
def process_images():
    """Handle image preprocessing requests"""
    data = request.get_json()
    process_type = data['type']
    filenames = data['filenames']

    processed_image_urls = []
    for filename in filenames:
        image = image_store.get(filename)
        if image is None:
            logger.warning(f"Image not found in store: {filename}")
            continue
            
        processed_image = handle_processing(process_type, image)
        if processed_image is not None:
            unique_filename = f"{process_type}_{filename}"
            image_store.set(unique_filename, processed_image, timeout=3600)
            processed_image_urls.append(f'/uploads/{unique_filename}')

    if processed_image_urls:
        return jsonify({'image_urls': processed_image_urls}), 200
    else:
        return jsonify({'error': 'Processing failed for all images'}), 400

@app.route('/augment', methods=['POST'])
def augment_images():
    """Handle image augmentation requests"""
    data = request.get_json()
    augment_type = data['type']
    filenames = data['filenames']

    augmented_image_urls = []
    for filename in filenames:
        image = image_store.get(filename)
        if image is None:
            logger.error(f"Image not found: {filename}")
            continue
        augmented_image = handle_augmentation(augment_type, image)
        if augmented_image is not None:
            unique_filename = f"{augment_type}_{filename}"
            image_store.set(unique_filename, augmented_image, timeout=3600)
            augmented_image_urls.append(f'/uploads/{unique_filename}')

    if augmented_image_urls:
        return jsonify({'image_urls': augmented_image_urls}), 200
    else:
        return jsonify({'error': 'Augmentation failed for all images'}), 400

@app.route('/detect', methods=['POST'])
def detect_tumor_route():
    """Handle tumor detection requests"""
    try:
        data = request.get_json()
        filenames = data.get('filenames', [])

        if not filenames:
            logger.warning("Filenames are required.")
            return jsonify({'error': 'Filenames are required'}), 400

        detected_image_urls = []
        tumor_detected_in_any = False
        detection_results = []

        for image_id in filenames:
            # Retrieve the image from memory
            image_data = image_store.get(image_id)

            if image_data is None:
                logger.error(f"Image not found: {image_id}")
                continue

            if model is None:
                logger.error("YOLO model not loaded.")
                return jsonify({'error': 'YOLO model not loaded'}), 500

            # Convert image to uint8 if necessary
            if image_data.dtype != np.uint8:
                image_data = np.clip(image_data, 0, 255)
                image_data = image_data.astype(np.uint8)

            # Detect tumor in the image
            detected_image, tumor_detected, detection_info = detect_tumor(image_data.copy())
            tumor_detected_in_any = tumor_detected_in_any or tumor_detected

            if detected_image is None:
                logger.error(f"Tumor detection failed for image: {image_id}")
                continue

            # Store the detected image back in memory
            detected_image_id = f"detected_{image_id}"
            image_store.set(detected_image_id, detected_image, timeout=3600)

            # Append detection result for this image
            detection_results.append({
                'image_url': f'/uploads/{detected_image_id}',
                'tumor_detected': tumor_detected,
                'details': detection_info
            })

            logger.info(f"Tumor detection completed for image: {image_id}")
            detected_image_urls.append(f'/uploads/{detected_image_id}')

        if detection_results:
            return jsonify({
                'detection_results': detection_results
            }), 200
        else:
            return jsonify({'error': 'Tumor detection failed for all images'}), 400

    except Exception as e:
        logger.exception(f"Error in /detect route: {e}")
        return jsonify({'error': 'Internal server error'}), 500

#------------------------------------------------------------------------------
# Static File Routes
#------------------------------------------------------------------------------
@app.route('/static/favicon/<path:filename>')
def favicon(filename):
    """Serve favicon files"""
    return send_from_directory(
        os.path.join(app.root_path, 'web_interface', 'favicon'),
        filename,
        mimetype='image/svg+xml'
    )

#==============================================================================
# MAIN ENTRY POINT
#==============================================================================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)