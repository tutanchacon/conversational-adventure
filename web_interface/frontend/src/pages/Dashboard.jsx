import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  LinearProgress,
  Chip,
  IconButton,
  Tooltip,
  Paper,
  Alert,
} from '@mui/material'
import {
  Refresh as RefreshIcon,
  TrendingUp as TrendingUpIcon,
  Storage as StorageIcon,
  Speed as SpeedIcon,
  Backup as BackupIcon,
  Timeline as TimelineIcon,
  Memory as MemoryIcon,
  Event as EventIcon,
} from '@mui/icons-material'
import { Line, Doughnut, Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  BarElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
} from 'chart.js'

import { apiService } from '../services/api'
import { websocketService } from '../services/websocket'
import { toast } from 'react-toastify'

// Registrar componentes de Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  BarElement,
  Title,
  ChartTooltip,
  Legend
)

function Dashboard() {
  const [metrics, setMetrics] = useState(null)
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  useEffect(() => {
    loadDashboardData()
    
    // Escuchar actualizaciones en tiempo real
    websocketService.onMetricsUpdate((data) => {
      console.log('📊 Métricas actualizadas:', data)
      setMetrics(data.data)
      setLastUpdate(new Date())
    })

    // Actualizar cada 30 segundos como fallback
    const interval = setInterval(loadDashboardData, 30000)
    
    return () => clearInterval(interval)
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      
      const [metricsData, analyticsData] = await Promise.all([
        apiService.getMetrics(),
        apiService.getAnalytics('24h')
      ])

      setMetrics(metricsData)
      setAnalytics(analyticsData)
      setLastUpdate(new Date())
      
    } catch (error) {
      console.error('Error cargando dashboard:', error)
      toast.error('Error cargando datos del dashboard')
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = () => {
    toast.info('Actualizando dashboard...')
    loadDashboardData()
  }

  // Configuración de gráficos
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#ffffff',
        },
      },
    },
    scales: {
      x: {
        ticks: { color: '#b3b3b3' },
        grid: { color: '#2d2d44' },
      },
      y: {
        ticks: { color: '#b3b3b3' },
        grid: { color: '#2d2d44' },
      },
    },
  }

  // Datos para el gráfico de línea (eventos por hora)
  const getEventsChartData = () => {
    if (!analytics?.data_points) return null

    return {
      labels: analytics.data_points.map(point => 
        new Date(point.timestamp).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
      ),
      datasets: [
        {
          label: 'Eventos por Hora',
          data: analytics.data_points.map(point => point.events),
          borderColor: '#4a90e2',
          backgroundColor: 'rgba(74, 144, 226, 0.1)',
          tension: 0.4,
          fill: true,
        },
      ],
    }
  }

  // Datos para el gráfico de uso de recursos
  const getResourcesChartData = () => {
    if (!analytics?.data_points) return null

    return {
      labels: ['CPU', 'Memoria', 'Almacenamiento'],
      datasets: [
        {
          data: [65, 45, 25], // Datos simulados
          backgroundColor: ['#e74c3c', '#f39c12', '#27ae60'],
          borderWidth: 0,
        },
      ],
    }
  }

  if (loading && !metrics) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress size={60} />
      </Box>
    )
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: 'white', mb: 0.5 }}>
            🎮 Adventure Game Dashboard
          </Typography>
          <Typography variant="body2" sx={{ color: '#b3b3b3' }}>
            Última actualización: {lastUpdate.toLocaleTimeString('es-ES')}
          </Typography>
        </Box>
        
        <Tooltip title="Actualizar Dashboard">
          <IconButton onClick={handleRefresh} sx={{ color: '#4a90e2' }}>
            <RefreshIcon />
          </IconButton>
        </Tooltip>
      </Box>

      {/* Métricas principales */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="h4" sx={{ color: '#4a90e2', fontWeight: 'bold' }}>
                    {metrics?.uptime_formatted || '---'}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Tiempo Activo
                  </Typography>
                </Box>
                <SpeedIcon sx={{ fontSize: 40, color: '#4a90e2', opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="h4" sx={{ color: '#27ae60', fontWeight: 'bold' }}>
                    {metrics?.requests_count || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Requests Totales
                  </Typography>
                </Box>
                <TrendingUpIcon sx={{ fontSize: 40, color: '#27ae60', opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="h4" sx={{ color: '#f39c12', fontWeight: 'bold' }}>
                    {metrics?.events_count || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Eventos del Juego
                  </Typography>
                </Box>
                <EventIcon sx={{ fontSize: 40, color: '#f39c12', opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="h4" sx={{ color: '#9b59b6', fontWeight: 'bold' }}>
                    {metrics?.total_backups || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Backups Disponibles
                  </Typography>
                </Box>
                <BackupIcon sx={{ fontSize: 40, color: '#9b59b6', opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Estado del sistema */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={8}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                <TimelineIcon sx={{ mr: 1, color: '#4a90e2' }} />
                Actividad del Sistema (Últimas 24h)
              </Typography>
              
              <Box sx={{ height: 300 }}>
                {getEventsChartData() ? (
                  <Line data={getEventsChartData()} options={chartOptions} />
                ) : (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <CircularProgress />
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                <MemoryIcon sx={{ mr: 1, color: '#f39c12' }} />
                Uso de Recursos
              </Typography>
              
              <Box sx={{ height: 250, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                {getResourcesChartData() ? (
                  <Doughnut 
                    data={getResourcesChartData()} 
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'bottom',
                          labels: { color: '#ffffff' },
                        },
                      },
                    }} 
                  />
                ) : (
                  <CircularProgress />
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Información adicional */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                🔌 Conexiones WebSocket
              </Typography>
              
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Typography variant="body1" sx={{ mr: 2 }}>
                  Conexiones Activas:
                </Typography>
                <Chip 
                  label={metrics?.active_websockets || 0}
                  color="primary"
                  size="small"
                />
              </Box>

              <LinearProgress 
                variant="determinate" 
                value={(metrics?.active_websockets || 0) * 10} 
                sx={{ 
                  height: 8, 
                  borderRadius: 4,
                  backgroundColor: '#2d2d44',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: '#4a90e2',
                  },
                }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                💾 Estado de Backups
              </Typography>
              
              {metrics?.last_backup ? (
                <Alert severity="success" sx={{ backgroundColor: 'rgba(39, 174, 96, 0.1)' }}>
                  <Typography variant="body2">
                    Último backup: {new Date(metrics.last_backup).toLocaleString('es-ES')}
                  </Typography>
                </Alert>
              ) : (
                <Alert severity="warning" sx={{ backgroundColor: 'rgba(243, 156, 18, 0.1)' }}>
                  <Typography variant="body2">
                    No hay información de backups recientes
                  </Typography>
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default Dashboard
