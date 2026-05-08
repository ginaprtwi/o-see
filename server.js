// =====================================
// server.js (GROQ VERSION)
// =====================================

// LOAD ENV
require('dotenv').config();

// PACKAGES
const express = require('express');
const cors = require('cors');
const OpenAI = require('openai');

// APP
const app = express();

app.use(cors());
app.use(express.json());

// =====================================
// CEK API KEY
// =====================================

console.log('GROQ API:', process.env.GROQ_API_KEY);

// =====================================
// GROQ CLIENT
// =====================================

const client = new OpenAI({
  apiKey: process.env.GROQ_API_KEY,
  baseURL: 'https://api.groq.com/openai/v1'
});

// =====================================
// CHAT ENDPOINT
// =====================================

app.post('/chat', async (req, res) => {
  try {

    const { message, mode } = req.body;

    let systemPrompt = '';

    // =================================
    // MODE ASSISTANT
    // =================================

    if (mode === 'assistant') {

      systemPrompt = `
Kamu adalah O-See.

Kepribadian:
- ngobrol kayak manusia biasa
- santai
- natural
- friendly
- ekspresif
- hangat
- jangan terlalu formal
- jangan terlalu kaku
- jangan terdengar seperti customer service
- kadang boleh bercanda ringan
- gunakan bahasa yang enak dibaca

Gaya bicara:
- pendek sampai sedang
- jelas
- tidak monoton
- sesekali boleh pakai kata seperti:
  "iyaa"
  "nah"
  "wkwk"
  "anjir"
  "btw"
  kalau cocok dengan konteks

Aturan:
- jangan terlalu banyak bullet point
- jangan terlalu panjang kalau tidak perlu
- kalau user curhat, respon dengan empati dan natural
- kalau user bingung, jelaskan simpel
- jangan mengulang pertanyaan user
- jawab seperti teman pintar yang asik diajak ngobrol

Identitas:
Nama kamu O-See.
Kamu adalah AI companion modern yang smart tapi santai.
`;

    } else {

      systemPrompt = `
Kamu adalah AI assistant yang santai, friendly, dan natural.
`;
    }

    // =================================
    // REQUEST KE GROQ
    // =================================

    const completion = await client.chat.completions.create({

      model: 'llama-3.1-8b-instant',

      messages: [
        {
          role: 'system',
          content: systemPrompt
        },
        {
          role: 'user',
          content: message
        }
      ],

      temperature: 1,
      top_p: 0.95,
      max_tokens: 1000

    });

    // =================================
    // AMBIL HASIL AI
    // =================================

    const reply = completion.choices[0].message.content;

    // =================================
    // RESPONSE
    // =================================

    res.json({
      reply
    });

  } catch (err) {

    console.error('ERROR:', err);

    res.status(500).json({
      error: err.message
    });

  }
});

// =====================================
// ROOT
// =====================================

app.get('/', (req, res) => {
  res.send('O-See server jalan 😘 (Groq Version)');
});

// =====================================
// START SERVER
// =====================================

const PORT = 3000;

app.listen(PORT, () => {
  console.log(`Server jalan di http://localhost:${PORT}`);
});