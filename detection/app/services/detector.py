from ultralytics import YOLO
import numpy as np
import io
from PIL import Image
from app.models.schemas import BoundingBox, FoodItemClassification, ClassificationDataModel

class FoodDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def rotate_image_if_portrait(self, img):
       width, height = img.size
       if height > width:
           return img.rotate(-90, expand=True), True
       return img, False

    def detect(self, image_bytes: bytes) -> ClassificationDataModel:
        
        image = Image.open(io.BytesIO(image_bytes))

        rotated_image, was_rotated = self.rotate_image_if_portrait(image)
        
        results = self.model.predict(
            source=rotated_image,
            conf=0.1,
            iou=0.45,
        )

        food_items = []
        for idx, result in enumerate(results):
            if result.boxes is not None:
                boxes = result.boxes.data.cpu().numpy()
                for i, box in enumerate(boxes):
                    food_items.append(
                        FoodItemClassification(
                            id=i,
                            class_name=self.model.names[int(box[5])],
                            confidence=float(box[4]),
                            bounding_box=BoundingBox(
                                x_min=int(box[0]),
                                y_min=int(box[1]),
                                x_max=int(box[2]),
                                y_max=int(box[3])
                            )
                        )
                    )

        return ClassificationDataModel(
            id=idx,
            food_items=food_items
        )