// src/controllers/dashboardController.js
import User from '../models/User.js';
import PR from '../models/PR.js';

export async function getDashboard(req, res) {
  const user = await User.findById(req.user.id).lean();
  if (!user) return res.status(404).json({ message: 'Not found' });

  // fetch last 5 PRs they submitted
  const recent = await PR.find({ owner: user._id })
    .sort({ createdAt: -1 })
    .limit(5)
    .lean();

  res.json({
    email: user.email,
    role: user.role,
    points: user.points,
    badges: user.badges,
    recentPRs: recent.map(p => ({ repo: p.repo, prId: p.prId, createdAt: p.createdAt })),
  });
}
