import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# OpenAIクライアント
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# GitHub Pages から叩くのでCORS開けておく
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて自分のGitHub Pagesドメインだけに絞る
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
ご本人の公に示されている活動・理念・専門性、
特に「女性の起業を伴走支援するIMとして意識したいこと」で示されている
支援ポリシーを反映した形でふるまってください。

（中略：ここに先ほど一緒に作った詳細プロンプトをそのまま貼り付けてOK。
　▼ 1. プロフィール・専門領域〜▼ 8. 最初の挨拶 までを入れる）
"""

@app.get("/")
def root():
    return {"message": "AI Shigesu backend is running."}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    user_message = req.message.strip()
    if not user_message:
        return ChatResponse(reply="まずは、今のご状況や気になっていることを少し教えていただけますか？")

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.6,
    )

    reply_text = completion.choices[0].message.content.strip()
    return ChatResponse(reply=reply_text)


# 🔽 これを追加すれば、python app.py でもサーバが立つ
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "10000"))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
