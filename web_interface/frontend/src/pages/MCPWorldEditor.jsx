import React, { useState, useEffect } from 'react';
import {
  Box, Grid, Paper, Typography, Button, TextField, 
  FormControl, InputLabel, Select, MenuItem, Chip,
  Card, CardContent, CardActions, Dialog, DialogTitle,
  DialogContent, DialogActions, Snackbar, Alert,
  List, ListItem, ListItemText, ListItemIcon,
  Tabs, Tab, Divider, IconButton
} from '@mui/material';
import {
  Add, LocationOn, Category, Event, Download,
  Upload, Refresh, Castle, Forest, Store, 
  Security, Build, Diamond, Chair
} from '@mui/icons-material';

const MCPWorldEditor = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [mcpStatus, setMcpStatus] = useState(null);
  const [worldOverview, setWorldOverview] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogType, setDialogType] = useState('location'); // location, object, event
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  
  // Estados para formularios
  const [locationForm, setLocationForm] = useState({
    name: '',
    description: '',
    preset: 'forest',
    connections: [],
    properties: {}
  });
  
  const [objectForm, setObjectForm] = useState({
    name: '',
    description: '',
    location_name: '',
    preset: 'treasure',
    properties: {}
  });
  
  const [eventForm, setEventForm] = useState({
    name: '',
    description: '',
    trigger_type: 'location_enter',
    trigger_value: '',
    action_type: 'message',
    action_data: {},
    properties: {}
  });

  // Cargar estado inicial
  useEffect(() => {
    loadMCPStatus();
    loadWorldOverview();
  }, []);

  const loadMCPStatus = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/mcp/status');
      const data = await response.json();
      setMcpStatus(data);
    } catch (error) {
      console.error('Error cargando estado MCP:', error);
      showSnackbar('Error cargando estado MCP', 'error');
    }
  };

  const loadWorldOverview = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/mcp/world/overview');
      const data = await response.json();
      setWorldOverview(data);
    } catch (error) {
      console.error('Error cargando vista del mundo:', error);
      showSnackbar('Error cargando vista del mundo', 'error');
    }
  };

  const showSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleCreateLocation = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/mcp/locations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(locationForm)
      });
      
      if (response.ok) {
        showSnackbar('Ubicación creada exitosamente');
        setOpenDialog(false);
        loadWorldOverview();
        setLocationForm({ name: '', description: '', preset: 'forest', connections: [], properties: {} });
      } else {
        const error = await response.json();
        showSnackbar(`Error: ${error.detail}`, 'error');
      }
    } catch (error) {
      showSnackbar('Error creando ubicación', 'error');
    }
  };

  const handleCreateObject = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/mcp/objects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(objectForm)
      });
      
      if (response.ok) {
        showSnackbar('Objeto creado exitosamente');
        setOpenDialog(false);
        loadWorldOverview();
        setObjectForm({ name: '', description: '', location_name: '', preset: 'treasure', properties: {} });
      } else {
        const error = await response.json();
        showSnackbar(`Error: ${error.detail}`, 'error');
      }
    } catch (error) {
      showSnackbar('Error creando objeto', 'error');
    }
  };

  const handleCreateEvent = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/mcp/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(eventForm)
      });
      
      if (response.ok) {
        showSnackbar('Evento creado exitosamente');
        setOpenDialog(false);
        loadWorldOverview();
        setEventForm({ 
          name: '', description: '', trigger_type: 'location_enter', 
          trigger_value: '', action_type: 'message', action_data: {}, properties: {} 
        });
      } else {
        const error = await response.json();
        showSnackbar(`Error: ${error.detail}`, 'error');
      }
    } catch (error) {
      showSnackbar('Error creando evento', 'error');
    }
  };

  const exportTemplates = async () => {
    try {
      const response = await fetch('/api/mcp/templates/export');
      const data = await response.json();
      
      // Descargar como archivo JSON
      const blob = new Blob([JSON.stringify(data.templates, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `mcp_templates_${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
      
      showSnackbar('Templates exportados exitosamente');
    } catch (error) {
      showSnackbar('Error exportando templates', 'error');
    }
  };

  const openCreateDialog = (type) => {
    setDialogType(type);
    setOpenDialog(true);
  };

  const getPresetIcon = (preset) => {
    const icons = {
      forest: <Forest />,
      castle: <Castle />,
      shop: <Store />,
      dungeon: <Security />,
      weapon: <Build />,
      treasure: <Diamond />,
      furniture: <Chair />
    };
    return icons[preset] || <Category />;
  };

  if (!mcpStatus) {
    return (
      <Box p={3}>
        <Typography variant="h6">Cargando MCP World Editor...</Typography>
      </Box>
    );
  }

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Castle color="primary" />
        MCP World Editor
      </Typography>

      {/* Estado del sistema */}
      <Paper sx={{ p: 2, mb: 3, bgcolor: 'success.light', color: 'success.contrastText' }}>
        <Typography variant="h6">✅ Sistema MCP Activo</Typography>
        <Typography variant="body2">
          Funciones disponibles: Ubicaciones, Objetos, Eventos, Templates, Export/Import
        </Typography>
      </Paper>

      {/* Botones de acción */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item>
          <Button 
            variant="contained" 
            startIcon={<LocationOn />}
            onClick={() => openCreateDialog('location')}
          >
            Nueva Ubicación
          </Button>
        </Grid>
        <Grid item>
          <Button 
            variant="contained" 
            startIcon={<Category />}
            onClick={() => openCreateDialog('object')}
          >
            Nuevo Objeto
          </Button>
        </Grid>
        <Grid item>
          <Button 
            variant="contained" 
            startIcon={<Event />}
            onClick={() => openCreateDialog('event')}
          >
            Nuevo Evento
          </Button>
        </Grid>
        <Grid item>
          <Button 
            variant="outlined" 
            startIcon={<Download />}
            onClick={exportTemplates}
          >
            Exportar Templates
          </Button>
        </Grid>
        <Grid item>
          <IconButton onClick={loadWorldOverview} color="primary">
            <Refresh />
          </IconButton>
        </Grid>
      </Grid>

      {/* Tabs para diferentes vistas */}
      <Paper>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Ubicaciones" />
          <Tab label="Objetos" />
          <Tab label="Eventos" />
          <Tab label="Vista General" />
        </Tabs>

        {/* Contenido de las tabs */}
        <Box p={3}>
          {activeTab === 0 && (
            <Grid container spacing={2}>
              {worldOverview?.locations?.map((location, index) => (
                <Grid item xs={12} md={6} lg={4} key={index}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <LocationOn color="primary" />
                        {location.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        {location.description}
                      </Typography>
                      {location.connections && location.connections.length > 0 && (
                        <Box sx={{ mt: 2 }}>
                          <Typography variant="caption">Conexiones:</Typography>
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                            {location.connections.map((conn, i) => (
                              <Chip key={i} label={conn} size="small" />
                            ))}
                          </Box>
                        </Box>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}

          {activeTab === 1 && (
            <Grid container spacing={2}>
              {worldOverview?.objects?.map((object, index) => (
                <Grid item xs={12} md={6} lg={4} key={index}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Category color="primary" />
                        {object.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        {object.description}
                      </Typography>
                      <Typography variant="caption" sx={{ mt: 1, display: 'block' }}>
                        Ubicación: {object.location_name}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}

          {activeTab === 2 && (
            <List>
              {worldOverview?.events?.map((event, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    <Event color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary={event.name}
                    secondary={`${event.trigger_type}: ${event.trigger_value} → ${event.action_type}`}
                  />
                </ListItem>
              ))}
            </List>
          )}

          {activeTab === 3 && worldOverview && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="h3" color="primary">
                    {worldOverview.total_locations || 0}
                  </Typography>
                  <Typography variant="h6">Ubicaciones</Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} md={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="h3" color="primary">
                    {worldOverview.total_objects || 0}
                  </Typography>
                  <Typography variant="h6">Objetos</Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} md={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="h3" color="primary">
                    {worldOverview.total_events || 0}
                  </Typography>
                  <Typography variant="h6">Eventos</Typography>
                </Paper>
              </Grid>
            </Grid>
          )}
        </Box>
      </Paper>

      {/* Dialog para crear elementos */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Crear {dialogType === 'location' ? 'Ubicación' : dialogType === 'object' ? 'Objeto' : 'Evento'}
        </DialogTitle>
        <DialogContent>
          {dialogType === 'location' && (
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Nombre"
                  value={locationForm.name}
                  onChange={(e) => setLocationForm({...locationForm, name: e.target.value})}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Descripción"
                  value={locationForm.description}
                  onChange={(e) => setLocationForm({...locationForm, description: e.target.value})}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Preset</InputLabel>
                  <Select
                    value={locationForm.preset}
                    onChange={(e) => setLocationForm({...locationForm, preset: e.target.value})}
                  >
                    <MenuItem value="forest">Bosque</MenuItem>
                    <MenuItem value="castle">Castillo</MenuItem>
                    <MenuItem value="dungeon">Mazmorra</MenuItem>
                    <MenuItem value="shop">Tienda</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          )}

          {dialogType === 'object' && (
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Nombre"
                  value={objectForm.name}
                  onChange={(e) => setObjectForm({...objectForm, name: e.target.value})}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Descripción"
                  value={objectForm.description}
                  onChange={(e) => setObjectForm({...objectForm, description: e.target.value})}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Ubicación"
                  value={objectForm.location_name}
                  onChange={(e) => setObjectForm({...objectForm, location_name: e.target.value})}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Preset</InputLabel>
                  <Select
                    value={objectForm.preset}
                    onChange={(e) => setObjectForm({...objectForm, preset: e.target.value})}
                  >
                    <MenuItem value="weapon">Arma</MenuItem>
                    <MenuItem value="tool">Herramienta</MenuItem>
                    <MenuItem value="treasure">Tesoro</MenuItem>
                    <MenuItem value="furniture">Mueble</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          )}

          {dialogType === 'event' && (
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Nombre"
                  value={eventForm.name}
                  onChange={(e) => setEventForm({...eventForm, name: e.target.value})}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={2}
                  label="Descripción"
                  value={eventForm.description}
                  onChange={(e) => setEventForm({...eventForm, description: e.target.value})}
                />
              </Grid>
              <Grid item xs={6}>
                <FormControl fullWidth>
                  <InputLabel>Tipo de Trigger</InputLabel>
                  <Select
                    value={eventForm.trigger_type}
                    onChange={(e) => setEventForm({...eventForm, trigger_type: e.target.value})}
                  >
                    <MenuItem value="location_enter">Entrar a ubicación</MenuItem>
                    <MenuItem value="object_use">Usar objeto</MenuItem>
                    <MenuItem value="command">Comando</MenuItem>
                    <MenuItem value="time">Tiempo</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Valor del Trigger"
                  value={eventForm.trigger_value}
                  onChange={(e) => setEventForm({...eventForm, trigger_value: e.target.value})}
                />
              </Grid>
              <Grid item xs={6}>
                <FormControl fullWidth>
                  <InputLabel>Tipo de Acción</InputLabel>
                  <Select
                    value={eventForm.action_type}
                    onChange={(e) => setEventForm({...eventForm, action_type: e.target.value})}
                  >
                    <MenuItem value="message">Mensaje</MenuItem>
                    <MenuItem value="spawn_object">Crear objeto</MenuItem>
                    <MenuItem value="modify_object">Modificar objeto</MenuItem>
                    <MenuItem value="change_location">Cambiar ubicación</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Datos de Acción (JSON)"
                  value={JSON.stringify(eventForm.action_data)}
                  onChange={(e) => {
                    try {
                      const data = JSON.parse(e.target.value);
                      setEventForm({...eventForm, action_data: data});
                    } catch {}
                  }}
                />
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancelar</Button>
          <Button 
            variant="contained"
            onClick={
              dialogType === 'location' ? handleCreateLocation :
              dialogType === 'object' ? handleCreateObject :
              handleCreateEvent
            }
          >
            Crear
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar para notificaciones */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({...snackbar, open: false})}
      >
        <Alert severity={snackbar.severity}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default MCPWorldEditor;
