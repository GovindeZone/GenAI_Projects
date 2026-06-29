require('dotenv').config();
const express = require('express');
const cors = require('cors');

const gmailRoutes = require('./routes/gmail');
const emailRoutes = require('./routes/emails');
const analyzeRoutes = require('./routes/analyze');

const app = express();

app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true,
}));
app.use(express.json());

app.use('/api/gmail', gmailRoutes);
app.use('/api/emails', emailRoutes);
app.use('/api/analyze', analyzeRoutes);

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: err.message || 'Internal server error' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Gmail Issue Dashboard API running on port ${PORT}`);
});
