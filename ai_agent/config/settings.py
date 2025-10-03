"""
Configuration settings for the AI Agent application.
"""

# Application settings
APP_TITLE = "AI エージェント - 電話営業ボット"
APP_VERSION = "1.0.0"
WINDOW_SIZE = "800x600"

# Speech settings
DEFAULT_VOICE_RATE = 150
DEFAULT_VOLUME = 0.8
VOICE_LANGUAGE = 'ja-JP'
SPEECH_TIMEOUT = 5
PHRASE_TIME_LIMIT = 10
AMBIENT_NOISE_DURATION = 0.5

# UI Colors and Styling
BG_COLOR = '#f0f0f0'
TITLE_FONT = ('Arial', 16, 'bold')
STATUS_FONT = ('Arial', 10, 'italic')
INPUT_FONT = ('Arial', 10)

# Conversation settings
MAX_CONVERSATION_HISTORY = 1000
RESPONSE_DELAY = 0.5

# Predefined questions for the rice sales conversation
PREDEFINED_QUESTIONS = [
    "こんにちは。私、X商事の高木と申します。突然のお電話失礼いたします。弊社では、主に弁当店様向けにお米の販売を行っておりまして、今日はその中でもおすすめの商品をご紹介させていただければと思い、ご連絡いたしました。",
    "現在ご好評いただいているのが、「近江ブレンド米・小粒タイプ」という商品で、1kgあたり588円（税別・送料込み）でご提供しております。",
    "このお米は、粒が通常より一回り小さいのが特徴で、弁当箱に詰めやすく、見た目のボリューム感が出しやすいと好評です。",
    "もしご興味があれば、無料サンプルをお届けさせていただいておりますので、よろしければ、お店のお名前・ご住所・ご担当者様のお名前をお教えいただけますでしょうか？"
]

# Response templates based on keywords
RESPONSE_TEMPLATES = {
    "interest": [
        "ありがとうございます。では、無料サンプルをお送りさせていただきますね。お店の詳細をお聞かせください。",
        "ご興味をお持ちいただき、ありがとうございます。詳しい資料もご用意しております。"
    ],
    "busy": [
        "お忙しい中、お時間をいただきありがとうございます。短時間でご説明させていただきます。",
        "お忙しいところ恐縮ですが、2分ほどお時間をいただけますでしょうか。"
    ],
    "price": [
        "1kgあたり588円（税別・送料込み）でご提供しております。送料も含まれておりますので、お得な価格設定となっております。",
        "価格は1kgあたり588円で、送料込みの価格となっております。"
    ],
    "quality": [
        "近江ブレンド米は、粒が小さくて弁当に詰めやすく、見た目も美しく仕上がります。味もおいしく、お客様にも好評です。",
        "このお米は特に弁当店様から好評をいただいており、見た目の美しさと味の良さが特徴です。"
    ],
    "default": [
        "ありがとうございます。他にご質問やご不明な点がございましたら、お気軽にお聞かせください。",
        "承知いたしました。何かご不明な点がございましたら、お気軽にお尋ねください。"
    ]
}

# Keywords for response matching
KEYWORD_MAPPINGS = {
    "interest": ["興味", "関心", "詳しく", "サンプル", "資料", "検討"],
    "busy": ["忙しい", "時間", "用事", "急いで", "急ぎ"],
    "price": ["値段", "価格", "いくら", "安い", "高い", "コスト"],
    "quality": ["米", "ご飯", "品質", "味", "おいしい", "粒"]
}
