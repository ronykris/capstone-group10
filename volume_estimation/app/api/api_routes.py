from fastapi import APIRouter, File, Form, HTTPException, UploadFile
import json
import logging
from typing import List

from ..lib.models import ClassificationDataModel, SegmentationDataModel, VolumeEstimationDataModel
from ..utils.volume_estimator import VolumeEstimator
from ..utils.image_processing import ImageProcessor

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/volume-estimate", response_model=VolumeEstimationDataModel)
async def estimate_volume(
    file: UploadFile = File(...),
    classification_data: str = Form(...),
    segmentation_data: str = Form(...)
):
    try:
        # Parse input data using Pydantic V2 syntax
        try:
            classification = ClassificationDataModel.model_validate_json(classification_data)
            segmentation = SegmentationDataModel.model_validate_json(segmentation_data)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"Invalid input data: {str(e)}")
        
        # Process image
        image_processor = ImageProcessor()
        image = await image_processor.process_upload(file)
        
        # Estimate volume
        estimator = VolumeEstimator()
        result = await estimator.estimate(image, classification, segmentation)
        
        return result
    except Exception as e:
        logger.error(f"Volume estimation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/healthcheck")
async def healthcheck():
    return {"status": "healthy"}