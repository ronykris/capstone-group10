import { Backend, getUrl } from "@/constants"
import { ClassificationData, SegmentationData, VolumeEstimationData } from "@/models";

const classificationProcessing = async (image: File) => {
    const baseUrl = getUrl(Backend.classification);
    const url = `${baseUrl}/detect`;
    
    try {
        const formData = new FormData();
        formData.append("file", image);

        const response = await fetch(url, {
            method: "POST",
            body: formData,
            headers: {
                // Add any necessary headers here
                // 'Content-Type': 'multipart/form-data', // Let the browser set this for FormData
            },
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data: ClassificationData = await response.json();
        return data; // Return the response data

    } catch (error) {
        console.error("Error processing classification:", error);
        throw error; // Re-throw the error after logging it
    }
};

const segmentationProcessing = async (image: File, classificationData: ClassificationData) => {
    const baseUrl = getUrl(Backend.segmentation);
    const url = `${baseUrl}/api/v1/segment`;
    
    try {
        const foodItems: SegmentationData['food_items'] = [];
        await Promise.all(classificationData.food_items.map(async (fi) => {
            const formData = new FormData();
            const singleClas:ClassificationData = {
                id: 1,
                food_items: [
                    fi
                ]
            } 
            formData.append("file", image);
            formData.append("classification_data", JSON.stringify(singleClas));
    
            const response = await fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    // Add any necessary headers here
                    // 'Content-Type': 'multipart/form-data', // Let the browser set this for FormData
                },
            });
    
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
    
            const data: SegmentationData = await response.json();
            foodItems.push(data.food_items[0])
        }))
        const response: SegmentationData = {
            id: 1,
            food_items: foodItems
        }
        return response; // Return the response data

    } catch (error) {
        console.error("Error processing classification:", error);
        throw error; // Re-throw the error after logging it
    }
};

const volumeEstProcessing = async (image: File, classificationData: ClassificationData, segmentationData: SegmentationData) => {
    const baseUrl = getUrl(Backend.volume);
    const url = `${baseUrl}/api/v1/volume-estimate`;
    
    try {
        const formData = new FormData();
        formData.append("file", image);
        formData.append("classification_data", JSON.stringify(classificationData));
        formData.append("segmentation_data", JSON.stringify(segmentationData));

        const response = await fetch(url, {
            method: "POST",
            body: formData,
            headers: {
                // Add any necessary headers here
                // 'Content-Type': 'multipart/form-data', // Let the browser set this for FormData
            },
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data: VolumeEstimationData = await response.json();
        return data; // Return the response data

    } catch (error) {
        console.error("Error processing classification:", error);
        throw error; // Re-throw the error after logging it
    }
};


const food_call = async (image: File) => {
    // classification call
    const classificationData = await classificationProcessing(image);
    // segmentation call
    const segmentationData = await segmentationProcessing(image, classificationData);

    // volume estimation call
    const volumeData = await volumeEstProcessing(image, classificationData, segmentationData);
    
    return {
        classificationData, volumeData
    }
}

export {
    food_call
}