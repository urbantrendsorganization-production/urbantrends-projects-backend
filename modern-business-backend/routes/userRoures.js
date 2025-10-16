import express from 'express';
import { getProfile } from '../controllers/usersControllers.js';
import checkJwt from '../middleware/checkJwt.js';

const router = express.Router();

router.get('/profile', checkJwt, getProfile);

export default router;
