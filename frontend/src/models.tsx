interface BoundingBox {
    x_min: number;
    y_min: number;
    x_max: number;
    y_max: number;
  }
  
  interface Macros {
    protein: number;
    fat: number;
    carbs: number;
    fiber: number;
  }
  
  interface FoodItemVolumeEstimation {
    id: number;
    class_name: string;
    macros: Macros;
    calories: number;
    confidence?: number;
  }
  
  interface VolumeEstimationData {
    food_items: FoodItemVolumeEstimation[];
    summary: string;
  }
  
  interface ClassificationData {
    id: number;
    food_items: {
      id: number;
      class_name: string;
      confidence: number;
      bounding_box: BoundingBox;
    }[];
  }

  interface SegmentationData {
    id: number;
    food_items: {
      id: number;
      class_name: string,
      masked_image:string,
      pixel_area: number,
      total_area: number
  }[]
  }

export type {
    VolumeEstimationData, ClassificationData, FoodItemVolumeEstimation, BoundingBox, Macros, SegmentationData
}