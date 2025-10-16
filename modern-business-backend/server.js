import connectDb from "./config/db.js";
import express from "express";
import dotenv from "dotenv";
import authRoutes from './routes/authRoutes.js';
import userRoutes from './routes/userRoures.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// connect to the database
connectDb();

// Middleware to parse JSON requests
app.use(express.json());


// routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);



app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});