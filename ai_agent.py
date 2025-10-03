import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyttsx3
import speech_recognition as sr
import threading
import queue
import time
import random
from datetime import datetime

class AIAgent:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI エージェント - 電話営業ボット")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize speech components
        self.tts_engine = None
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Conversation state
        self.is_talking = False
        self.conversation_history = []
        self.current_question_index = 0
        self.conversation_log = []
        
        # Audio queue for speech processing
        self.audio_queue = queue.Queue()
        
        # Predefined questions in Japanese
        self.questions = [
            "こんにちは。私、X商事の高木と申します。突然のお電話失礼いたします。弊社では、主に弁当店様向けにお米の販売を行っておりまして、今日はその中でもおすすめの商品をご紹介させていただければと思い、ご連絡いたしました。",
            "現在ご好評いただいているのが、「近江ブレンド米・小粒タイプ」という商品で、1kgあたり588円（税別・送料込み）でご提供しております。",
            "このお米は、粒が通常より一回り小さいのが特徴で、弁当箱に詰めやすく、見た目のボリューム感が出しやすいと好評です。",
            "もしご興味があれば、無料サンプルをお届けさせていただいておりますので、よろしければ、お店のお名前・ご住所・ご担当者様のお名前をお教えいただけますでしょうか？"
        ]
        
        # User responses for context
        self.user_responses = []
        
        self.setup_ui()
        self.initialize_tts()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="AI エージェント - 電話営業ボット", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Start button
        self.start_button = ttk.Button(control_frame, text="開始", 
                                      command=self.start_conversation,
                                      style='Start.TButton')
        self.start_button.grid(row=0, column=0, padx=(0, 5))
        
        # Stop button
        self.stop_button = ttk.Button(control_frame, text="停止", 
                                     command=self.stop_conversation,
                                     state='disabled')
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Send text button
        self.send_text_button = ttk.Button(control_frame, text="テキスト送信", 
                                          command=self.send_text_message)
        self.send_text_button.grid(row=0, column=2, padx=5)
        
        # Clear log button
        self.clear_button = ttk.Button(control_frame, text="ログクリア", 
                                      command=self.clear_log)
        self.clear_button.grid(row=0, column=3, padx=5)
        
        # Initialize talking button
        self.init_button = ttk.Button(control_frame, text="会話初期化", 
                                     command=self.initialize_conversation)
        self.init_button.grid(row=0, column=4, padx=5)
        
        # Volume control frame
        volume_frame = ttk.LabelFrame(main_frame, text="音量制御", padding="5")
        volume_frame.grid(row=1, column=3, sticky=(tk.N, tk.S), padx=(10, 0))
        
        # Volume slider
        self.volume_var = tk.DoubleVar(value=0.8)
        self.volume_slider = ttk.Scale(volume_frame, from_=0.0, to=1.0, 
                                      variable=self.volume_var, 
                                      orient='vertical', length=150,
                                      command=self.update_volume)
        self.volume_slider.grid(row=0, column=0)
        
        # Volume label
        self.volume_label = ttk.Label(volume_frame, text="音量: 80%")
        self.volume_label.grid(row=1, column=0, pady=(5, 0))
        
        # Voice pitch visualization frame
        pitch_frame = ttk.LabelFrame(main_frame, text="声の高さ", padding="5")
        pitch_frame.grid(row=1, column=4, sticky=(tk.N, tk.S), padx=(10, 0))
        
        # Pitch visualization canvas
        self.pitch_canvas = tk.Canvas(pitch_frame, width=100, height=150, bg='white')
        self.pitch_canvas.grid(row=0, column=0)
        
        # Conversation history
        history_frame = ttk.LabelFrame(main_frame, text="会話履歴", padding="5")
        history_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=15, width=60,
                                                     font=('Arial', 10), wrap=tk.WORD)
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # User input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        input_frame.columnconfigure(0, weight=1)
        
        # Text input for manual messages
        self.text_input = ttk.Entry(input_frame, font=('Arial', 10))
        self.text_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.text_input.bind('<Return>', lambda e: self.send_text_message())
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="準備完了", 
                                     font=('Arial', 10, 'italic'))
        self.status_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        # Configure styles
        style = ttk.Style()
        style.configure('Start.TButton', foreground='green')
        
    def initialize_tts(self):
        try:
            self.tts_engine = pyttsx3.init()
            
            # Set Japanese female voice
            voices = self.tts_engine.getProperty('voices')
            japanese_voice = None
            
            for voice in voices:
                if 'japanese' in voice.name.lower() or 'ja' in voice.id.lower():
                    japanese_voice = voice
                    break
            
            if japanese_voice:
                self.tts_engine.setProperty('voice', japanese_voice.id)
            
            # Set voice properties
            self.tts_engine.setProperty('rate', 150)  # Speed
            self.tts_engine.setProperty('volume', self.volume_var.get())
            
            self.update_status("音声エンジン初期化完了")
        except Exception as e:
            self.update_status(f"音声エンジン初期化エラー: {str(e)}")
            messagebox.showerror("エラー", f"音声エンジンの初期化に失敗しました: {str(e)}")
    
    def update_volume(self, value=None):
        volume = self.volume_var.get()
        if self.tts_engine:
            self.tts_engine.setProperty('volume', volume)
        self.volume_label.config(text=f"音量: {int(volume * 100)}%")
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def start_conversation(self):
        self.is_talking = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.update_status("会話開始中...")
        
        # Start conversation thread
        thread = threading.Thread(target=self.conversation_loop)
        thread.daemon = True
        thread.start()
    
    def stop_conversation(self):
        self.is_talking = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.update_status("会話停止")
    
    def conversation_loop(self):
        try:
            # Ask the first question
            if self.current_question_index < len(self.questions):
                question = self.questions[self.current_question_index]
                self.speak_and_display("ボット", question)
                self.current_question_index += 1
            
            while self.is_talking:
                # Listen for user response
                user_response = self.listen_for_speech()
                
                if user_response and self.is_talking:
                    self.user_responses.append(user_response)
                    self.speak_and_display("ユーザー", user_response)
                    
                    # Generate next response
                    self.generate_next_response()
                    
                elif not self.is_talking:
                    break
                    
                time.sleep(0.5)
                    
        except Exception as e:
            self.update_status(f"会話エラー: {str(e)}")
            messagebox.showerror("エラー", f"会話中にエラーが発生しました: {str(e)}")
    
    def listen_for_speech(self):
        try:
            self.update_status("音声を聞いています...")
            
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
            # Listen for audio
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language='ja-JP')
            self.update_status("音声認識完了")
            return text
            
        except sr.WaitTimeoutError:
            self.update_status("音声入力タイムアウト")
            return None
        except sr.UnknownValueError:
            self.update_status("音声が認識できませんでした")
            return None
        except sr.RequestError as e:
            self.update_status(f"音声認識サービスエラー: {str(e)}")
            return None
        except Exception as e:
            self.update_status(f"音声認識エラー: {str(e)}")
            return None
    
    def generate_next_response(self):
        # Simple response generation based on context
        if self.current_question_index < len(self.questions):
            # Ask next predefined question
            response = self.questions[self.current_question_index]
            self.current_question_index += 1
        else:
            # Generate contextual response
            last_response = self.user_responses[-1] if self.user_responses else ""
            
            # Simple keyword-based responses
            if any(keyword in last_response for keyword in ["興味", "関心", "詳しく", "サンプル"]):
                response = "ありがとうございます。では、無料サンプルをお送りさせていただきますね。お店の詳細をお聞かせください。"
            elif any(keyword in last_response for keyword in ["忙しい", "時間", "用事"]):
                response = "お忙しい中、お時間をいただきありがとうございます。短時間でご説明させていただきます。"
            elif any(keyword in last_response for keyword in ["値段", "価格", "いくら", "安い", "高い"]):
                response = "1kgあたり588円（税別・送料込み）でご提供しております。送料も含まれておりますので、お得な価格設定となっております。"
            elif any(keyword in last_response for keyword in ["米", "ご飯", "品質", "味"]):
                response = "近江ブレンド米は、粒が小さくて弁当に詰めやすく、見た目も美しく仕上がります。味もおいしく、お客様にも好評です。"
            else:
                response = "ありがとうございます。他にご質問やご不明な点がございましたら、お気軽にお聞かせください。"
        
        self.speak_and_display("ボット", response)
    
    def speak_and_display(self, speaker, message):
        # Display in conversation history
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history_text.insert(tk.END, f"[{timestamp}] {speaker}: {message}\n\n")
        self.history_text.see(tk.END)
        
        # Speak the message
        if speaker == "ボット" and self.tts_engine:
            self.speak_message(message)
    
    def speak_message(self, message):
        try:
            # Visualize voice pitch changes
            self.animate_pitch()
            
            # Speak the message
            self.tts_engine.say(message)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            self.update_status(f"音声出力エラー: {str(e)}")
    
    def animate_pitch(self):
        # Simple pitch visualization animation
        self.pitch_canvas.delete("all")
        
        # Generate random pitch pattern
        for i in range(10):
            x = i * 10
            height = random.randint(20, 120)
            color = f"#{random.randint(100, 255):02x}{random.randint(100, 255):02x}{random.randint(100, 255):02x}"
            
            self.pitch_canvas.create_rectangle(x, 150-height, x+8, 150, 
                                             fill=color, outline="")
        
        self.root.update_idletasks()
    
    def send_text_message(self):
        text = self.text_input.get().strip()
        if text:
            self.user_responses.append(text)
            self.speak_and_display("ユーザー", text)
            self.text_input.delete(0, tk.END)
            
            # Generate response
            if self.is_talking:
                self.generate_next_response()
    
    def clear_log(self):
        self.history_text.delete(1.0, tk.END)
        self.conversation_log.clear()
        self.update_status("ログをクリアしました")
    
    def initialize_conversation(self):
        self.current_question_index = 0
        self.user_responses.clear()
        self.clear_log()
        self.update_status("会話を初期化しました")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AIAgent()
    app.run()
