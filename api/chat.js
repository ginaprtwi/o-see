const OpenAI = require('openai');

const client = new OpenAI({
  apiKey: process.env.GROQ_API_KEY,
  baseURL: 'https://api.groq.com/openai/v1'
});

module.exports = async (req, res) => {

  // =========================
  // CORS
  // =========================

  res.setHeader(
    'Access-Control-Allow-Origin',
    '*'
  );

  res.setHeader(
    'Access-Control-Allow-Methods',
    'POST'
  );

  res.setHeader(
    'Access-Control-Allow-Headers',
    'Content-Type'
  );

  // =========================
  // METHOD CHECK
  // =========================

  if(req.method !== 'POST'){

    return res.status(405).json({
      error:'Method not allowed'
    });

  }

  try{

    const { message, mode } = req.body;

    let systemPrompt = '';

    // =========================
    // ASSISTANT MODE
    // =========================

    if(mode === 'assistant'){

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

    }

    else{

      systemPrompt = `
Kamu adalah AI assistant yang santai,
friendly,
dan natural.
`;

    }

    // =========================
    // REQUEST KE GROQ
    // =========================

    const completion =
      await client.chat.completions.create({

        model:'llama-3.1-8b-instant',

        messages:[
          {
            role:'system',
            content:systemPrompt
          },
          {
            role:'user',
            content:message
          }
        ],

        temperature:1,
        top_p:0.95,
        max_tokens:1000

      });

    // =========================
    // RESPONSE
    // =========================

    const reply =
      completion
      .choices[0]
      .message
      .content;

    res.status(200).json({
      reply
    });

  }

  catch(err){

    console.error(err);

    res.status(500).json({
      error:err.message
    });

  }

};