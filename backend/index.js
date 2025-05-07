const express = require('express');
const cors = require('cors');
const { MongoClient } = require('mongodb');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

let mongoClient = null;
let mongoUrl = '';

// Save MongoDB connection URL
app.post('/api/save-mongodb-connection', async (req, res) => {
  const { url } = req.body;
  if (!url) return res.status(400).json({ error: 'Missing MongoDB URL' });
  mongoUrl = url;
  try {
    mongoClient = new MongoClient(url);
    await mongoClient.connect();
    res.json({ message: 'Connected to MongoDB successfully!' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Example: Run a MongoDB query (for demonstration)
app.post('/api/run-mongodb-query', async (req, res) => {
  if (!mongoClient) return res.status(400).json({ error: 'Not connected to MongoDB' });
  const { dbName, collectionName, query } = req.body;
  try {
    const db = mongoClient.db(dbName);
    const collection = db.collection(collectionName);
    const results = await collection.find(query || {}).toArray();
    res.json({ results });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
