// components/EnhancedImageViewer.tsx
"use client";
import { useEffect, useRef, useState } from 'react';
import { 
  TransformWrapper, 
  TransformComponent,
  useControls
} from 'react-zoom-pan-pinch';
import { Box, Paper, Typography, IconButton } from '@mui/material';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import ZoomOutIcon from '@mui/icons-material/ZoomOut';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import { FoodItemClassification } from '@/models';

interface Props {
  imageUrl: string;
  foodItems: FoodItemClassification[];
}

const Controls = () => {
  const { zoomIn, zoomOut, resetTransform } = useControls();
  return (
    <Box sx={{ mb: 1 }}>
      <IconButton onClick={() => zoomIn()}>
        <ZoomInIcon />
      </IconButton>
      <IconButton onClick={() => zoomOut()}>
        <ZoomOutIcon />
      </IconButton>
      <IconButton onClick={() => resetTransform()}>
        <RestartAltIcon />
      </IconButton>
    </Box>
  );
};

const EnhancedImageViewer: React.FC<Props> = ({ imageUrl, foodItems }) => {
  const [imageDimensions, setImageDimensions] = useState({ width: 0, height: 0 });
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const image = new Image();
    image.src = imageUrl;
    image.onload = () => {
      setImageDimensions({
        width: image.width,
        height: image.height
      });
      
      if (canvasRef.current && imageRef.current) {
        drawBoundingBoxes();
      }
    };
  }, [imageUrl]);

  const drawBoundingBoxes = () => {
    const canvas = canvasRef.current;
    const image = imageRef.current;
    
    if (!canvas || !image) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear previous drawings
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw bounding boxes
    foodItems.forEach(item => {
      const box = item.bounding_box;
      
      // Draw rectangle
      ctx.strokeStyle = '#FF6B6B';
      ctx.lineWidth = 2;
      ctx.strokeRect(
        box.x_min,
        box.y_min,
        box.x_max - box.x_min,
        box.y_max - box.y_min
      );

      // Draw label
      ctx.fillStyle = '#FF6B6B';
      ctx.fillRect(
        box.x_min,
        box.y_min - 25,
        ctx.measureText(`${item.class_name} ${(item.confidence * 100).toFixed(1)}%`).width + 10,
        20
      );
      
      ctx.fillStyle = 'white';
      ctx.font = '14px Arial';
      ctx.fillText(
        `${item.class_name} ${(item.confidence * 100).toFixed(1)}%`,
        box.x_min + 5,
        box.y_min - 10
      );
    });
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Detected Items
      </Typography>
      
      <TransformWrapper
        initialScale={1}
        minScale={0.5}
        maxScale={4}
        centerOnInit
        onTransformed={drawBoundingBoxes}
      >
        <Controls />
        <TransformComponent
          wrapperStyle={{
            width: '100%',
            height: '100%',
            maxWidth: '800px',
            maxHeight: '600px'
          }}
        >
          <div style={{ position: 'relative' }}>
            <img
              ref={imageRef}
              src={imageUrl}
              alt="Food"
              style={{ width: '100%', height: 'auto' }}
            />
            <canvas
              ref={canvasRef}
              width={imageDimensions.width}
              height={imageDimensions.height}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                pointerEvents: 'none'
              }}
            />
          </div>
        </TransformComponent>
      </TransformWrapper>
    </Paper>
  );
};

export default EnhancedImageViewer;