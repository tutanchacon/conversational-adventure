import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

class ApiService {
        constructor() {
                this.client = axios.create({
                        baseURL: BASE_URL,
                        timeout: 10000,
                        headers: {
                                'Content-Type': 'application/json',
                        },
                })

                // Interceptor para requests
                this.client.interceptors.request.use(
                        (config) => {
                                console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`)
                                return config
                        },
                        (error) => {
                                console.error('❌ API Request Error:', error)
                                return Promise.reject(error)
                        }
                )

                // Interceptor para responses
                this.client.interceptors.response.use(
                        (response) => {
                                console.log(`✅ API Response: ${response.status} ${response.config.url}`)
                                return response
                        },
                        (error) => {
                                console.error('❌ API Response Error:', error.response?.status, error.message)
                                return Promise.reject(error)
                        }
                )
        }

        // Health Check
        async checkHealth() {
                const response = await this.client.get('/api/health')
                return response.data
        }

        // System Status
        async getSystemStatus() {
                const response = await this.client.get('/api/system/status')
                return response.data
        }

        // Métricas del sistema
        async getMetrics() {
                const response = await this.client.get('/api/demo/metrics')
                return response.data
        }

        // Gestión de Backups
        async getBackups() {
                const response = await this.client.get('/api/demo/backups')
                return response.data
        }

        async createBackup(backupType = 'manual') {
                const response = await this.client.post('/api/backups/create', {
                        backup_type: backupType
                })
                return response.data
        }

        // Eventos del juego
        async getEvents(limit = 100, offset = 0) {
                const response = await this.client.get('/api/events', {
                        params: { limit, offset }
                })
                return response.data
        }

        // Estadísticas y Analytics
        async getAnalytics(timeframe = '24h') {
                try {
                        // Mock data para analytics hasta que implementemos el endpoint
                        return {
                                timeframe,
                                data_points: this.generateMockAnalytics(),
                                summary: {
                                        total_events: 1234,
                                        average_events_per_hour: 51.4,
                                        peak_hour: '14:00',
                                        system_uptime: '99.8%'
                                }
                        }
                } catch (error) {
                        console.warn('Analytics endpoint not available, using mock data')
                        return this.getMockAnalytics(timeframe)
                }
        }

        // Logs del sistema
        async getLogs(level = 'all', limit = 100) {
                try {
                        // Mock data para logs hasta que implementemos el endpoint
                        return this.generateMockLogs(level, limit)
                } catch (error) {
                        console.warn('Logs endpoint not available, using mock data')
                        return this.getMockLogs(level, limit)
                }
        }

        // Mock Data Generators
        generateMockAnalytics() {
                const now = new Date()
                const dataPoints = []

                for (let i = 23; i >= 0; i--) {
                        const hour = new Date(now.getTime() - i * 60 * 60 * 1000)
                        dataPoints.push({
                                timestamp: hour.toISOString(),
                                events: Math.floor(Math.random() * 100) + 20,
                                active_users: Math.floor(Math.random() * 10) + 1,
                                memory_usage: Math.floor(Math.random() * 30) + 40,
                                cpu_usage: Math.floor(Math.random() * 40) + 20
                        })
                }

                return dataPoints
        }

        generateMockLogs(level, limit) {
                const levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
                const messages = [
                        'Sistema iniciado correctamente',
                        'Backup automático completado',
                        'Nueva conexión WebSocket establecida',
                        'Métricas actualizadas',
                        'Usuario autenticado exitosamente',
                        'Limpieza de memoria ejecutada',
                        'Verificación de integridad completada',
                        'Evento de juego procesado'
                ]

                const logs = []
                const now = new Date()

                for (let i = 0; i < limit; i++) {
                        const timestamp = new Date(now.getTime() - i * 30000) // Cada 30 segundos
                        logs.push({
                                timestamp: timestamp.toISOString(),
                                level: levels[Math.floor(Math.random() * levels.length)],
                                logger: 'adventure-game',
                                message: messages[Math.floor(Math.random() * messages.length)],
                                module: 'main.py'
                        })
                }

                return {
                        logs: level === 'all' ? logs : logs.filter(log => log.level === level.toUpperCase()),
                        total_count: logs.length
                }
        }

        getMockAnalytics(timeframe) {
                return {
                        timeframe,
                        data_points: this.generateMockAnalytics(),
                        summary: {
                                total_events: 1234,
                                average_events_per_hour: 51.4,
                                peak_hour: '14:00',
                                system_uptime: '99.8%'
                        }
                }
        }

        getMockLogs(level, limit) {
                return this.generateMockLogs(level, limit)
        }
}

export const apiService = new ApiService()
