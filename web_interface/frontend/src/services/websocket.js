import { io } from 'socket.io-client'

class WebSocketService {
        constructor() {
                this.socket = null
                this.listeners = new Map()
                this.connected = false
        }

        connect() {
                const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8001'

                console.log('🔌 Conectando WebSocket:', WS_URL)

                this.socket = io(WS_URL, {
                        transports: ['websocket'],
                        autoConnect: true,
                        reconnection: true,
                        reconnectionDelay: 1000,
                        reconnectionAttempts: 5,
                })

                this.socket.on('connect', () => {
                        console.log('✅ WebSocket conectado')
                        this.connected = true
                        this.emit('connection', { status: 'connected' })
                })

                this.socket.on('disconnect', () => {
                        console.log('🔌 WebSocket desconectado')
                        this.connected = false
                        this.emit('connection', { status: 'disconnected' })
                })

                this.socket.on('connect_error', (error) => {
                        console.error('❌ Error de conexión WebSocket:', error)
                        this.connected = false
                        this.emit('connection', { status: 'error', error: error.message })
                })

                // Escuchar mensajes del servidor
                this.socket.on('message', (data) => {
                        console.log('📡 Mensaje WebSocket recibido:', data)
                        try {
                                const message = typeof data === 'string' ? JSON.parse(data) : data
                                this.emit('message', message)

                                // Emitir eventos específicos por tipo
                                if (message.type) {
                                        this.emit(message.type, message)
                                }
                        } catch (error) {
                                console.error('Error parseando mensaje WebSocket:', error)
                        }
                })

                // Ping/Pong para mantener conexión viva
                this.socket.on('pong', () => {
                        console.log('🏓 Pong recibido')
                })

                // Iniciar ping periódico
                this.startPing()
        }

        disconnect() {
                if (this.socket) {
                        console.log('🔌 Desconectando WebSocket')
                        this.socket.disconnect()
                        this.socket = null
                        this.connected = false
                }
        }

        send(message) {
                if (this.socket && this.connected) {
                        console.log('📤 Enviando mensaje WebSocket:', message)
                        this.socket.emit('message', JSON.stringify(message))
                } else {
                        console.warn('⚠️ WebSocket no conectado, no se puede enviar mensaje')
                }
        }

        startPing() {
                setInterval(() => {
                        if (this.connected) {
                                this.send({ type: 'ping', timestamp: new Date().toISOString() })
                        }
                }, 30000) // Ping cada 30 segundos
        }

        // Sistema de eventos personalizado
        on(event, callback) {
                if (!this.listeners.has(event)) {
                        this.listeners.set(event, [])
                }
                this.listeners.get(event).push(callback)
        }

        off(event, callback) {
                if (this.listeners.has(event)) {
                        const callbacks = this.listeners.get(event)
                        const index = callbacks.indexOf(callback)
                        if (index > -1) {
                                callbacks.splice(index, 1)
                        }
                }
        }

        emit(event, data) {
                if (this.listeners.has(event)) {
                        this.listeners.get(event).forEach(callback => {
                                try {
                                        callback(data)
                                } catch (error) {
                                        console.error(`Error en listener de evento '${event}':`, error)
                                }
                        })
                }
        }

        // Métodos de conveniencia
        onMessage(callback) {
                this.on('message', callback)
        }

        onMetricsUpdate(callback) {
                this.on('metrics_update', callback)
        }

        onBackupCreated(callback) {
                this.on('backup_created', callback)
        }

        onSystemStatus(callback) {
                this.on('system_status', callback)
        }

        onConnection(callback) {
                this.on('connection', callback)
        }

        isConnected() {
                return this.connected
        }
}

export const websocketService = new WebSocketService()
