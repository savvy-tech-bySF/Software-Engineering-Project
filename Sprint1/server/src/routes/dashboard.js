// src/routes/dashboard.js
import { Router } from 'express';
import { requireAuth } from '../middleware/auth.js';
import { getDashboard } from '../controllers/dashboardcontroller.js';

const router = Router();
router.get('/', requireAuth, getDashboard);
export default router;
