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
import { ClassificationData, FoodItemVolumeEstimation, VolumeEstimationData } from '@/models';
import { food_call } from '@/utils/api_processing';
import EnhancedImageViewer from '@/components/interfactive-image';



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
      valueGetter: (_, value,) => value?.macros?.fat
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
            <EnhancedImageViewer 
              imageUrl={imageUrl}
              foodItems={classificationData.food_items}
            />
          )}
        </Box>
      )}
    </Container>
  );
}