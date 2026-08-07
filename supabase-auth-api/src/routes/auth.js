const express = require('express');
const router = express.Router();
const supabase = require('../config/supabase');

// POST /auth/signup
router.post('/signup', async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }

  const { data, error } = await supabase.auth.signUp({
    email,
    password,
  });

  if (error) {
    return res.status(400).json({ error: error.message });
  }

  return res.status(201).json(data);
});

// POST /auth/login
router.post('/login', async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password are required' });
  }

  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    return res.status(401).json({ error: 'Invalid login credentials' });
  }

  return res.status(200).json({
    access_token: data.session.access_token,
    refresh_token: data.session.refresh_token,
    user: data.user
  });
});

module.exports = router;

const verifyToken = require('../middleware/auth');

// POST /auth/logout
router.post('/logout', verifyToken, async (req, res) => {
  const { error } = await supabase.auth.admin.signOut(req.token); // or local client signout

  if (error) {
    return res.status(400).json({ error: error.message });
  }

  return res.status(204).send();
});