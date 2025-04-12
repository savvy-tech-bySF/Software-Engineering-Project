// src/controllers/prController.js
import axios from 'axios';
import PR from '../models/PR.js';

export async function submitPR(req, res) {
  const { repoUrl, prId } = req.body;
  if (!repoUrl || !prId)
    return res.status(400).json({ message: 'repoUrl & prId required' });

  // parse "owner/repo"
  const path = repoUrl.split('github.com/')[1]?.replace(/\.git$/, '');
  if (!path) return res.status(400).json({ message: 'Invalid GitHub URL' });

  try {
    const { data } = await axios.get(
      `https://api.github.com/repos/${path}/pulls/${prId}`,
      { headers: { Authorization: `token ${process.env.GITHUB_TOKEN}` } }
    );

    const pr = await PR.create({
      owner: req.user.id,
      repo: path,
      prId,
      data,
    });

    res.json({ pr });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Failed to fetch or save PR' });
  }
}
