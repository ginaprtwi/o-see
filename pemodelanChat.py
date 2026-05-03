# backend.py
import pandas as pd
import json
import random
from groq import Groq

# ── 1. LOAD DATA & BIKIN PASANGAN ─────────────────────────────────────────────
def load_conversation_pairs(json_path: str, n: int = 50):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.json_normalize(data['messages'])
    df = df[df['type'] == 'message'].copy()

    def extract_plain_text(text):
        if isinstance(text, str):
            return text
        elif isinstance(text, list):
            return ' '.join(
                item['text'] for item in text
                if isinstance(item, dict) and item.get('type') == 'plain'
            )
        return ''

    df['text_clean'] = df['text'].apply(extract_plain_text)
    df = df[df['text_clean'].str.strip() != ''].reset_index(drop=True)

    # Bikin pasangan Gina → osy
    pairs = []
    for i in range(len(df) - 1):
        curr = df.iloc[i]
        nxt  = df.iloc[i + 1]
        if 'Gina' in str(curr['from']) and 'osy' in str(nxt['from']).lower():
            pairs.append({
                'gina': curr['text_clean'],
                'osy' : nxt['text_clean']
            })

    # Ambil n pasangan random
    chosen = random.sample(pairs, min(n, len(pairs)))
    return chosen


# ── 2. SYSTEM PROMPT ───────────────────────────────────────────────────────────
def build_system_prompt(pairs: list) -> str:
    examples = '\n'.join(
        f'Gina: {p["gina"]}\nosy: {p["osy"]}' for p in pairs
    )
    return f"""Kamu adalah osy — balas pesan seperti osy berdasarkan contoh percakapan nyata berikut:

{examples}

Aturan:
- Balas sesuai konteks pesan yang masuk
- Tiru gaya bahasa, singkatan, dan ekspresi osy dari contoh
- Jawab singkat & natural kayak chat beneran
- Boleh capslock kalau excited
- Jangan formal
"""


# ── 3. CHATBOT CLASS ───────────────────────────────────────────────────────────
class OsyBot:
    def __init__(self, json_path: str, api_key: str):
        self.client  = Groq(api_key=api_key)
        self.history = []

        pairs              = load_conversation_pairs(json_path, n=50)
        self.system_prompt = build_system_prompt(pairs)

    def chat(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.system_prompt},
                *self.history
            ],
            max_tokens=200,
            temperature=0.7,
        )

        reply = response.choices[0].message.content.strip()
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def reset(self):
        self.history = []


# ── 4. TEST LOKAL ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    API_KEY   = "gsk_xxxx"       # ← Groq API key
    JSON_PATH = "result.json"    # ← file JSON original

    bot = OsyBot(json_path=JSON_PATH, api_key=API_KEY)

    print("Chatbot osy siap! Ketik 'quit' untuk keluar.\n")
    while True:
        user = input("Kamu: ").strip()
        if not user:
            continue
        if user.lower() == "quit":
            break
        reply = bot.chat(user)
        print(f"osy: {reply}\n")