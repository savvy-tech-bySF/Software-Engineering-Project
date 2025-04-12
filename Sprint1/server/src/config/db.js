import mongoose from 'mongoose';
import dotenv from 'dotenv';
dotenv.config();

export function connectDB() {
  const uri = process.env.DB_URI;
  if (!uri) {
    throw new Error('Missing DB_URI in .env');
  }
  return mongoose.connect(uri);
}
