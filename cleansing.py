import pandas as pd
import json
import re
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from wordcloud import WordCloud
plt.rcParams['font.family'] = 'Segoe UI Emoji'

# ── COLOR PALETTE ─────────────────────────────────────────────
PINK = '#F7A8D7'
PURPLE = '#B56BFF'
LILAC = '#D8B4F8'
DARK_PURPLE = '#7B2CBF'
SOFT_PINK = '#FFF0FA'

# ── 1. LOAD DATA ─────────────────────────────────────────────
with open('result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.json_normalize(data['messages'])

# ── 2. CLEANING ──────────────────────────────────────────────

# Filter pesan osy aja
df = df[df['from'].str.contains('osy', case=False, na=False)].copy()

# Filter hanya type "message"
df = df[df['type'] == 'message'].copy()

# Ekstrak teks plain
def extract_plain_text(text):
    if isinstance(text, str):
        return text
    elif isinstance(text, list):
        return ' '.join(
            item['text']
            for item in text
            if isinstance(item, dict) and item.get('type') == 'plain'
        )
    return ''

df['text_clean'] = df['text'].apply(extract_plain_text)

# Drop kosong
df = df[df['text_clean'].str.strip() != ''].copy()

# Parse datetime
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour

print(f"Total pesan osy: {len(df)}")
print(df[['date', 'text_clean']].head())

# ── 3. EKSTRAK KATA & EMOJI ─────────────────────────────────

STOPWORDS = {
    'ak', 'km', 'iyh', 'jg', 'mw', 'bnr', 'yh', 'tp',
    'bleh', 'nnti', 'gpp', 'jdi', 'jd', 'gt', 'bgt',
    'kl', 'klo', 'blm', 'anu', 'iya', 'ituh', 'bs',
    'si', 'krn', 'tdk', 'yah', 'sm', 'ad', 'lg',
    'sdh', 'kok', 'apa', 'dgn', 'sandy',
    'yang', 'di', 'dan', 'ini', 'itu', 'ke',
    'dengan', 'untuk', 'ada', 'ya', 'aku',
    'kamu', 'dia', 'kak', 'tuh', 'sih', 'deh',
    'dong', 'lah', 'nih', 'tapi', 'juga',
    'udah', 'udh', 'gak', 'ga', 'gk', 'nggak',
    'ngga', 'nya', 'aja', 'kayak', 'kyk',
    'mau', 'bisa', 'yg', 'gue', 'gw', 'lu',
    'lo', 'jadi', 'kalo', 'kalau', 'sama',
    'buat', 'dari', 'tau', 'a', 'e', 'i',
    'o', 'u', 'lagi', 'terus', 'habis',
    'banget', 'saja', 'atau', 'lebih',
    'punya', 'lain', 'pake', 'pas',
    'hal', 'ok', 'oke', 'haha',
    'hehe', 'wkwk', 'wkwkwk'
}

EMOJI_PATTERN = re.compile(
    "[\U00010000-\U0010ffff"
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\u2600-\u26FF\u2700-\u27BF]+",
    flags=re.UNICODE
)

all_text = ' '.join(df['text_clean'].tolist()).lower()

# Ekstrak emoji
emojis = EMOJI_PATTERN.findall(all_text)
emoji_counter = Counter(''.join(emojis))
top_emojis = emoji_counter.most_common(15)

# Hapus emoji
text_no_emoji = EMOJI_PATTERN.sub('', all_text)

# Ambil kata
words = re.findall(r'\b[a-zA-Z]{2,}\b', text_no_emoji)

# Filter stopwords
words_filtered = [w for w in words if w not in STOPWORDS]

# Hitung frekuensi
word_counter = Counter(words_filtered)
top_words = word_counter.most_common(20)

# ── 4. GRAFIK ───────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Background utama
fig.patch.set_facecolor('#FFE6F7')

# Styling semua subplot
for ax in axes.flat:
    ax.set_facecolor(SOFT_PINK)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.title.set_color(DARK_PURPLE)

    ax.tick_params(colors=DARK_PURPLE)

    ax.xaxis.label.set_color(DARK_PURPLE)
    ax.yaxis.label.set_color(DARK_PURPLE)

fig.suptitle(
    "Chat Analysis — osy",
    fontsize=20,
    fontweight='bold',
    color=DARK_PURPLE
)

# ── Grafik 1: Kata Pilihan ─────────────────────────────────

kata_custom = ['jomok', 'imut', 'rusdi']

frekuensi_custom = {
    kata: all_text.count(kata)
    for kata in kata_custom
}

custom_labels = list(frekuensi_custom.keys())
custom_vals = list(frekuensi_custom.values())

ax1 = axes[0, 0]

bars = ax1.barh(
    custom_labels[::-1],
    custom_vals[::-1],
    color=PURPLE
)

ax1.set_title('Frekuensi Kata Pilihan', fontweight='bold')
ax1.set_xlabel('Frekuensi')

ax1.bar_label(
    bars,
    padding=3,
    fontsize=8,
    color=DARK_PURPLE
)

ax1.xaxis.set_major_locator(
    ticker.MaxNLocator(integer=True)
)

# ── Grafik 2: Emoji ─────────────────────────────────────────

ax2 = axes[0, 1]

if top_emojis:
    emoji_labels, emoji_vals = zip(*top_emojis)

    ax2.bar(
        emoji_labels,
        emoji_vals,
        color=PINK
    )

    ax2.set_title(
        'Top 15 Emoji yang Sering Dipakai',
        fontweight='bold'
    )

    ax2.set_xlabel('Emoji')
    ax2.set_ylabel('Frekuensi')

    for i, v in enumerate(emoji_vals):
        ax2.text(
            i,
            v + 0.3,
            str(v),
            ha='center',
            fontsize=8,
            color=DARK_PURPLE
        )

else:
    ax2.text(
        0.5,
        0.5,
        'Tidak ada emoji',
        ha='center',
        va='center'
    )

# ── Grafik 3: Jam Aktif ────────────────────────────────────

ax3 = axes[1, 0]

hour_counts = df['hour'].value_counts().sort_index()

ax3.bar(
    hour_counts.index,
    hour_counts.values,
    color=LILAC,
    width=0.8
)

ax3.set_title('Jam Aktif Chat', fontweight='bold')

ax3.set_xlabel('Jam (0–23)')
ax3.set_ylabel('Jumlah Pesan')

ax3.set_xticks(range(0, 24))

ax3.set_xticklabels(
    [f'{h:02d}:00' for h in range(24)],
    rotation=45,
    ha='right',
    fontsize=7
)

# ── Grafik 4: Word Cloud ───────────────────────────────────

ax4 = axes[1, 1]

wc = WordCloud(
    width=600,
    height=400,
    background_color='white',
    colormap='RdPu',
    max_words=100
).generate_from_frequencies(word_counter)

ax4.imshow(wc, interpolation='bilinear')

ax4.axis('off')

ax4.set_title(
    'Word Cloud',
    fontweight='bold'
)

# ── SAVE ───────────────────────────────────────────────────

plt.tight_layout()

plt.savefig(
    'chat_analysis_osy.png',
    dpi=150,
    bbox_inches='tight'
)

plt.show()

print("Grafik disimpan: chat_analysis_osy.png")