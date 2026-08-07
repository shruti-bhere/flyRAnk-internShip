const { createClient } = require('@supabase/supabase-js');
const fetch = require('node-fetch');
const WebSocket = require('ws');
require('dotenv').config();

global.WebSocket = WebSocket;

const supabaseUrl = process.env.SUPABASE_URL ? process.env.SUPABASE_URL.trim() : '';
const supabaseKey = process.env.SUPABASE_KEY ? process.env.SUPABASE_KEY.trim() : '';

if (!supabaseUrl || !supabaseKey) {
  throw new Error('SUPABASE_URL and SUPABASE_KEY are required in .env file');
}

const supabase = createClient(supabaseUrl, supabaseKey, {
  auth: {
    persistSession: false,
    autoRefreshToken: false,
    detectSessionInUrl: false
  },
  global: {
    fetch: fetch
  }
});

module.exports = supabase;