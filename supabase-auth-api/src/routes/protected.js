const express = require('express');
const router = express.Router();
const supabase = require('../config/supabase');

// GET /protected/profile
router.get('/profile', async (req, res) => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Access token required' });
  }

  const token = authHeader.split(' ')[1];

  const { data: { user }, error } = await supabase.auth.getUser(token);

  if (error || !user) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }

  return res.status(200).json({
    id: user.id,
    email: user.email,
    created_at: user.created_at
  });
});

module.exports = router;

const express = require('express');
const router = express.Router();
const verifyToken = require('../middleware/auth');

router.use(verifyToken); // Protections to all routes below

router.get('/profile', (req, res) => {
  res.status(200).json({
    id: req.user.id,
    email: req.user.email,
    created_at: req.user.created_at
  });
});

router.get('/dashboard', (req, res) => {
  res.status(200).json({ message: `Welcome to dashboard, ${req.user.email}` });
});

module.exports = router;