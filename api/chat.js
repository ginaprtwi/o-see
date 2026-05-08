import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.GROQ_API_KEY,
  baseURL: 'https://api.groq.com/openai/v1'
});

export default async function handler(req, res){

  // =========================
  // CORS
  // =========================

  res.setHeader(
    'Access-Control-Allow-Origin',
    '*'
  );

  res.setHeader(
    'Access-Control-Allow-Methods',
    'POST, OPTIONS'
  );

  res.setHeader(
    'Access-Control-Allow-Headers',
    'Content-Type'
  );

  if(req.method === 'OPTIONS'){
    return res.status(200).end();
  }

  // =========================
  // METHOD CHECK
  // =========================

  if(req.method !== 'POST'){

    return res.status(405).json({
      error:'Method not allowed'
    });

  }

  try{

    // =========================
    // BODY FIX VERCEL
    // =========================

    const body =
      typeof req.body === 'string'
        ? JSON.parse(req.body)
        : req.body;

    const {
      message,
      mode
    } = body;

    // =========================
    // PROMPT
    // =========================

    let systemPrompt = `
Kamu adalah O-See.

Ngobrol santai,
natural,
friendly,
hangat,
dan jangan terlalu formal.

Jawab kayak teman pintar
yang asik diajak ngobrol.
`;

    // =========================
    // AI REQUEST
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

    return res.status(200).json({

      reply:
        completion
        .choices[0]
        .message
        .content

    });

  }

  catch(err){

    console.error(
      'VERCEL ERROR:',
      err
    );

    return res.status(500).json({

      error:
        err.message ||
        'Unknown error'

    });

  }

}