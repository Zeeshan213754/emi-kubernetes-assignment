const express = require('express');
const os = require('os');
const { MongoClient } = require('mongodb');

const app = express();
app.use(express.json());
app.use(express.static('public'));

const client = new MongoClient(process.env.MONGO_URL, { serverSelectionTimeoutMS: 3000 });
const col = () => client.db().collection('calculations');

const podIP = Object.values(os.networkInterfaces()).flat()
  .find(i => i.family === 'IPv4' && !i.internal)?.address;

app.post('/api/emi', async (req, res) => {
  const body = req.body || {};
  const P = Number(body.P);
  const rate = Number(body.rate);
  const n = Number(body.n);

  if (![P, rate, n].every(v => Number.isFinite(v) && v > 0)) {
    return res.status(400).json({ error: 'All inputs must be positive numbers' });
  }

  const r = rate / 12 / 100;
  const emi = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
  const totalPayment = emi * n;
  const totalInterest = totalPayment - P;
  const servedBy = process.env.HOSTNAME;

  try {
    await col().insertOne({ principal: P, rate, months: n, emi, servedBy, createdAt: new Date() });
  } catch (e) {
    return res.status(503).json({ error: 'Database unavailable' });
  }

  res.json({ emi, totalPayment, totalInterest, servedBy, podIP });
});

app.get('/api/history', async (req, res) => {
  try {
    const rows = await col().find().sort({ createdAt: -1 }).limit(10).toArray();
    res.json(rows);
  } catch (e) {
    res.status(503).json({ error: 'Database unavailable' });
  }
});

app.get('/health', async (req, res) => {
  try {
    await client.db().command({ ping: 1 });
    res.sendStatus(200);
  } catch (e) {
    res.sendStatus(503);
  }
});

client.connect().catch(err => console.error('Mongo connect error:', err.message));
app.listen(3000, () => console.log('Listening on port 3000'));
