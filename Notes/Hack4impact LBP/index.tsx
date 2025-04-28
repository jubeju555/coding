import React, { useState } from 'react';
import { TextField, Typography, Box, Checkbox, FormControlLabel } from '@mui/material';

const CreateFormQuestion: React.FC = () => {
  const [formTitle, setFormTitle] = useState('');
  const [formDescription, setFormDescription] = useState('');
  const [isRequired, setIsRequired] = useState(false);

  return (
    <Box
      sx={{
        width: '100%',
        maxWidth: '600px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '20px',
        margin: '0 auto',
      }}
    >
      <Typography variant="h5" gutterBottom>
        Create Form Question
      </Typography>
      <TextField
        label="Form Title"
        variant="outlined"
        value={formTitle}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormTitle(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Form Description"
        variant="outlined"
        value={formDescription}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormDescription(e.target.value)}
        multiline
        rows={4}
        fullWidth
        margin="normal"
      />
      <FormControlLabel
        control={
          <Checkbox
            checked={isRequired}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setIsRequired(e.target.checked)}
          />
        }
        label="Required"
      />
    </Box>
  );
};

export default CreateFormQuestion;
