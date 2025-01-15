# NeuroScan: Advanced Brain Tumor Detection System

## Overview

NeuroScan is an advanced brain tumor detection system that utilizes deep learning and image processing techniques to assist in the early identification and analysis of brain tumors from MRI and CT scans.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Usage](#usage)
- [Model Pipeline](#model-pipeline)
- [Data Processing Pipeline](#data-processing-pipeline)
- [Deep Learning Model Architecture](#deep-learning-model-architecture)

## Features

- **User-Friendly Interface**: Easily upload and manage medical images.
- **Advanced Preprocessing**: Perform image normalization, noise reduction, skull stripping, and artifact removal.
- **Data Augmentation**: Enhance datasets with rotation, translation, scaling, flipping, elastic deformation, intensity adjustment, noise injection, shearing, and random cropping.
- **Real-Time Processing**: Quick analysis with efficient algorithms.

## System Architecture

The NeuroScan system comprises a web-based frontend and a Flask backend. Users interact with the application through the web interface, which allows for image upload, preprocessing, augmentation, and tumor detection. The backend handles requests from the frontend, processes images, and utilizes a YOLOv8 deep learning model for tumor detection. Images can be analyzed directly or after optional preprocessing and augmentation steps. Temporary image storage is managed in-memory to ensure efficient processing.

## Usage

1. **Start the Application**:

   ```bash
   python run.py
   ```

2. **Access the Web Interface**:

   Open your web browser and navigate to `http://127.0.0.1:5000`.

3. **Upload Images**:

   - Click on the "Upload Image" button.
   - Select MRI or CT scan images to upload.

4. **Preprocess Images**:

   - Choose preprocessing options like normalization, noise reduction, or skull stripping.

5. **Data Augmentation**:

   - Apply augmentation techniques to enhance your dataset.

## Model Pipeline

The model pipeline involves several key steps:

- **Image Upload**: Users upload MRI or CT images via the web interface.
- **Optional Preprocessing**: Images can be preprocessed to enhance quality, involving techniques like normalization, noise reduction, skull stripping, and artifact removal.
- **Optional Augmentation**: Users can augment images to expand the dataset using various transformations.
- **Tumor Detection**: The YOLOv8 model analyzes the images to detect brain tumors, providing detection results and confidence scores.
- **Results Display**: Detection outcomes are presented to the user through the web interface.

## Data Processing Pipeline

The data processing pipeline includes:

- **Direct Detection**: Uploaded images can be directly analyzed by the YOLOv8 model without preprocessing or augmentation.
- **Preprocessing Steps**: If chosen, images undergo preprocessing to improve detection accuracy.
- **Augmentation Steps**: Users may apply augmentation techniques to create varied data samples.
- **Intermediate Storage**: An in-memory cache temporarily stores images during processing.
- **Detection and Output**: Processed images are passed to the YOLOv8 model, and results are returned to the user.

## Deep Learning Model Architecture

The YOLOv8 model is the core of the tumor detection system:

- **Architecture**: YOLOv8 is an advanced object detection model known for its speed and accuracy, suitable for real-time applications.
- **Processing**: It processes images through convolutional layers to extract features and predicts bounding boxes around detected tumors.
- **Integration**: The model is integrated into the Flask backend and is loaded once at startup for efficiency.
- **Compatibility**: Capable of handling both raw and preprocessed images, providing flexibility in workflow.
