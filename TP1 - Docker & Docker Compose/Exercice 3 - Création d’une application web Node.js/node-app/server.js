const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware de base
app.use(express.json());

// Routes
app.get('/', (req, res) => {
    res.json({
        message: 'Bienvenue sur notre application Node.js containerisée!',
        timestamp: new Date().toISOString()
    });
});

app.get('/api/health', (req, res) => {
    res.status(200).json({
        status: 'OK',
        message: 'L\'application fonctionne correctement',
        uptime: process.uptime(),
        timestamp: new Date().toISOString()
    });
});

app.get('/api/info', (req, res) => {
    res.json({
        nodeVersion: process.version,
        platform: process.platform,
        memoryUsage: process.memoryUsage(),
        environment: process.env.NODE_ENV || 'development'
    });
});

app.get('/api/time', (req, res) => {
    res.json({
        currentTime: new Date().toISOString(),
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        timestamp: Date.now()
    });
});

// Gestion des erreurs 404
app.use('*', (req, res) => {
    res.status(404).json({
        error: 'Route non trouvée',
        availableRoutes: ['/', '/api/health', '/api/info', '/api/time']
    });
});

// Démarrage du serveur
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Serveur démarré sur le port ${PORT}`);
    console.log(`📍 URL: http://localhost:${PORT}`);
});