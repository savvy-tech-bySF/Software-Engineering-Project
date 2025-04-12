// src/models/User.js
import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
  email:    { type: String, required: true, unique: true },
  password: { type: String, required: true },           // hashed
  role:     { type: String, enum: ['coder','reviewer','admin'], default: 'coder' },
  points:   { type: Number, default: 0 },
  badges:   [{ type: String }],
  recentReviews: [{ type: mongoose.Schema.Types.ObjectId, ref: 'PR' }],
}, { timestamps: true });

export default mongoose.model('User', userSchema);
