"""
Main window UI for the AI Agent application.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional, Callable
from ..config.settings import (
    APP_TITLE, WINDOW_SIZE, BG_COLOR, TITLE_FONT, STATUS_FONT, INPUT_FONT
)


class MainWindow:
    """Main application window with all UI components."""
    
    def __init__(self):
        """Initialize the main window."""
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BG_COLOR)
        
        # Callback functions
        self.start_callback: Optional[Callable] = None
        self.stop_callback: Optional[Callable] = None
        self.send_text_callback: Optional[Callable] = None
        self.clear_log_callback: Optional[Callable] = None
        self.init_conversation_callback: Optional[Callable] = None
        self.volume_change_callback: Optional[Callable] = None
        
        self._setup_ui()
        self._configure_styles()
    
    def _setup_ui(self):
        """Set up the main UI components."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text=APP_TITLE, font=TITLE_FONT)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Create control buttons
        self._create_control_buttons(control_frame)
        
        # Volume control frame
        self._create_volume_control(main_frame)
        
        # Voice visualization frame
        self._create_voice_visualization(main_frame)
        
        # Conversation history
        self._create_conversation_history(main_frame)
        
        # User input frame
        self._create_input_frame(main_frame)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="準備完了", font=STATUS_FONT)
        self.status_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))
    
    def _create_control_buttons(self, parent):
        """Create control buttons."""
        # Start button
        self.start_button = ttk.Button(parent, text="開始", 
                                      command=self._on_start_clicked,
                                      style='Start.TButton')
        self.start_button.grid(row=0, column=0, padx=(0, 5))
        
        # Stop button
        self.stop_button = ttk.Button(parent, text="停止", 
                                     command=self._on_stop_clicked,
                                     state='disabled')
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Send text button
        self.send_text_button = ttk.Button(parent, text="テキスト送信", 
                                          command=self._on_send_text_clicked)
        self.send_text_button.grid(row=0, column=2, padx=5)
        
        # Clear log button
        self.clear_button = ttk.Button(parent, text="ログクリア", 
                                      command=self._on_clear_log_clicked)
        self.clear_button.grid(row=0, column=3, padx=5)
        
        # Initialize talking button
        self.init_button = ttk.Button(parent, text="会話初期化", 
                                     command=self._on_init_conversation_clicked)
        self.init_button.grid(row=0, column=4, padx=5)
    
    def _create_volume_control(self, parent):
        """Create volume control components."""
        volume_frame = ttk.LabelFrame(parent, text="音量制御", padding="5")
        volume_frame.grid(row=1, column=3, sticky=(tk.N, tk.S), padx=(10, 0))
        
        # Volume slider
        self.volume_var = tk.DoubleVar(value=0.8)
        self.volume_slider = ttk.Scale(volume_frame, from_=0.0, to=1.0, 
                                      variable=self.volume_var, 
                                      orient='vertical', length=150,
                                      command=self._on_volume_changed)
        self.volume_slider.grid(row=0, column=0)
        
        # Volume label
        self.volume_label = ttk.Label(volume_frame, text="音量: 80%")
        self.volume_label.grid(row=1, column=0, pady=(5, 0))
    
    def _create_voice_visualization(self, parent):
        """Create voice visualization components."""
        pitch_frame = ttk.LabelFrame(parent, text="声の高さ", padding="5")
        pitch_frame.grid(row=1, column=4, sticky=(tk.N, tk.S), padx=(10, 0))
        
        # Pitch visualization canvas
        self.pitch_canvas = tk.Canvas(pitch_frame, width=100, height=150, bg='white')
        self.pitch_canvas.grid(row=0, column=0)
    
    def _create_conversation_history(self, parent):
        """Create conversation history components."""
        history_frame = ttk.LabelFrame(parent, text="会話履歴", padding="5")
        history_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=15, width=60,
                                                     font=INPUT_FONT, wrap=tk.WORD)
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def _create_input_frame(self, parent):
        """Create user input components."""
        input_frame = ttk.Frame(parent)
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        input_frame.columnconfigure(0, weight=1)
        
        # Text input for manual messages
        self.text_input = ttk.Entry(input_frame, font=INPUT_FONT)
        self.text_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.text_input.bind('<Return>', lambda e: self._on_send_text_clicked())
    
    def _configure_styles(self):
        """Configure UI styles."""
        style = ttk.Style()
        style.configure('Start.TButton', foreground='green')
    
    # Callback methods
    def _on_start_clicked(self):
        """Handle start button click."""
        if self.start_callback:
            self.start_callback()
    
    def _on_stop_clicked(self):
        """Handle stop button click."""
        if self.stop_callback:
            self.stop_callback()
    
    def _on_send_text_clicked(self):
        """Handle send text button click."""
        text = self.text_input.get().strip()
        if text and self.send_text_callback:
            self.send_text_callback(text)
            self.text_input.delete(0, tk.END)
    
    def _on_clear_log_clicked(self):
        """Handle clear log button click."""
        if self.clear_log_callback:
            self.clear_log_callback()
    
    def _on_init_conversation_clicked(self):
        """Handle initialize conversation button click."""
        if self.init_conversation_callback:
            self.init_conversation_callback()
    
    def _on_volume_changed(self, value=None):
        """Handle volume slider change."""
        volume = self.volume_var.get()
        self.volume_label.config(text=f"音量: {int(volume * 100)}%")
        if self.volume_change_callback:
            self.volume_change_callback(volume)
    
    # Public methods for external control
    def set_start_callback(self, callback: Callable):
        """Set callback for start button."""
        self.start_callback = callback
    
    def set_stop_callback(self, callback: Callable):
        """Set callback for stop button."""
        self.stop_callback = callback
    
    def set_send_text_callback(self, callback: Callable):
        """Set callback for send text button."""
        self.send_text_callback = callback
    
    def set_clear_log_callback(self, callback: Callable):
        """Set callback for clear log button."""
        self.clear_log_callback = callback
    
    def set_init_conversation_callback(self, callback: Callable):
        """Set callback for initialize conversation button."""
        self.init_conversation_callback = callback
    
    def set_volume_change_callback(self, callback: Callable):
        """Set callback for volume change."""
        self.volume_change_callback = callback
    
    def update_status(self, message: str):
        """Update status label."""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def add_to_history(self, entry: dict):
        """Add entry to conversation history."""
        timestamp = entry.get('timestamp', '')
        speaker = entry.get('speaker', '')
        message = entry.get('message', '')
        
        self.history_text.insert(tk.END, f"[{timestamp}] {speaker}: {message}\n\n")
        self.history_text.see(tk.END)
    
    def clear_history(self):
        """Clear conversation history display."""
        self.history_text.delete(1.0, tk.END)
    
    def set_conversation_state(self, is_active: bool):
        """Set conversation state and update button states."""
        if is_active:
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
        else:
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
    
    def update_voice_visualization(self, pitch_data: list):
        """Update voice visualization with pitch data."""
        self.pitch_canvas.delete("all")
        
        for x, height, color in pitch_data:
            self.pitch_canvas.create_rectangle(x, 150-height, x+8, 150, 
                                             fill=color, outline="")
        
        self.root.update_idletasks()
    
    def show_error(self, title: str, message: str):
        """Show error message dialog."""
        messagebox.showerror(title, message)
    
    def show_info(self, title: str, message: str):
        """Show info message dialog."""
        messagebox.showinfo(title, message)
    
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
    
    def destroy(self):
        """Destroy the window."""
        self.root.destroy()
