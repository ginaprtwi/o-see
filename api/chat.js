const OpenAI = require('openai');

const client = new OpenAI({
  apiKey: process.env.GROQ_API_KEY,
  baseURL: 'https://api.groq.com/openai/v1'
});

export default async function handler(req, res){

  res.setHeader(
    'Access-Control-Allow-Origin',
    '*'
  );

  if(req.method !== 'POST'){

    return res.status(405).json({
      error:'Method not allowed'
    });

  }

  try{

    const body =
      typeof req.body === 'string'
        ? JSON.parse(req.body)
        : req.body;

    const { message, mode } = body;

    const completion =
      await client.chat.completions.create({

        model:'llama-3.1-8b-instant',

        messages:[
          {
            role:'system',
            content:'Kamu adalah O-See. Ngobrol santai dan natural.'
          },
          {
            role:'user',
            content:message
          }
        ],

        temperature:1,
        max_tokens:1000

      });

    return res.status(200).json({

      reply:
        completion
        .choices[0]
        .message
        .content

    });

  }

  catch(err){

    console.error(err);

    return res.status(500).json({
      error:err.message
    });

  }

}