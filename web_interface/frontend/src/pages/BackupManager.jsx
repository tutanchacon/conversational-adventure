import React, { useState, useEffect } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  LinearProgress,
  Alert,
} from '@mui/material'
import {
  Add as AddIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
  Restore as RestoreIcon,
  Delete as DeleteIcon,
  Info as InfoIcon,
} from '@mui/icons-material'
import { toast } from 'react-toastify'

import { apiService } from '../services/api'
import { websocketService } from '../services/websocket'

function BackupManager() {
  const [backups, setBackups] = useState([])
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
  const [selectedBackup, setSelectedBackup] = useState(null)
  const [confirmDialog, setConfirmDialog] = useState(false)

  useEffect(() => {
    loadBackups()
    
    // Escuchar notificaciones de backups
    websocketService.onBackupCreated((data) => {
      toast.success(`Backup creado: ${data.backup_id}`)
      loadBackups()
    })
  }, [])

  const loadBackups = async () => {
    try {
      setLoading(true)
      const data = await apiService.getBackups()
      setBackups(Array.isArray(data) ? data : [])
    } catch (error) {
      console.error('Error cargando backups:', error)
      toast.error('Error cargando lista de backups')
      setBackups([])
    } finally {
      setLoading(false)
    }
  }

  const handleCreateBackup = async () => {
    try {
      setCreating(true)
      toast.info('Creando backup...')
      
      const result = await apiService.createBackup('manual')
      toast.success(`Backup creado exitosamente: ${result.backup_id}`)
      
      // Recargar lista después de un pequeño delay
      setTimeout(loadBackups, 1000)
      
    } catch (error) {
      console.error('Error creando backup:', error)
      toast.error('Error creando backup')
    } finally {
      setCreating(false)
    }
  }

  const formatFileSize = (bytes) => {
    if (!bytes) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getBackupTypeColor = (type) => {
    switch (type) {
      case 'auto': return 'primary'
      case 'manual': return 'secondary'
      case 'scheduled': return 'info'
      default: return 'default'
    }
  }

  const handleBackupInfo = (backup) => {
    setSelectedBackup(backup)
    setConfirmDialog(true)
  }

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 2 }}>
        <LinearProgress />
        <Typography variant="body2" sx={{ mt: 1, textAlign: 'center', color: '#b3b3b3' }}>
          Cargando backups...
        </Typography>
      </Box>
    )
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: 'white', mb: 0.5 }}>
            💾 Gestión de Backups
          </Typography>
          <Typography variant="body2" sx={{ color: '#b3b3b3' }}>
            Administra los respaldos del sistema
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreateBackup}
            disabled={creating}
            sx={{ 
              backgroundColor: '#27ae60',
              '&:hover': { backgroundColor: '#2ecc71' }
            }}
          >
            {creating ? 'Creando...' : 'Crear Backup'}
          </Button>
          
          <IconButton onClick={loadBackups} sx={{ color: '#4a90e2' }}>
            <RefreshIcon />
          </IconButton>
        </Box>
      </Box>

      {/* Estadísticas rápidas */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h5" sx={{ color: '#4a90e2', fontWeight: 'bold' }}>
                {backups.length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Total Backups
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h5" sx={{ color: '#27ae60', fontWeight: 'bold' }}>
                {backups.filter(b => b.backup_type === 'auto').length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Backups Automáticos
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h5" sx={{ color: '#f39c12', fontWeight: 'bold' }}>
                {backups.filter(b => b.backup_type === 'manual').length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Backups Manuales
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h5" sx={{ color: '#9b59b6', fontWeight: 'bold' }}>
                {formatFileSize(backups.reduce((total, b) => total + (b.size_bytes || 0), 0))}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Espacio Total
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Lista de backups */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Lista de Backups
          </Typography>
          
          {backups.length === 0 ? (
            <Alert severity="info" sx={{ backgroundColor: 'rgba(74, 144, 226, 0.1)' }}>
              <Typography variant="body2">
                No hay backups disponibles. Crea tu primer backup usando el botón "Crear Backup".
              </Typography>
            </Alert>
          ) : (
            <TableContainer component={Paper} sx={{ backgroundColor: '#1a1a2e' }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ color: '#ffffff', fontWeight: 'bold' }}>ID del Backup</TableCell>
                    <TableCell sx={{ color: '#ffffff', fontWeight: 'bold' }}>Fecha</TableCell>
                    <TableCell sx={{ color: '#ffffff', fontWeight: 'bold' }}>Tipo</TableCell>
                    <TableCell sx={{ color: '#ffffff', fontWeight: 'bold' }}>Tamaño</TableCell>
                    <TableCell sx={{ color: '#ffffff', fontWeight: 'bold' }}>Archivos</TableCell>
                    <TableCell sx={{ color: '#ffffff', fontWeight: 'bold' }}>Estado</TableCell>
                    <TableCell sx={{ color: '#ffffff', fontWeight: 'bold' }}>Acciones</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {backups.map((backup) => (
                    <TableRow key={backup.backup_id}>
                      <TableCell sx={{ color: '#b3b3b3', fontFamily: 'monospace' }}>
                        {backup.backup_id}
                      </TableCell>
                      <TableCell sx={{ color: '#b3b3b3' }}>
                        {new Date(backup.timestamp).toLocaleString('es-ES')}
                      </TableCell>
                      <TableCell>
                        <Chip 
                          label={backup.backup_type || 'unknown'}
                          color={getBackupTypeColor(backup.backup_type)}
                          size="small"
                        />
                      </TableCell>
                      <TableCell sx={{ color: '#b3b3b3' }}>
                        {formatFileSize(backup.size_bytes)}
                      </TableCell>
                      <TableCell sx={{ color: '#b3b3b3' }}>
                        {backup.files_count || 0}
                      </TableCell>
                      <TableCell>
                        <Chip 
                          label={backup.status || 'completed'}
                          color="success"
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <IconButton
                          size="small"
                          onClick={() => handleBackupInfo(backup)}
                          sx={{ color: '#4a90e2' }}
                        >
                          <InfoIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </CardContent>
      </Card>

      {/* Dialog de información del backup */}
      <Dialog
        open={confirmDialog}
        onClose={() => setConfirmDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle sx={{ backgroundColor: '#1a1a2e', color: '#ffffff' }}>
          Información del Backup
        </DialogTitle>
        <DialogContent sx={{ backgroundColor: '#1a1a2e', color: '#ffffff' }}>
          {selectedBackup && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>ID:</strong> {selectedBackup.backup_id}
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Fecha:</strong> {new Date(selectedBackup.timestamp).toLocaleString('es-ES')}
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Tipo:</strong> {selectedBackup.backup_type}
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Tamaño:</strong> {formatFileSize(selectedBackup.size_bytes)}
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Archivos:</strong> {selectedBackup.files_count}
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Hash de Integridad:</strong> 
                <code style={{ marginLeft: 8, color: '#4a90e2' }}>
                  {selectedBackup.integrity_hash}
                </code>
              </Typography>
              {selectedBackup.game_state_summary && (
                <Typography variant="body1" sx={{ mb: 1 }}>
                  <strong>Estado del Juego:</strong> {selectedBackup.game_state_summary}
                </Typography>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions sx={{ backgroundColor: '#1a1a2e' }}>
          <Button onClick={() => setConfirmDialog(false)} color="primary">
            Cerrar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default BackupManager
