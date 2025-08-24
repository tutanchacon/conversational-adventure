import React from 'react'
import { Box, Typography, Alert } from '@mui/material'

function Settings() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" sx={{ color: 'white', mb: 3 }}>
        ⚙️ Settings
      </Typography>
      
      <Alert severity="info" sx={{ backgroundColor: 'rgba(74, 144, 226, 0.1)' }}>
        <Typography variant="body1">
          🚧 Página en construcción
        </Typography>
        <Typography variant="body2" sx={{ mt: 1 }}>
          La configuración del sistema estará disponible próximamente.
        </Typography>
      </Alert>
    </Box>
  )
}

export default Settings
