import React, { useState, useEffect } from 'react'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import { CssBaseline, Box, CircularProgress, Typography, Alert } from '@mui/material'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

// Components
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import BackupManager from './pages/BackupManager'
import SystemLogs from './pages/SystemLogs'
import Analytics from './pages/Analytics'
import Settings from './pages/Settings'
import MCPWorldEditor from './pages/MCPWorldEditor'

// Services
import { apiService } from './services/api'
import { websocketService } from './services/websocket'

// Theme personalizado para Adventure Game
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#4a90e2',
      light: '#7bb3f0',
      dark: '#357abd',
    },
    secondary: {
      main: '#f39c12',
      light: '#f7dc6f',
      dark: '#d68910',
    },
    background: {
      default: '#0f1419',
      paper: '#1a1a2e',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b3b3b3',
    },
    success: {
      main: '#27ae60',
    },
    error: {
      main: '#e74c3c',
    },
    warning: {
      main: '#f39c12',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
      color: '#ffffff',
    },
    h5: {
      fontWeight: 500,
      color: '#ffffff',
    },
    h6: {
      fontWeight: 500,
      color: '#ffffff',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#1a1a2e',
          border: '1px solid #2d2d44',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#1a1a2e',
          border: '1px solid #2d2d44',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: '8px',
        },
      },
    },
  },
})

function App() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [systemStatus, setSystemStatus] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    initializeApp()
  }, [])

  const initializeApp = async () => {
    try {
      setLoading(true)
      setError(null)

      // Verificar conexión con el backend
      console.log('🚀 Inicializando Adventure Game Dashboard...')
      
      const healthCheck = await apiService.checkHealth()
      console.log('✅ Backend conectado:', healthCheck)

      // Obtener estado del sistema
      const status = await apiService.getSystemStatus()
      setSystemStatus(status)
      console.log('📊 Estado del sistema:', status)

      // Inicializar WebSocket
      websocketService.connect()
      websocketService.onMessage((message) => {
        console.log('📡 WebSocket mensaje:', message)
        
        if (message.type === 'metrics_update') {
          // Actualizar métricas en tiempo real
          // Este evento lo manejarán los componentes individuales
        }
      })

      setLoading(false)
      console.log('🎉 Dashboard inicializado correctamente')

    } catch (err) {
      console.error('❌ Error inicializando app:', err)
      setError(err.message || 'Error de conexión con el servidor')
      setLoading(false)
    }
  }

  const handleRetry = () => {
    initializeApp()
  }

  if (loading) {
    return (
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <Box className="loading-container">
          <Box textAlign="center">
            <CircularProgress size={60} color="primary" />
            <Typography variant="h6" sx={{ mt: 2, color: 'white' }}>
              🎮 Cargando Adventure Game Dashboard...
            </Typography>
            <Typography variant="body2" sx={{ mt: 1, color: '#b3b3b3' }}>
              Conectando con el servidor backend
            </Typography>
          </Box>
        </Box>
      </ThemeProvider>
    )
  }

  if (error) {
    return (
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <Box className="error-container">
          <Alert 
            severity="error" 
            sx={{ mb: 3, maxWidth: 500 }}
            action={
              <button onClick={handleRetry} style={{
                background: 'none',
                border: 'none',
                color: '#4a90e2',
                cursor: 'pointer',
                textDecoration: 'underline'
              }}>
                Reintentar
              </button>
            }
          >
            <Typography variant="h6">Error de Conexión</Typography>
            <Typography variant="body2">{error}</Typography>
          </Alert>
          
          <Typography variant="body1" color="textSecondary" sx={{ mb: 2 }}>
            🔧 Asegúrate de que el servidor backend esté ejecutándose:
          </Typography>
          <Typography variant="body2" component="pre" sx={{ 
            backgroundColor: '#1a1a2e', 
            p: 2, 
            borderRadius: 1,
            fontSize: '0.875rem'
          }}>
            python .\web_interface\backend\app\demo_server.py
          </Typography>
        </Box>
      </ThemeProvider>
    )
  }

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <Box className="adventure-dashboard" sx={{ display: 'flex', minHeight: '100vh' }}>
          <Sidebar 
            open={sidebarOpen} 
            onToggle={() => setSidebarOpen(!sidebarOpen)}
            systemStatus={systemStatus}
          />
          
          <Box
            component="main"
            sx={{
              flexGrow: 1,
              p: 3,
              width: { sm: `calc(100% - ${sidebarOpen ? 280 : 70}px)` },
              ml: { sm: sidebarOpen ? '280px' : '70px' },
              transition: 'margin 0.3s ease-in-out',
              backgroundColor: '#0f1419',
              minHeight: '100vh',
            }}
          >
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/mcp-editor" element={<MCPWorldEditor />} />
              <Route path="/backups" element={<BackupManager />} />
              <Route path="/logs" element={<SystemLogs />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Box>
        </Box>

        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="dark"
        />
      </Router>
    </ThemeProvider>
  )
}

export default App
