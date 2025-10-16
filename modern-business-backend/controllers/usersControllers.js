import connectDb from "../config/db.js";

export const getProfile = async (req, res) => {
    try {
        const database = await connectDb();
        const { sub: auth0_id } = req.auth;
        const [rows] = await database.execute('SELECT * FROM users WHERE auth0_id = ?', [auth0_id]);
        if (rows.length === 0) {
            return res.status(404).json({ message: "User not found" });
        }
        res.json(rows[0]);
    } catch (error) {
        console.error("Error fetching profile:", error);
        res.status(500).json({ message: "Internal server error" });
    }
};