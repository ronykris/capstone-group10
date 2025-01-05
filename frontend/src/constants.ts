const BASE_DOMAIN = "http://localhost"
enum Backend {
    volume, segmentation, classification, foodSegmentation
}
const PORTS = {
    [Backend.volume]: 8003,
    [Backend.segmentation]: 8002,
    [Backend.classification]: 8000,
    [Backend.foodSegmentation]: 8004,
}
const getUrl = (backend: Backend) => `${BASE_DOMAIN}:${PORTS[backend]}`;

const IMAGE_CONFIG = {
    height: 400, 
    width: 400
}
export {
    getUrl,
    IMAGE_CONFIG,
    Backend
}