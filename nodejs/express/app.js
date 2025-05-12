const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

// Import routers
const healthRouter = require('./routers/health_check/health_handler');
const voiceRouter = require('./routers/voice/voice_handler');

// Set up logging
const logger = console;

// Initialize Express app
const app = express();

// Initialize middleware
app.use(helmet());
app.use(cors({
  origin: '*',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With', 'unith-voice-x-api']
}));
app.use(express.json());
app.use(morgan('dev'));

// Swagger configuration
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Express Template Connector API',
      version: '0.1.0',
      description: 'API documentation for the Express Template Connector',
    },
    servers: [
      {
        url: 'http://localhost:8080',
        description: 'Development server',
      },
    ],
    components: {
      securitySchemes: {
        apiKey: {
          type: 'apiKey',
          in: 'header',
          name: 'unith-voice-x-api',
        },
      },
    },
  },
  apis: ['./routers/**/*.js'], // Path to the API docs
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// Initialize routers
app.use('/', healthRouter);
app.use('/', voiceRouter);

// Set up Swagger documentation
app.get('/docs', (req, res) => {
  res.redirect('/api-docs');
});

app.get('/redoc', (req, res) => {
  res.redirect('/api-docs');
});

// Start the server
const PORT = process.env.PORT || 8080;
app.listen(PORT, '0.0.0.0', () => {
  logger.info(`Server running on port ${PORT}`);
  logger.info(`API Documentation available at http://localhost:${PORT}/api-docs`);
});

module.exports = app;
