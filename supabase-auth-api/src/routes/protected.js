const express = require('express');
const router = express.Router();
const verifyToken = require('../middleware/auth');

// Apply authentication middleware to all protected routes
router.use(verifyToken);

// GET /protected/profile
router.get('/profile', (req, res) => {
  return res.status(200).json({
    id: req.user.id,
    email: req.user.email,
    created_at: req.user.created_at
  });
});

// GET /protected/dashboard (Optional test endpoint)
router.get('/dashboard', (req, res) => {
  return res.status(200).json({
    message: `Welcome to the protected dashboard, ${req.user.email}!`
  });
});

module.exports = router;