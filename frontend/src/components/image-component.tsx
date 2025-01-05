// components/ImageInput.tsx
"use client"
import { useState } from 'react';
import { 
  Box, 
  Button, 
  Paper,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import Image from 'next/image';
import { IMAGE_CONFIG } from '@/constants';

interface ImageInputProps {
  onSubmit: (image: File) => void;
}

const ImageInput: React.FC<ImageInputProps> = ({ onSubmit }) => {
  const [image, setImage] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const selectedImage = event.target.files[0];
      setImage(selectedImage);
      setImageUrl(URL.createObjectURL(selectedImage));
    }
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (image) {
      onSubmit(image);
    }
  };

  return (
    <Paper sx={{ p: 3 }}>
      <form onSubmit={handleSubmit}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <input
            accept="image/*"
            style={{ display: 'none' }}
            id="image-upload"
            type="file"
            onChange={handleImageChange}
          />
          <label htmlFor="image-upload">
            <Button
              variant="contained"
              component="span"
              startIcon={<CloudUploadIcon />}
            >
              Select Image
            </Button>
          </label>
          
          {imageUrl && (
            <Box sx={{ mt: 2 }}>
              <Image
                src={imageUrl}
                alt="Selected"
                width={IMAGE_CONFIG.width}
                height={IMAGE_CONFIG.height}
              />
            </Box>
          )}

          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={!image}
            sx={{ mt: 2, alignSelf: 'flex-start' }}
          >
            Analyze Image
          </Button>
        </Box>
      </form>
    </Paper>
  );
};

export default ImageInput;