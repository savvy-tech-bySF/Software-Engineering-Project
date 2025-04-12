// src/controllers/authController.js
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';
import User from '../models/User.js';
dotenv.config();

const SALT_ROUNDS = 10;

export async function signup(req, res) {
  const { email, password, role } = req.body;
  if (!email || !password)
    return res.status(400).json({ message: 'Email & password required' });

  const hash = await bcrypt.hash(password, SALT_ROUNDS);
  try {
    const user = await User.create({ email, password: hash, role });
    const token = jwt.sign({ id: user._id, email, role: user.role }, process.env.JWT_SECRET, { expiresIn: '7d' });
    res.json({ token });
  } catch (err) {
    res.status(400).json({ message: 'User exists or invalid data' });
  }
}

export async function login(req, res) {
  const { email, password } = req.body;
  const user = await User.findOne({ email });
  if (!user) return res.status(401).json({ message: 'Invalid creds' });

  const ok = await bcrypt.compare(password, user.password);
  if (!ok) return res.status(401).json({ message: 'Invalid creds' });

  const token = jwt.sign({ id: user._id, email, role: user.role }, process.env.JWT_SECRET, { expiresIn: '7d' });
  res.json({ token });
}
