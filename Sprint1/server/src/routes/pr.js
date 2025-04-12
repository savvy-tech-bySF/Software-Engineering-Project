// src/routes/pr.js
import { Router } from 'express';
import { requireAuth } from '../middleware/auth.js';
import { submitPR } from '../controllers/prcontroller.js';

const router = Router();
router.post('/submit', requireAuth, submitPR);
export default router;
