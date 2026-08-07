const express = require('express');
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('../swagger.json');
require('dotenv').config();

const app = express();
app.use(express.json());

// Routes Imports
const authRoutes = require('./routes/auth');
const publicRoutes = require('./routes/public');
const protectedRoutes = require('./routes/protected');

// Route Mounting
app.use('/auth', authRoutes);
app.use('/public', publicRoutes);
app.use('/protected', protectedRoutes);

// Swagger Documentation Route
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running and connected to Supabase on port ${PORT}`);
  console.log(`Swagger UI available at http://localhost:${PORT}/docs`);
});