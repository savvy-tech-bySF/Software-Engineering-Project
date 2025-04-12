// src/server.js
import dotenv from 'dotenv';
dotenv.config();
import app from './app.js';
import { connectDB } from './config/db.js';

const PORT = process.env.PORT || 4000;
connectDB()
  .then(() => {
    console.log('🔗 MongoDB connected');
    app.listen(PORT, () => console.log(`🚀 Listening on http://localhost:${PORT}`));
  })
  .catch(err => {
    console.error('DB error:', err);
    process.exit(1);
  });
