// =====================================
// server.js
// =====================================

// install dulu:
// npm install express cors openai

const express = require('express');
const cors = require('cors');
const OpenAI = require('openai');

const app = express();

app.use(cors());
app.use(express.json());

// =====================================
// OPENROUTER
// =====================================

const client = new OpenAI({

  apiKey: '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',

  baseURL: 'https://openrouter.ai/api/v1'

});

// =====================================
// CHAT ENDPOINT
// =====================================

app.post('/chat', async (req, res) => {

  try {

    const {
      message,
      mode
    } = req.body;

    let systemPrompt = '';

    // =================================
    // MODE ASSISTANT
    // =================================

    if (mode === 'assistant') {

      systemPrompt = `

Kamu adalah O-See AI Assistant.

Tugas kamu:
- bantu user belajar
- bantu brainstorming
- bantu produktivitas
- bantu jawab pertanyaan random
- jadi teman ngobrol santai

Gaya ngobrol:
- natural
- friendly
- singkat
- jangan terlalu formal
- jawab jelas
- jangan terlalu kaku

`;

    }

    // =================================
    // DEFAULT
    // =================================

    else {

      systemPrompt =
        'Kamu adalah AI assistant yang friendly.';

    }

    // =================================
    // AI REQUEST
    // =================================

    const completion =
      await client.chat.completions.create({

        model:
          'google/gemma-2-9b-it:free',

        messages: [

          {
            role: 'system',
            content: systemPrompt
          },

          {
            role: 'user',
            content: message
          }

        ]

      });

    const reply =
      completion
      .choices[0]
      .message
      .content;

    res.json({

      reply

    });

  }

  catch(err) {

    console.error(err);

    res.status(500).json({

      error: err.message

    });

  }

});

// =====================================
// ROOT
// =====================================

app.get('/', (req, res) => {

  res.send('O-See server jalan 😘');

});

// =====================================
// START SERVER
// =====================================

app.listen(3000, () => {

  console.log(
    'Server jalan di http://localhost:3000'
  );

});