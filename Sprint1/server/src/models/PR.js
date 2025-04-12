// src/models/PR.js
import mongoose from 'mongoose';

const prSchema = new mongoose.Schema({
  owner:    { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  repo:     { type: String, required: true }, // "owner/repo"
  prId:     { type: Number, required: true },
  data:     { type: Object },                 // raw GitHub/GitLab response
}, { timestamps: true });

export default mongoose.model('PR', prSchema);
