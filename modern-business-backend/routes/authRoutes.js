import express from 'express';
import { syncUsers } from '../controllers/authControllers.js';
import checkJwt from '../middleware/checkJwt.js';

const router = express.Router();

router.post('/sync', checkJwt, syncUsers);

export default router;