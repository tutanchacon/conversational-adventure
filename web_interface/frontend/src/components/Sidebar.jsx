import React from 'react'
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  Divider,
  IconButton,
  Chip,
  Tooltip,
} from '@mui/material'
import {
  Dashboard as DashboardIcon,
  Backup as BackupIcon,
  Assignment as LogsIcon,
  Analytics as AnalyticsIcon,
  Settings as SettingsIcon,
  Menu as MenuIcon,
  Close as CloseIcon,
  Circle as CircleIcon,
  SportsEsports as GameIcon,
  Castle as CastleIcon,
} from '@mui/icons-material'
import { useNavigate, useLocation } from 'react-router-dom'

const drawerWidth = 280
const collapsedWidth = 70

const menuItems = [
  { path: '/', label: 'Dashboard', icon: DashboardIcon, color: '#4a90e2' },
  { path: '/mcp-editor', label: 'MCP World Editor', icon: CastleIcon, color: '#e67e22' },
  { path: '/backups', label: 'Backups', icon: BackupIcon, color: '#27ae60' },
  { path: '/logs', label: 'System Logs', icon: LogsIcon, color: '#f39c12' },
  { path: '/analytics', label: 'Analytics', icon: AnalyticsIcon, color: '#9b59b6' },
  { path: '/settings', label: 'Settings', icon: SettingsIcon, color: '#7f8c8d' },
]

function Sidebar({ open, onToggle, systemStatus }) {
  const navigate = useNavigate()
  const location = useLocation()

  const getSystemHealthColor = () => {
    if (!systemStatus) return '#7f8c8d' // gris por defecto
    
    const { adventure_game, backup_system } = systemStatus
    
    if (adventure_game?.status === 'running' && backup_system?.status === 'running') {
      return '#27ae60' // verde - todo funcionando
    } else if (adventure_game?.status === 'running' || backup_system?.status === 'running') {
      return '#f39c12' // amarillo - funcionamiento parcial
    } else {
      return '#e74c3c' // rojo - problemas
    }
  }

  const getSystemHealthText = () => {
    if (!systemStatus) return 'Conectando...'
    
    const { adventure_game, backup_system } = systemStatus
    
    if (adventure_game?.status === 'running' && backup_system?.status === 'running') {
      return 'Sistema Saludable'
    } else if (adventure_game?.status === 'running' || backup_system?.status === 'running') {
      return 'Funcionamiento Parcial'
    } else {
      return 'Sistema con Problemas'
    }
  }

  const handleNavigation = (path) => {
    navigate(path)
  }

  const drawerContent = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box
        sx={{
          p: 2,
          background: 'linear-gradient(135deg, #4a90e2 0%, #357abd 100%)',
          color: 'white',
          textAlign: open ? 'left' : 'center',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          {open && (
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center' }}>
                <GameIcon sx={{ mr: 1 }} />
                Adventure Game
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.9 }}>
                Dashboard v2.0
              </Typography>
            </Box>
          )}
          <IconButton
            onClick={onToggle}
            size="small"
            sx={{ color: 'white' }}
          >
            {open ? <CloseIcon /> : <MenuIcon />}
          </IconButton>
        </Box>
      </Box>

      {/* System Status */}
      <Box sx={{ p: open ? 2 : 1, borderBottom: '1px solid #2d2d44' }}>
        <Tooltip title={getSystemHealthText()} placement="right">
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: open ? 'flex-start' : 'center',
            }}
          >
            <CircleIcon
              sx={{
                fontSize: 12,
                color: getSystemHealthColor(),
                mr: open ? 1 : 0,
              }}
            />
            {open && (
              <Typography variant="body2" sx={{ fontSize: '0.75rem' }}>
                {getSystemHealthText()}
              </Typography>
            )}
          </Box>
        </Tooltip>
      </Box>

      {/* Navigation Menu */}
      <List sx={{ flexGrow: 1, py: 1 }}>
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          
          return (
            <ListItem
              key={item.path}
              button
              onClick={() => handleNavigation(item.path)}
              sx={{
                mx: 1,
                mb: 0.5,
                borderRadius: 2,
                backgroundColor: isActive ? 'rgba(74, 144, 226, 0.1)' : 'transparent',
                border: isActive ? '1px solid rgba(74, 144, 226, 0.3)' : '1px solid transparent',
                '&:hover': {
                  backgroundColor: 'rgba(74, 144, 226, 0.05)',
                  border: '1px solid rgba(74, 144, 226, 0.2)',
                },
                justifyContent: open ? 'flex-start' : 'center',
                px: open ? 2 : 1,
              }}
            >
              <Tooltip title={!open ? item.label : ''} placement="right">
                <ListItemIcon
                  sx={{
                    color: isActive ? item.color : '#b3b3b3',
                    minWidth: open ? 40 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                  <Icon />
                </ListItemIcon>
              </Tooltip>
              
              {open && (
                <ListItemText
                  primary={item.label}
                  sx={{
                    color: isActive ? '#ffffff' : '#b3b3b3',
                    '& .MuiListItemText-primary': {
                      fontSize: '0.875rem',
                      fontWeight: isActive ? 500 : 400,
                    },
                  }}
                />
              )}
            </ListItem>
          )
        })}
      </List>

      {/* Footer */}
      {open && (
        <Box sx={{ p: 2, borderTop: '1px solid #2d2d44' }}>
          <Typography variant="caption" sx={{ color: '#7f8c8d', textAlign: 'center', display: 'block' }}>
            Adventure Game Web Interface
          </Typography>
          <Typography variant="caption" sx={{ color: '#7f8c8d', textAlign: 'center', display: 'block' }}>
            Built with ❤️ and React
          </Typography>
        </Box>
      )}
    </Box>
  )

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: open ? drawerWidth : collapsedWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: open ? drawerWidth : collapsedWidth,
          boxSizing: 'border-box',
          backgroundColor: '#1a1a2e',
          borderRight: '1px solid #2d2d44',
          transition: 'width 0.3s ease-in-out',
          overflowX: 'hidden',
        },
      }}
    >
      {drawerContent}
    </Drawer>
  )
}

export default Sidebar
