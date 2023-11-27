import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import openai
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from config import OPENAI_API_KEY, CLIPDROP_API_KEY

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

SPOTIFY_CLIENT_ID = '0456943ace9d4666b09ae7cc8a6d253f'
SPOTIFY_CLIENT_SECRET = '659148aa437a4217af46f8b3d8744841'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'
SPOTIFY_SCOPE = 'user-modify-playback-state user-read-playback-state'

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                    client_secret=SPOTIFY_CLIENT_SECRET,
                                                    redirect_uri=SPOTIFY_REDIRECT_URI,
                                                    scope=SPOTIFY_SCOPE))

def generate_image(image_prompt):
    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
                      files={
                          'prompt': (None, image_prompt, 'text/plain')
                      },
                      headers={'x-api-key': CLIPDROP_API_KEY})
    if r.ok:
        return r.content
    else:
        r.raise_for_status()


def overlay_images(background_stream, overlay_path):
    # Open the background and overlay images
    background = Image.open(background_stream)
    overlay = Image.open(overlay_path)

    # Resize the background image to fit within specified coordinates
    target_size = (561 - 138, 275 - 0)  # Width and height
    resized_background = background.resize(target_size, Image.Resampling.LANCZOS)

    # Create a new blank (white) image (canvas) matching the size of the overlay image
    canvas = Image.new('RGB', overlay.size, (255, 255, 255))

    # Position for the resized background image within specified coordinates
    position = (138, 0)  # Top-left corner

    # Paste the resized background onto the canvas
    canvas.paste(resized_background, position)

    # Overlay the images
    canvas.paste(overlay, (0, 0), overlay)

    return ImageTk.PhotoImage(canvas)


class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro Timer")
        self.geometry("1000x650")

        self.label_timer = tk.Label(self, text="25:00", font=("Arial", 30))
        self.label_timer.pack(pady=50)

        self.start_button = tk.Button(self, text="Start", command=self.start_pomodoro)
        self.start_button.pack()

        self.question_entry = tk.Entry(self, width=50)
        self.question_entry.pack(pady=20)
        self.ask_button = tk.Button(self, text="Ask ChatGPT", command=self.ask_chatgpt)
        self.ask_button.pack()

        self.chat_output = tk.Text(self, height=10, width=50)
        self.chat_output.pack(pady=20)

    def set_background_image(self, image_prompt="abstract art"):
        image_bytes = generate_image(image_prompt)

        byte_stream = BytesIO(image_bytes)
        overlay_image_path = 'Images/LofiGirl_NoBackground.png'

        # Use the overlay_images function
        tk_combined_image = overlay_images(byte_stream, overlay_image_path)


        if hasattr(self, 'background_label'):
            self.background_label.destroy()

        self.background_label = tk.Label(self, image=tk_combined_image)
        self.background_label.image = tk_combined_image
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        
        # Raise other elements to the top
        self.label_timer.lift()
        self.start_button.lift()
        self.question_entry.lift()
        self.ask_button.lift()
        self.chat_output.lift()

    def play_music(self, track_uri):
        spotify.start_playback(uris=[track_uri])
    def pause_music(self):
        spotify.pause_playback()
    def set_static_layer(self):
        # Open the static layer image
        #static_layer = Image.open("Images/LofiGirl_NoBackground.png")
        #tk_static_layer = ImageTk.PhotoImage(static_layer)
        
        if hasattr(self, 'static_layer_label'):
            self.static_layer_label.destroy()
        
        #self.static_layer_label = tk.Label(self, image=tk_static_layer)
        #self.static_layer_label.image = tk_static_layer
        #self.static_layer_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Raise other elements above the static layer
        self.label_timer.lift()
        self.start_button.lift()
        self.question_entry.lift()
        self.ask_button.lift()
        self.chat_output.lift()
    

    def start_timer(self, minutes):
        for i in range(minutes * 60, 0, -1):
            if not self.label_timer.winfo_exists():
                break
            mins, secs = divmod(i, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            self.label_timer.config(text=timer)
            self.update()
            time.sleep(1)

    def run_pomodoro(self, num_sessions, study_time=25, short_break=5, long_break=15, sessions_before_long_break=4):
        for session in range(1, num_sessions + 1):
            messagebox.showinfo("Pomodoro Timer", f"Session {session} of {num_sessions}. Start studying!")
            self.start_timer(study_time)

            #self.play_music('spotify:track:your_track_uri')
            self.play_music('spotify:track:15DeqWWQB4dcEWzJg15VrN?si=84e6f713c2264109')

            messagebox.showinfo("Pomodoro Timer", f"Session {session} of {num_sessions}. Start studying!")
            #self.pause_music()
            
            if session == num_sessions:
                messagebox.showinfo("Pomodoro Timer", "Well done! You've completed all your study sessions!")
                break
            
            if session % sessions_before_long_break == 0:
                messagebox.showinfo("Pomodoro Timer", f"Take a long break of {long_break} minutes!")
                self.start_timer(long_break)
            else:
                messagebox.showinfo("Pomodoro Timer", f"Take a short break of {short_break} minutes!")
                self.start_timer(short_break)

    def start_pomodoro(self):
        sessions = simpledialog.askinteger("Input", "How many study sessions would you like?")
        if not sessions:
            return

        inspiration = simpledialog.askstring("Inspiration", "What inspires you?")
        if not inspiration:
            return

        self.set_background_image(inspiration)
        self.set_static_layer()  # Add the static layer
        self.run_pomodoro(sessions)

    def ask_chatgpt(self):
        question = self.question_entry.get()
        if question:
            response = openai.Completion.create(engine="davinci", prompt=question, max_tokens=150)
            self.chat_output.insert(tk.END, f"You: {question}\nChatGPT: {response.choices[0].text.strip()}\n")
            self.chat_output.see(tk.END)

if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()

