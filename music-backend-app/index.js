import connectDb from "./config/db.js";
import express from "express";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Connect to the database
connectDb();


// Middleware to parse JSON requests
app.use(express.json());

// welcome route
app.get("/", (req, res) => {
    res.send("Welcome to the Music Backend API");
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});