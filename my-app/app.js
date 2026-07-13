const express = require('express');
const { Pool } = require('pg');

const app = express();
app.use(express.json());

// ==========================================
// 1. STORAGE IMPLEMENTATIONS (Layering)
// ==========================================

// Version A: In-Memory Storage (Juni System - Temporary RAM)
class InMemoryUserRepository {
    constructor() { this.users = []; this.idCounter = 1; }
    async create(user) {
        const newUser = { id: this.idCounter++, ...user };
        this.users.push(newUser);
        return newUser;
    }
    async findAll() { return this.users; }
}

// Version B: Postgres Storage (Navin System - Permanent Database)
class PostgresUserRepository {
    constructor() {
        this.pool = new Pool({ connectionString: process.env.DATABASE_URL });
    }
    async create(user) {
        const result = await this.pool.query(
            'INSERT INTO users(name, email) VALUES($1, $2) RETURNING *',
            [user.name, user.email]
        );
        return result.rows[0];
    }
    async findAll() {
        const result = await this.pool.query('SELECT * FROM users');
        return result.rows;
    }
}

// ==========================================
// THE PAYOFF: SWAPPING THE ENGINE HERE
// ==========================================
// Laglyas hi line uncomment kara ani kharchi comment kara jar test karaycha asel tar:
// const userRepo = new InMemoryUserRepository(); 

const userRepo = new PostgresUserRepository(); // Ekach line cha badal!

// ==========================================
// 2. HTTP ROUTES (He bilkul badalnar nahi!)
// ==========================================

app.post('/users', async (req, res) => {
    try {
        const { name, email } = req.body;
        const newUser = await userRepo.create({ name, email });
        res.status(201).json(newUser);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/users', async (req, res) => {
    try {
        const users = await userRepo.findAll();
        res.json(users);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`App running on port ${PORT}`));