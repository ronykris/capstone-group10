// app/page.tsx
"use client";
import { useState } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Paper, 
  CircularProgress,
  Card,
  CardContent,
  CardHeader
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import ImageInput from "@/components/image-component";
import { IMAGE_CONFIG } from '@/constants';
import Image from 'next/image';
import { BoundingBox, ClassificationData, FoodItemVolumeEstimation, VolumeEstimationData } from '@/models';
import { food_call } from '@/utils/api_processing';


const BoundingBoxOverlay = ({ 
  box, 
  className, 
  color 
}: { 
  box: BoundingBox; 
  className: string; 
  color: string; 
}) => (
  <Box
    sx={{
      position: 'absolute',
      left: box.x_min,
      top: box.y_min,
      width: box.x_max - box.x_min,
      height: box.y_max - box.y_min,
      border: 2,
      borderColor: color,
      display: 'flex',
      alignItems: 'flex-end',
      justifyContent: 'center'
    }}
  >
    <Typography
      sx={{
        bgcolor: 'background.paper',
        px: 1,
        py: 0.5,
        borderRadius: '4px 4px 0 0',
        fontSize: '0.875rem'
      }}
    >
      {className}
    </Typography>
  </Box>
);

const MacrosTable = ({ foodItems }: { foodItems: FoodItemVolumeEstimation[] }) => {
  const processedData = foodItems.map((data, index) => ({...data, id: index}))
  const columns: GridColDef<FoodItemVolumeEstimation>[] = [
    { 
      field: 'class_name', 
      headerName: 'Food Item', 
      flex: 1 
    },
    { 
      field: 'calories', 
      headerName: 'Calories', 
      type: 'number',
      width: 100,
      align: 'right',
      headerAlign: 'right',
    },
    { 
      field: 'fat', 
      headerName: 'Fat (g)', 
      type: 'number',
      width: 130,
      align: 'right',
      headerAlign: 'right',
      valueGetter: (_, value, ...rest) => {
        console.log(value, rest);
        return value?.macros?.fat
      }
    },
    { 
      field: 'protein', 
      headerName: 'Protein (g)', 
      type: 'number',
      width: 130,
      align: 'right',
      headerAlign: 'right',
      valueGetter: (_, value ) => value?.macros?.protein
    },
    { 
      field: 'carbs', 
      headerName: 'Carbs (g)', 
      type: 'number',
      width: 130,
      align: 'right',
      headerAlign: 'right',
      valueGetter: (_, value) => value?.macros?.carbs
    },
    { 
      field: 'fiber', 
      headerName: 'Fiber (g)', 
      type: 'number',
      width: 130,
      align: 'right',
      headerAlign: 'right',
      valueGetter: (_, value) => value?.macros?.fiber
    },
  ];

  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={processedData}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: {
              pageSize: 5,
            },
          },
        }}
        pageSizeOptions={[5, 10, 25]}
        disableRowSelectionOnClick
      />
    </Box>
  );
};

export default function Home() {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [volumeData, setVolumeData] = useState<VolumeEstimationData | null>(null);
  const [classificationData, setClassificationData] = useState<ClassificationData | null>(null);
  const [loading, setLoading] = useState(false);

  const onSubmit = async (image: File) => {
    setLoading(true);
    try {
      const response = await food_call(image);

      setVolumeData(response.volumeData);
      setClassificationData(response.classificationData);
      setImageUrl(URL.createObjectURL(image));
    } catch (error) {
      console.error('Error processing image:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRandomColor = () => {
    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD'];
    return colors[Math.floor(Math.random() * colors.length)];
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom>
        Food Analysis
      </Typography>
      
      <Box sx={{ mb: 4 }}>
        <ImageInput onSubmit={onSubmit} />
      </Box>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress />
          <Typography sx={{ ml: 2 }}>
            Analyzing your image...
          </Typography>
        </Box>
      )}

      {volumeData && (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <Card>
            <CardHeader title="Analysis Summary" />
            <CardContent>
              <Typography color="text.secondary">
                {volumeData.summary}
              </Typography>
            </CardContent>
          </Card>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Nutritional Information
            </Typography>
            <MacrosTable foodItems={volumeData.food_items} />
          </Paper>

          {imageUrl && classificationData && (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Detected Items
              </Typography>
              <Box sx={{ position: 'relative', display: 'inline-block' }}>
                <Image
                  src={imageUrl}
                  alt="Analyzed food"
                  width={IMAGE_CONFIG.width}
                  height={IMAGE_CONFIG.height}
                />
                {classificationData.food_items.map((item) => (
                  <BoundingBoxOverlay
                    key={item.id}
                    box={item.bounding_box}
                    className={item.class_name}
                    color={getRandomColor()}
                  />
                ))}
              </Box>
            </Paper>
          )}
        </Box>
      )}
    </Container>
  );
}