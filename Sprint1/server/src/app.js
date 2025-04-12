// src/app.js
import express from 'express';
import cors from 'cors';
import authRoutes from './routes/auth.js';
import prRoutes from './routes/pr.js';
import dashboardRoutes from './routes/dashboard.js';

const app = express();
app.use(express.json());
app.use(cors({ origin: process.env.FRONTEND_URL || 'http://localhost:3000', credentials: true }));
app.use('/api/auth', authRoutes);
app.use('/api/pr', prRoutes);
app.use('/api/dashboard', dashboardRoutes);
app.get('/', (_, res) => res.send('CodeQuest API running'));

app.get('/api/test', (req, res) => {
    res.json({ message: 'Test route working!' });
  });

app.post('/api/test-post', (req, res) => {
    const { name } = req.body;
    res.json({ message: `Hello, ${name}` });
});
  
export default app;
