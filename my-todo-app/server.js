const express = require('express');
const Database = require('better-sqlite3');

const app = express();
app.use(express.json());

// Stage 0: Connect to SQLite DB & create table
const db = new Database('tasks.db');
db.pragma('journal_mode = WAL');

db.exec(`
  CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER DEFAULT 0
  );
`);

// Seed default data if empty
const count = db.prepare('SELECT COUNT(*) AS count FROM tasks').get();
if (count.count === 0) {
  const insert = db.prepare('INSERT INTO tasks (title, done) VALUES (?, ?)');
  insert.run('Buy groceries', 0);
  insert.run('Walk the dog', 1);
  insert.run('Complete Week 2 assignment', 0);
}

// Helper: Convert SQLite 0/1 to Boolean
const formatTask = (row) => ({
  id: row.id,
  title: row.title,
  done: Boolean(row.done),
});

// Stage 1: Read Endpoints
app.get('/tasks', (req, res) => {
  const { search, done } = req.query;
  let query = 'SELECT * FROM tasks';
  const params = [];
  const conditions = [];

  if (search) {
    conditions.push('title LIKE ?');
    params.push(`%${search}%`);
  }
  if (done !== undefined) {
    conditions.push('done = ?');
    params.push(done === 'true' ? 1 : 0);
  }

  if (conditions.length > 0) {
    query += ' WHERE ' + conditions.join(' AND ');
  }

  const rows = db.prepare(query).all(...params);
  res.json(rows.map(formatTask));
});

app.get('/tasks/:id', (req, res) => {
  const task = db.prepare('SELECT * FROM tasks WHERE id = ?').get(req.params.id);
  if (!task) {
    return res.status(404).json({ error: 'Task not found' });
  }
  res.json(formatTask(task));
});

// Stage 2: Create Endpoint
app.post('/tasks', (req, res) => {
  const { title, done = false } = req.body;

  if (!title || typeof title !== 'string' || title.trim() === '') {
    return res.status(400).json({ error: 'Title is required' });
  }

  const stmt = db.prepare('INSERT INTO tasks (title, done) VALUES (?, ?)');
  const result = stmt.run(title.trim(), done ? 1 : 0);

  const newTask = db.prepare('SELECT * FROM tasks WHERE id = ?').get(result.lastInsertRowid);
  res.status(201).json(formatTask(newTask));
});

// Stage 3: Update & Delete Endpoints
app.put('/tasks/:id', (req, res) => {
  const { title, done } = req.body;
  const existing = db.prepare('SELECT * FROM tasks WHERE id = ?').get(req.params.id);

  if (!existing) {
    return res.status(404).json({ error: 'Task not found' });
  }

  const updatedTitle = title !== undefined ? title.trim() : existing.title;
  const updatedDone = done !== undefined ? (done ? 1 : 0) : existing.done;

  db.prepare('UPDATE tasks SET title = ?, done = ? WHERE id = ?')
    .run(updatedTitle, updatedDone, req.params.id);

  const updated = db.prepare('SELECT * FROM tasks WHERE id = ?').get(req.params.id);
  res.json(formatTask(updated));
});

app.delete('/tasks/:id', (req, res) => {
  const result = db.prepare('DELETE FROM tasks WHERE id = ?').run(req.params.id);
  if (result.changes === 0) {
    return res.status(404).json({ error: 'Task not found' });
  }
  res.status(204).send();
});

// Optional Extra: Stats
app.get('/stats', (req, res) => {
  const total = db.prepare('SELECT COUNT(*) AS count FROM tasks').get().count;
  const completed = db.prepare('SELECT COUNT(*) AS count FROM tasks WHERE done = 1').get().count;
  res.json({ total, completed, pending: total - completed });
});

app.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
});