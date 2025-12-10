# ===== ここから追記 =====

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# CORS 設定（GitHub Pages から叩けるように）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI クライアント
client = OpenAI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

SYSTEM_PROMPT = """
あなたは、日本・福島を拠点に人材育成と女性起業家支援を行う
「重巣敦子さん（リファインアカデミー株式会社代表取締役）」の
公開情報および起業家支援に関するコラム内容をもとに作られた
“仮想エージェント”です。

実在の重巣敦子さん本人ではありませんが、
ご本人の理念・専門性・伴走支援スタイルを反映し、
女性の「わたしらしい働き方・起業」を優しく、具体的に整理する
相談役としてふるまってください。
"""

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    user_message = req.message.strip()

    if not user_message:
        return ChatResponse(reply="まずは、今のご状況や気になっていることを教えてくださいね。")

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.6,
    )

    reply = completion.choices[0].message.content.strip()

    return ChatResponse(reply=reply)


# ローカル起動 or Render の python app.py 用
if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
