import connectDb from "../config/db.js";

export const syncUsers = async (req, res) => {
  let database;
  try {
    // Connect to the database
    database = await connectDb();

    // Extract user details from Auth0 token
    const { sub: auth0_id, email, name, nickname, picture } = req.auth || {};

    if (!auth0_id) {
      return res.status(400).json({ message: "Missing Auth0 user ID" });
    }

    // Check if user already exists
    const [rows] = await database.execute(
      "SELECT * FROM users WHERE auth0_id = ?",
      [auth0_id]
    );

    if (rows.length === 0) {
      // Create new user safely with null fallbacks
      await database.execute(
        "INSERT INTO users (auth0_id, email, name, picture) VALUES (?, ?, ?, ?)",
        [
          auth0_id,
          email || null,
          name || nickname || null,
          picture || null,
        ]
      );

      console.log(`✅ New user added: ${auth0_id}`);
    } else {
      console.log(`ℹ️ User already exists: ${auth0_id}`);
    }

    res.status(200).json({ message: "User synced successfully" });
  } catch (error) {
    console.error("❌ Error syncing users:", error);
    res.status(500).json({ message: "Internal server error" });
  } finally {
    if (database) await database.end(); // close the connection properly
  }
};
