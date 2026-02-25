"""
🌟 Kids Learning World 🌟
A colorful, fun learning app for 3-year-olds!
Topics: Alphabets, Numbers, Words, Math Signs, Tables

Requirements:
    pip install gtts pygame

Run: python kids_learning_app.py
"""

import tkinter as tk
from tkinter import font as tkfont
import threading
import os
import sys
import tempfile
import time
import random
import math

# ── Audio setup ───────────────────────────────────────────────────────────────
try:
    from gtts import gTTS
    import pygame
    pygame.mixer.init()
    AUDIO_OK = True
except ImportError:
    AUDIO_OK = False

# ── Color Palette ─────────────────────────────────────────────────────────────
COLORS = {
    "bg":       "#FFF9F0",
    "red":      "#FF6B6B",
    "orange":   "#FF9F43",
    "yellow":   "#FECA57",
    "green":    "#1DD1A1",
    "teal":     "#00D2D3",
    "blue":     "#54A0FF",
    "purple":   "#5F27CD",
    "pink":     "#FF9FF3",
    "dark":     "#2D3436",
    "white":    "#FFFFFF",
    "light":    "#F8F9FA",
    "card_shadow": "#E0E0E0",
}

CARD_COLORS = [
    "#FF6B6B","#FF9F43","#FECA57","#1DD1A1",
    "#00D2D3","#54A0FF","#5F27CD","#FF9FF3",
    "#FF6348","#7BED9F","#70A1FF","#ECCC68",
]

ALPHABET_WORDS = {
    "A": ("Apple",   "🍎"), "B": ("Ball",    "⚽"), "C": ("Cat",     "🐱"),
    "D": ("Dog",     "🐶"), "E": ("Elephant","🐘"), "F": ("Fish",    "🐟"),
    "G": ("Grapes",  "🍇"), "H": ("House",   "🏠"), "I": ("Ice Cream","🍦"),
    "J": ("Jellyfish","🪼"),"K": ("Kite",    "🪁"), "L": ("Lion",    "🦁"),
    "M": ("Moon",    "🌙"), "N": ("Nest",    "🪺"), "O": ("Orange",  "🍊"),
    "P": ("Parrot",  "🦜"), "Q": ("Queen",   "👑"), "R": ("Rainbow", "🌈"),
    "S": ("Sun",     "☀️"), "T": ("Train",   "🚂"), "U": ("Umbrella","☂️"),
    "V": ("Violin",  "🎻"), "W": ("Watermelon","🍉"),"X": ("Xylophone","🎵"),
    "Y": ("Yacht",   "⛵"), "Z": ("Zebra",   "🦓"),
}

NUMBER_WORDS = {
    1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five",
    6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten",
    11:"Eleven", 12:"Twelve", 13:"Thirteen", 14:"Fourteen", 15:"Fifteen",
    16:"Sixteen", 17:"Seventeen", 18:"Eighteen", 19:"Nineteen", 20:"Twenty",
}

NUMBER_EMOJIS = ["","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣",
                 "🔟","1️⃣1️⃣","1️⃣2️⃣","1️⃣3️⃣","1️⃣4️⃣","1️⃣5️⃣",
                 "1️⃣6️⃣","1️⃣7️⃣","1️⃣8️⃣","1️⃣9️⃣","2️⃣0️⃣"]

MATH_SIGNS = {
    "+": ("Plus",       "Adding things together! 2 + 3 = 5",  "🟢"),
    "-": ("Minus",      "Taking away! 5 - 2 = 3",             "🔴"),
    "×": ("Multiply",   "Groups of things! 3 × 2 = 6",        "🟣"),
    "÷": ("Divide",     "Sharing equally! 6 ÷ 2 = 3",         "🟡"),
    "=": ("Equals",     "Both sides are the same!",           "🔵"),
    ">": ("Greater Than","Bigger number! 5 > 3",              "🟠"),
    "<": ("Less Than",  "Smaller number! 3 < 5",              "🩷"),
    "%": ("Percent",    "Out of 100! 50% = half",             "🤍"),
}

SPELL_WORDS = [
    ("CAT",  "🐱", "C-A-T spells CAT!"),
    ("DOG",  "🐶", "D-O-G spells DOG!"),
    ("SUN",  "☀️", "S-U-N spells SUN!"),
    ("BEE",  "🐝", "B-E-E spells BEE!"),
    ("EGG",  "🥚", "E-G-G spells EGG!"),
    ("HEN",  "🐔", "H-E-N spells HEN!"),
    ("COW",  "🐄", "C-O-W spells COW!"),
    ("PIG",  "🐷", "P-I-G spells PIG!"),
    ("ANT",  "🐜", "A-N-T spells ANT!"),
    ("OWL",  "🦉", "O-W-L spells OWL!"),
    ("FLY",  "🪰", "F-L-Y spells FLY!"),
    ("BAT",  "🦇", "B-A-T spells BAT!"),
    ("FOX",  "🦊", "F-O-X spells FOX!"),
    ("BUS",  "🚌", "B-U-S spells BUS!"),
    ("CUP",  "☕", "C-U-P spells CUP!"),
    ("HAT",  "🎩", "H-A-T spells HAT!"),
    ("JAM",  "🍓", "J-A-M spells JAM!"),
    ("MAP",  "🗺️", "M-A-P spells MAP!"),
    ("NET",  "🥅", "N-E-T spells NET!"),
    ("POT",  "🪴", "P-O-T spells POT!"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Audio helper
# ─────────────────────────────────────────────────────────────────────────────
_audio_cache = {}
_last_speak: list = [0.0, ""]   # [timestamp, text]

def speak(text: str):
    if not AUDIO_OK:
        return
    import time as _time
    now = _time.monotonic()
    if text == _last_speak[1] and now - _last_speak[0] < 0.5:
        return   # same text within 500 ms → ignore duplicate
    _last_speak[0] = now
    _last_speak[1] = text
    def _do():
        try:
            key = text.lower().strip()
            if key not in _audio_cache:
                tts = gTTS(text=text, lang="en", slow=False)
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(tmp.name)
                _audio_cache[key] = tmp.name
            path = _audio_cache[key]
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except Exception:
            pass
    threading.Thread(target=_do, daemon=True).start()


# ─────────────────────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────────────────────
class KidsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌟 Kids Learning World 🌟")
        self.geometry("1100x750")
        self.minsize(900, 650)
        self.configure(bg=COLORS["bg"])
        self.resizable(True, True)

        # Fonts
        self.f_title  = tkfont.Font(family="Arial Rounded MT Bold" if sys.platform=="win32" else "Arial", size=28, weight="bold")
        self.f_big    = tkfont.Font(family="Arial Rounded MT Bold" if sys.platform=="win32" else "Arial", size=22, weight="bold")
        self.f_card   = tkfont.Font(family="Arial Rounded MT Bold" if sys.platform=="win32" else "Arial", size=18, weight="bold")
        self.f_med    = tkfont.Font(family="Arial", size=14, weight="bold")
        self.f_small  = tkfont.Font(family="Arial", size=11)
        self.f_emoji  = tkfont.Font(family="Segoe UI Emoji" if sys.platform=="win32" else "Arial", size=40)
        self.f_emoji_sm= tkfont.Font(family="Segoe UI Emoji" if sys.platform=="win32" else "Arial", size=24)

        self.current_section = None
        self._stars = []
        self._build_layout()
        self._show_home()
        self.after(200, self._animate_stars)  # Delay until window is fully rendered
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    # ── Layout skeleton ───────────────────────────────────────────────────────
    def _build_layout(self):
        # Top nav bar
        self.nav = tk.Frame(self, bg=COLORS["purple"], height=70)
        self.nav.pack(fill="x")
        self.nav.pack_propagate(False)

        tk.Label(self.nav, text="🌟 Kids Learning World 🌟",
                 font=self.f_big, bg=COLORS["purple"], fg=COLORS["white"]
                 ).pack(side="left", padx=20, pady=15)

        # Nav buttons
        nav_items = [
            ("🏠 Home",      self._show_home,      COLORS["yellow"]),
            ("🔤 Alphabets", self._show_alphabets,  COLORS["green"]),
            ("🔢 Numbers",   self._show_numbers,    COLORS["blue"]),
            ("📝 Spellings", self._show_spellings,  COLORS["pink"]),
            ("➕ Math Signs",self._show_math,       COLORS["orange"]),
            ("📊 Tables",    self._show_tables,     COLORS["teal"]),
        ]
        for label, cmd, color in nav_items:
            btn = tk.Button(self.nav, text=label, font=self.f_small,
                            bg=color, fg=COLORS["dark"],
                            relief="flat", padx=10, pady=8,
                            cursor="hand2", bd=0,
                            activebackground=COLORS["white"],
                            command=cmd)
            btn.pack(side="right", padx=4, pady=12)

        # Main canvas area
        self.main = tk.Frame(self, bg=COLORS["bg"])
        self.main.pack(fill="both", expand=True)

        # Floating star canvas (decorative background)
        self.star_canvas = tk.Canvas(self.main, bg=COLORS["bg"],
                                     highlightthickness=0)
        self.star_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Content frame (sits above stars)
        self.content = tk.Frame(self.main, bg=COLORS["bg"])
        self.content.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Audio hint label
        if not AUDIO_OK:
            tk.Label(self.nav,
                     text="📢 Install gtts & pygame for sound",
                     font=self.f_small, bg=COLORS["red"], fg="white",
                     padx=8
                     ).pack(side="right", padx=4, pady=16)

    def _clear_content(self):
        self.unbind_all("<MouseWheel>")
        for w in self.content.winfo_children():
            w.destroy()

    # ── Animated stars background ─────────────────────────────────────────────
    def _animate_stars(self):
        c = self.star_canvas
        c.delete("star")
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 60 or h < 60:   # Window not ready yet, try again shortly
            self.after(200, self._animate_stars)
            return
        star_chars = ["✦","✧","⭐","🌟","💫","⚡","🌈"]
        for _ in range(18):
            x = random.randint(20, w-20)
            y = random.randint(20, h-20)
            s = random.choice(star_chars)
            size = random.randint(12, 22)
            alpha_color = random.choice(["#FFD70044","#FF69B444","#87CEEB44",
                                         "#98FB9844","#DDA0DD44"])
            c.create_text(x, y, text=s, font=("Arial", size),
                          fill=random.choice(["#FFECB3","#B3E5FC","#C8E6C9",
                                              "#F8BBD0","#E1BEE7"]),
                          tags="star")
        self.after(3000, self._animate_stars)

    # ─────────────────────────────────────────────────────────────────────────
    # HOME SCREEN
    # ─────────────────────────────────────────────────────────────────────────
    def _show_home(self):
        self._clear_content()
        f = self.content

        tk.Label(f, text="Welcome, Little Learner! 🎉",
                 font=self.f_title, bg=COLORS["bg"], fg=COLORS["purple"]
                 ).pack(pady=(40, 8))
        tk.Label(f, text="Tap any button to start learning today!",
                 font=self.f_med, bg=COLORS["bg"], fg=COLORS["dark"]
                 ).pack(pady=(0, 30))

        grid = tk.Frame(f, bg=COLORS["bg"])
        grid.pack()

        tiles = [
            ("🔤", "Alphabets", "Learn A to Z!", COLORS["green"],   self._show_alphabets),
            ("🔢", "Numbers",   "Count 1 to 20!",COLORS["blue"],    self._show_numbers),
            ("📝", "Spellings", "Spell words!",  COLORS["pink"],    self._show_spellings),
            ("➕", "Math Signs","Plus, Minus...", COLORS["orange"],  self._show_math),
            ("📊", "Tables",    "2×3 = 6!",      COLORS["teal"],    self._show_tables),
        ]

        for i, (emoji, title, desc, color, cmd) in enumerate(tiles):
            col = i % 3
            row = i // 3
            card = tk.Frame(grid, bg=color, cursor="hand2",
                            relief="flat", bd=0)
            card.grid(row=row, column=col, padx=16, pady=16,
                      ipadx=20, ipady=16, sticky="nsew")

            tk.Label(card, text=emoji, font=self.f_emoji,
                     bg=color).pack(pady=(12,2))
            tk.Label(card, text=title, font=self.f_card,
                     bg=color, fg=COLORS["white"]).pack()
            tk.Label(card, text=desc, font=self.f_small,
                     bg=color, fg=COLORS["white"]).pack(pady=(2,12))

            card.bind("<Button-1>", lambda e, c=cmd: c())
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda e, c=cmd: c())

            # Hover effect
            def on_enter(e, w=card, c=color):
                w.configure(bg=self._darken(c))
                for ch in w.winfo_children(): ch.configure(bg=self._darken(c))
            def on_leave(e, w=card, c=color):
                w.configure(bg=c)
                for ch in w.winfo_children(): ch.configure(bg=c)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

        tk.Label(f, text="🔊 Tap any card to hear the sound!",
                 font=self.f_small, bg=COLORS["bg"], fg=COLORS["teal"]
                 ).pack(pady=20)

    def _on_closing(self):
        for path in _audio_cache.values():
            try:
                os.unlink(path)
            except Exception:
                pass
        self.destroy()

    def _darken(self, hex_color):
        r = int(hex_color[1:3],16)
        g = int(hex_color[3:5],16)
        b = int(hex_color[5:7],16)
        r = max(0, r-30); g = max(0, g-30); b = max(0, b-30)
        return f"#{r:02X}{g:02X}{b:02X}"

    # ─────────────────────────────────────────────────────────────────────────
    # ALPHABETS
    # ─────────────────────────────────────────────────────────────────────────
    def _show_alphabets(self):
        self._clear_content()
        f = self.content

        tk.Label(f, text="🔤 Learn the Alphabet!",
                 font=self.f_title, bg=COLORS["bg"], fg=COLORS["green"]
                 ).pack(pady=(20, 4))
        tk.Label(f, text="Click any letter to hear it!",
                 font=self.f_small, bg=COLORS["bg"], fg=COLORS["dark"]
                 ).pack(pady=(0,10))

        # Detail panel at top
        detail = tk.Frame(f, bg=COLORS["green"], pady=10)
        detail.pack(fill="x", padx=40, pady=(0, 10))
        self._alph_letter_lbl = tk.Label(detail, text="A", font=self.f_title,
                                          bg=COLORS["green"], fg="white")
        self._alph_letter_lbl.pack(side="left", padx=20)
        self._alph_word_lbl = tk.Label(detail, text="A is for Apple 🍎",
                                        font=self.f_big, bg=COLORS["green"], fg="white")
        self._alph_word_lbl.pack(side="left", padx=10)

        # Scrollable grid
        canvas = tk.Canvas(f, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(f, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=COLORS["bg"])
        scrollable.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(20,0))
        scrollbar.pack(side="right", fill="y")

        letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        cols = 7
        for i, letter in enumerate(letters):
            row = i // cols
            col = i % cols
            color = CARD_COLORS[i % len(CARD_COLORS)]
            word, emoji = ALPHABET_WORDS[letter]

            card = tk.Frame(scrollable, bg=color, cursor="hand2",
                            relief="flat", bd=0, width=110, height=110)
            card.grid(row=row, column=col, padx=8, pady=8)
            card.pack_propagate(False)

            tk.Label(card, text=letter, font=self.f_title,
                     bg=color, fg="white").pack(pady=(10,0))
            tk.Label(card, text=emoji, font=self.f_emoji_sm,
                     bg=color).pack()
            tk.Label(card, text=word[:6], font=self.f_small,
                     bg=color, fg="white").pack()

            def on_click(e, l=letter, w=word, em=emoji, c=color):
                self._alph_letter_lbl.configure(text=l, bg=c)
                self._alph_word_lbl.configure(
                    text=f"{l} is for {w} {em}", bg=c)
                detail.configure(bg=c)
                speak(f"{l}. {l} is for {w}. {w}.")
            card.bind("<Button-1>", on_click)
            for ch in card.winfo_children():
                ch.bind("<Button-1>", on_click)

        # Mouse wheel scroll
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # ─────────────────────────────────────────────────────────────────────────
    # NUMBERS
    # ─────────────────────────────────────────────────────────────────────────
    def _show_numbers(self):
        self._clear_content()
        f = self.content

        tk.Label(f, text="🔢 Let's Count!",
                 font=self.f_title, bg=COLORS["bg"], fg=COLORS["blue"]
                 ).pack(pady=(20,4))
        tk.Label(f, text="Click a number to hear it!",
                 font=self.f_small, bg=COLORS["bg"], fg=COLORS["dark"]
                 ).pack(pady=(0,10))

        # Detail strip
        detail = tk.Frame(f, bg=COLORS["blue"], pady=12)
        detail.pack(fill="x", padx=40, pady=(0,10))
        self._num_lbl = tk.Label(detail, text="1️⃣  One",
                                  font=self.f_big, bg=COLORS["blue"], fg="white")
        self._num_lbl.pack()

        # Grid
        outer = tk.Frame(f, bg=COLORS["bg"])
        outer.pack(fill="both", expand=True, padx=20, pady=4)

        cols = 5
        for i in range(1, 21):
            row = (i-1) // cols
            col = (i-1) % cols
            color = CARD_COLORS[i % len(CARD_COLORS)]
            word = NUMBER_WORDS[i]
            emoji = NUMBER_EMOJIS[i] if i <= 10 else ""

            card = tk.Frame(outer, bg=color, cursor="hand2",
                            relief="flat", bd=0, width=150, height=110)
            card.grid(row=row, column=col, padx=10, pady=8)
            card.pack_propagate(False)

            tk.Label(card, text=str(i), font=self.f_title,
                     bg=color, fg="white").pack(pady=(10,0))
            if emoji:
                tk.Label(card, text=emoji, font=self.f_emoji_sm,
                         bg=color).pack()
            tk.Label(card, text=word, font=self.f_med,
                     bg=color, fg="white").pack()

            dots_txt = ("●" * min(i,10)) + ("\n"+"●" * max(0,i-10) if i>10 else "")
            tk.Label(card, text=dots_txt, font=("Arial",7),
                     bg=color, fg="white", wraplength=130).pack()

            def on_click(e, n=i, w=word, em=emoji, c=color):
                self._num_lbl.configure(
                    text=f"{em}  {n}  —  {w}  {em}", bg=c)
                detail.configure(bg=c)
                speak(f"{n}. {w}.")
            card.bind("<Button-1>", on_click)
            for ch in card.winfo_children():
                ch.bind("<Button-1>", on_click)

    # ─────────────────────────────────────────────────────────────────────────
    # SPELLINGS
    # ─────────────────────────────────────────────────────────────────────────
    def _show_spellings(self):
        self._clear_content()
        f = self.content

        tk.Label(f, text="📝 Spell It Out!",
                 font=self.f_title, bg=COLORS["bg"], fg=COLORS["pink"]
                 ).pack(pady=(20,4))
        tk.Label(f, text="Click a word to hear how it's spelled!",
                 font=self.f_small, bg=COLORS["bg"], fg=COLORS["dark"]
                 ).pack(pady=(0,10))

        # Spell detail panel
        detail = tk.Frame(f, bg=COLORS["pink"], pady=14)
        detail.pack(fill="x", padx=40, pady=(0,10))
        self._spell_lbl = tk.Label(detail, text="🐱  C - A - T  =  CAT",
                                    font=self.f_big, bg=COLORS["pink"], fg="white")
        self._spell_lbl.pack()

        # Word cards grid
        canvas = tk.Canvas(f, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(f, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=COLORS["bg"])
        scrollable.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(20,0))
        scrollbar.pack(side="right", fill="y")

        cols = 5
        for i, (word, emoji, hint) in enumerate(SPELL_WORDS):
            row = i // cols
            col = i % cols
            color = CARD_COLORS[i % len(CARD_COLORS)]
            letters = " - ".join(list(word))

            card = tk.Frame(scrollable, bg=color, cursor="hand2",
                            relief="flat", bd=0, width=150, height=120)
            card.grid(row=row, column=col, padx=8, pady=8)
            card.pack_propagate(False)

            tk.Label(card, text=emoji, font=self.f_emoji_sm,
                     bg=color).pack(pady=(8,0))
            tk.Label(card, text=word, font=self.f_card,
                     bg=color, fg="white").pack()
            tk.Label(card, text=letters, font=self.f_small,
                     bg=color, fg="white").pack(pady=(2,8))

            def on_click(e, w=word, em=emoji, h=hint, c=color, l=letters):
                self._spell_lbl.configure(
                    text=f"{em}  {l}  =  {w}", bg=c)
                detail.configure(bg=c)
                speak(h)
            card.bind("<Button-1>", on_click)
            for ch in card.winfo_children():
                ch.bind("<Button-1>", on_click)

        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # ─────────────────────────────────────────────────────────────────────────
    # MATH SIGNS
    # ─────────────────────────────────────────────────────────────────────────
    def _show_math(self):
        self._clear_content()
        f = self.content

        tk.Label(f, text="➕ Math Signs!",
                 font=self.f_title, bg=COLORS["bg"], fg=COLORS["orange"]
                 ).pack(pady=(20,4))
        tk.Label(f, text="Click a sign to learn what it means!",
                 font=self.f_small, bg=COLORS["bg"], fg=COLORS["dark"]
                 ).pack(pady=(0,10))

        # Detail panel
        detail = tk.Frame(f, bg=COLORS["orange"], pady=14)
        detail.pack(fill="x", padx=40, pady=(0,10))
        self._math_lbl = tk.Label(detail,
                                   text="➕  Plus — Adding things together!  2 + 3 = 5",
                                   font=self.f_big, bg=COLORS["orange"], fg="white",
                                   wraplength=800)
        self._math_lbl.pack()

        # Sign cards
        outer = tk.Frame(f, bg=COLORS["bg"])
        outer.pack(fill="both", expand=True, padx=40, pady=10)

        for i, (sign, (name, desc, dot)) in enumerate(MATH_SIGNS.items()):
            color = CARD_COLORS[i*3 % len(CARD_COLORS)]
            row = i // 4
            col = i % 4

            card = tk.Frame(outer, bg=color, cursor="hand2",
                            relief="flat", bd=0, width=180, height=150)
            card.grid(row=row, column=col, padx=16, pady=12)
            card.pack_propagate(False)

            tk.Label(card, text=sign, font=tkfont.Font(family="Arial", size=52, weight="bold"),
                     bg=color, fg="white").pack(pady=(8,0))
            tk.Label(card, text=name, font=self.f_card,
                     bg=color, fg="white").pack()
            tk.Label(card, text=desc[:28]+"…" if len(desc)>28 else desc,
                     font=self.f_small, bg=color, fg="white",
                     wraplength=160).pack(pady=(2,8))

            def on_click(e, s=sign, n=name, d=desc, c=color, em=dot):
                self._math_lbl.configure(text=f"{s}  {n} — {d}", bg=c)
                detail.configure(bg=c)
                speak(f"{n}. {d}")
            card.bind("<Button-1>", on_click)
            for ch in card.winfo_children():
                ch.bind("<Button-1>", on_click)

    # ─────────────────────────────────────────────────────────────────────────
    # TABLES
    # ─────────────────────────────────────────────────────────────────────────
    def _show_tables(self):
        self._clear_content()
        f = self.content

        tk.Label(f, text="📊 Multiplication Tables!",
                 font=self.f_title, bg=COLORS["bg"], fg=COLORS["teal"]
                 ).pack(pady=(15,4))
        tk.Label(f, text="Pick a table and click each row to hear it!",
                 font=self.f_small, bg=COLORS["bg"], fg=COLORS["dark"]
                 ).pack(pady=(0,8))

        body = tk.Frame(f, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=20)

        # Left: table selector
        left = tk.Frame(body, bg=COLORS["bg"], width=220)
        left.pack(side="left", fill="y", padx=(0,10))
        left.pack_propagate(False)

        tk.Label(left, text="Choose Table:",
                 font=self.f_med, bg=COLORS["bg"], fg=COLORS["teal"]
                 ).pack(pady=(10,6))

        self._table_num = tk.IntVar(value=2)
        self._table_frame = None

        btn_frame = tk.Frame(left, bg=COLORS["bg"])
        btn_frame.pack(fill="x")

        table_btns_row = tk.Frame(left, bg=COLORS["bg"])
        table_btns_row.pack()
        for n in range(1, 13):
            color = CARD_COLORS[n % len(CARD_COLORS)]
            btn = tk.Button(table_btns_row, text=f"✖ {n}", font=self.f_med,
                            bg=color, fg="white", relief="flat",
                            cursor="hand2", width=6, pady=6,
                            command=lambda x=n: self._load_table(x, right))
            btn.grid(row=(n-1)//3, column=(n-1)%3, padx=4, pady=4)

        # Right: table display
        right = tk.Frame(body, bg=COLORS["white"],
                         relief="solid", bd=1)
        right.pack(side="left", fill="both", expand=True)
        self._load_table(2, right)

    def _load_table(self, num: int, parent: tk.Frame):
        for w in parent.winfo_children():
            w.destroy()

        color = CARD_COLORS[num % len(CARD_COLORS)]

        tk.Label(parent, text=f"Table of {num} 📊",
                 font=self.f_big, bg=color, fg="white",
                 pady=12).pack(fill="x")

        for i in range(1, 13):
            result = num * i
            row_color = COLORS["white"] if i % 2 == 0 else COLORS["light"]

            row = tk.Frame(parent, bg=row_color, cursor="hand2")
            row.pack(fill="x", padx=20, pady=2)

            text = f"  {num}  ×  {i}  =  {result}"
            lbl = tk.Label(row, text=text, font=self.f_big,
                           bg=row_color, fg=COLORS["dark"],
                           pady=8, anchor="w")
            lbl.pack(side="left", fill="x", expand=True)

            sound_lbl = tk.Label(row, text="🔊", font=self.f_emoji_sm,
                                  bg=row_color, cursor="hand2")
            sound_lbl.pack(side="right", padx=10)

            phrase = f"{num} times {i} equals {result}"
            row.bind("<Button-1>", lambda e, p=phrase: speak(p))
            lbl.bind("<Button-1>", lambda e, p=phrase: speak(p))
            sound_lbl.bind("<Button-1>", lambda e, p=phrase: speak(p))

            def enter(e, w=row, c=color):
                w.configure(bg=c)
                for ch in w.winfo_children(): ch.configure(bg=c)
            def leave(e, w=row, c=row_color):
                w.configure(bg=c)
                for ch in w.winfo_children(): ch.configure(bg=c)
            row.bind("<Enter>", enter)
            row.bind("<Leave>", leave)

        speak(f"Table of {num}")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = KidsApp()
    app.mainloop()
