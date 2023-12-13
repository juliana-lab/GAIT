import tkinter as tk
from PIL import Image, ImageTk
from tkinter import simpledialog,messagebox
from tkinter import font as tkfont
import threading
import pygame
import time
import requests
from io import BytesIO
from config import OPENAI_API_KEY, CLIPDROP_API_KEY
from openai import OpenAI


#openai.api_key = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY) 




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


class WelcomePage(tk.Tk):
    def __init__(self,background_image_path):
        super().__init__()
        pygame.init()

        rgb_tuple = (251, 237, 228)
        hex_color = '#%02x%02x%02x' % rgb_tuple
        self.dominant_color = hex_color

        self.title("Welcome Page")
        self.configure(bg=self.dominant_color)
        self.attributes("-fullscreen", True)

        self.create_widgets(background_image_path)

    def create_widgets(self, background_image_path):
        try:
            # Load the background image
            image = Image.open(background_image_path)
            background_photo = ImageTk.PhotoImage(image)

            # Set the image on top of the background
            image_label = tk.Label(self, image=background_photo, bg=self.dominant_color)
            image_label.image = background_photo  # Keep a reference to the image.
            image_label.pack(pady=50)  # You can use pack or place to position your image.

        except Exception as e:
            print(f"Failed to load background image: {e}")

        button_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        start_button = tk.Button(self, text="Start", command=self.on_start_clicked,
                                 bg=self.dominant_color, fg="black",  # White text on colored background
                                 font=button_font,
                                 height=2, width=10)  # Adjust height and width as needed
        start_button.place(relx=0.5, rely=0.7, anchor="center")

        exit_button = tk.Button(self, text="Exit full screen", command=self.exit_fullscreen,
                                 bg=self.dominant_color, fg="black",  # White text on colored background
                                 font=button_font,
                                 height=2, width=13)  # Adjust height and width as needed
        #exit_button.place(relx=0.98, rely=0.98, anchor="se")
        exit_button.place(relx=1.0, rely=1.0, anchor="se")

    def on_start_clicked(self):
        self.open_new_page()

    def play_music(self, music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()

    def open_new_page(self):
        new_window = tk.Toplevel(self)
        new_window.configure(bg=self.dominant_color)
        new_window.attributes("-fullscreen", True)
        self.previous_window = new_window

        def create_image_with_title(parent, image_path, title,col,row,music_file):
            try:
                img = Image.open(image_path)
                img = img.resize((533, 333))  # Resize the image
                photo = ImageTk.PhotoImage(img)

                title_label = tk.Label(parent, text=title, bg=self.dominant_color, font=("Arial", 25,'bold'))
                #title_label.grid(row=0, column=col, sticky='w', padx=10)
                title_label.grid(row=row, column=col, sticky='w', padx=10, pady=(20, 10))  # Add vertical padding

                label = tk.Label(parent, image=photo, bg=self.dominant_color)
                label.image = photo  # Keep a reference to the image.
                #label.grid(row=1, column=col, padx=10)
                label.grid(row=row + 1, column=col, padx=10, pady=(10, 20))
                label.bind("<Enter>", lambda event, music_file=music_file: self.play_music(music_file))
                label.bind("<Leave>", lambda event: pygame.mixer.music.stop())
                # Inside create_image_with_title function
                label.bind("<Button-1>",
                           lambda event, music_file=music_file, image_path=image_path: self.show_combined_popup_dialog(
                               event, music_file, image_path))

            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

        # Add images and titles
        start_row =2
        create_image_with_title(new_window, 'Images/UrbanScholar.png', 'The Urban Scholar',col=0,row=start_row,music_file='Music/CityGirl.MP3')
        create_image_with_title(new_window, 'Images/BeachsideDreamer.png', 'The Beachside Dreamer',col=1,row=start_row,music_file='Music/BeachGirl.MP3')
        create_image_with_title(new_window, 'Images/CozyCabin.png', 'The Cozy Cabin Composer',col=0,row=start_row+2,music_file='Music/CabinGirl.mp3')
        create_image_with_title(new_window, 'Images/GardenNook.png', 'The Garden Nook Novelist',col=1,row=start_row+2,music_file='Music/GardenGirl.MP3')

        try:
            background_image_path = 'PomodoroDall.png'
            img = Image.open(background_image_path)
            photo = ImageTk.PhotoImage(img)

            background_label = tk.Label(new_window, image=photo, bg=self.dominant_color)
            background_label.image = photo  # Keep a reference to the image.
            background_label.grid(row=start_row, column=3, rowspan=6,
                                  sticky='nsew')  # Adjust the row and column as needed
        except Exception as e:
            print(f"Failed to load background image: {e}")

        exit_button = tk.Button(new_window, text="Exit full screen", command=self.exit_fullscreen,
                                bg=self.dominant_color, fg="black",
                                font=tkfont.Font(family="Helvetica", size=16, weight="bold"),
                                height=2, width=13)
        #exit_button.grid(row=start_row + 8, column=3, padx=10, pady=10, sticky='se')  # Bottom right corner
        exit_button.place(relx=1.0, rely=1.0, anchor="se")
        # Function to show pop-up dialog

    def show_combined_popup_dialog(self, event, music_file,image_path):
        # Create a custom dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Pomodoro Settings")

        # Define the dimensions of the dialog (width x height)
        dialog_width = 400
        dialog_height = 200

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position to center the dialog
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2

        # Set the geometry of the dialog to center it and make it bigger
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

        # Create labels and entry fields for questions
        sections_label = tk.Label(dialog, text="How many Pomodoro Sections?")
        sections_label.pack()
        sections_entry = tk.Entry(dialog)
        sections_entry.pack()

        inspiration_label = tk.Label(dialog, text="Background inspiration:")
        inspiration_label.pack()
        inspiration_entry = tk.Entry(dialog)
        inspiration_entry.pack()


        # Create a button to submit the answers and start the timer
        submit_button = tk.Button(dialog, text="Submit",
                                  command=lambda: self.start_pomodoro_from_popup(dialog,sections_entry,
                                                                                 inspiration_entry, image_path,music_file))
        submit_button.pack()

    def start_pomodoro_from_popup(self, dialog,sections_entry, inspiration_entry, image_path,music_file):
        # Destroy the popup dialog
        inspiration_text = inspiration_entry.get()
        sections_text = sections_entry.get()

        dialog.destroy()

        # Open the new page with the selected background image
        self.open_pomodoro_page(sections_text,inspiration_text,image_path,music_file)


    def open_pomodoro_page(self,sections_text,inspiration_text ,background_image_path,music_file):
        if hasattr(self, 'previous_window'):
            self.previous_window.destroy()

        self.session_number = 0
        self.sessions_before_long_break = 4  # Adjust as needed
        self.long_break = 15 * 60  # 15 minutes
        self.short_break = 5 * 60  # 5 minutes
        #self.pomodoro_duration = 25 * 60  # 25 minutes
        self.pomodoro_duration = 10  # 25 minutes

        new_page = tk.Toplevel(self)
        new_page.configure(bg=self.dominant_color)
        new_page.attributes("-fullscreen", True)

        # Customize the loading label
        loading_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        loading_label = tk.Label(new_page, text="Loading...", bg=self.dominant_color, fg="black", font=loading_font)
        loading_label.place(relx=0.5, rely=0.5, anchor="center")

        # Timer label
        timer_font = tkfont.Font(family="Helvetica", size=48, weight="bold")
        timer_label = tk.Label(new_page, bg=self.dominant_color, fg="black", font=timer_font)
        timer_label.place(relx=0.5, rely=0.2, anchor="center")

        # Parse the number of sections
        try:
            num_sessions = int(sections_text)
        except ValueError:
            messagebox.showerror("Error", "Invalid number of sessions.")
            return


        # Initialize timer
        #self.timer_seconds = 25 * 60  # 25 minutes
        #self.start_timer(new_page, timer_label, self.pomodoro_duration)


        # Function to update the timer
        def update_timer():
            if self.pomodoro_duration > 0:
                minutes, seconds = divmod(self.pomodoro_duration, 60)
                timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.pomodoro_duration -= 1
                new_page.after(1000, update_timer)
            else:
                self.session_number += 1
                if self.session_number == num_sessions:
                    #messagebox.showinfo("Pomodoro Timer", "Well done! You've completed all your study sessions!")
                    return  # Ends the timer updates

                if self.session_number % self.sessions_before_long_break == 0:
                    #messagebox.showinfo("Pomodoro Timer", f"Take a long break of {self.long_break // 60} minutes!")
                    self.start_timer(new_page, timer_label, self.long_break)
                else:
                    #messagebox.showinfo("Pomodoro Timer", f"Take a short break of {self.short_break // 60} minutes!")
                    self.start_timer(new_page, timer_label, self.short_break)

            # Session label
            session_string = "Session #" + str(self.session_number)
            session_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
            session_label = tk.Label(new_page, text=session_string, bg=self.dominant_color, fg="black",
                                     font=session_font)
            session_label.place(relx=0.1, rely=0.5, anchor="center")



        # Function to update the GUI with the image
        def update_image():
            image_bytes = generate_image(inspiration_text)
            byte_stream = BytesIO(image_bytes)

            #image = Image.open(byte_stream)
            tk_combined_image = overlay_images(byte_stream, background_image_path)

            # Update the GUI
            loading_label.configure(image=tk_combined_image, text="")
            loading_label.image = tk_combined_image  # Keep a reference


            update_timer()

            self.create_chatgpt_interface(new_page)

            self.play_music(music_file)

        # Create a separate thread for image generation
        thread = threading.Thread(target=update_image)
        thread.start()

        exit_button = tk.Button(new_page, text="Exit full screen", command=self.exit_fullscreen,
                                bg=self.dominant_color, fg="black",
                                font=tkfont.Font(family="Helvetica", size=16, weight="bold"),
                                height=2, width=13)
        exit_button.place(relx=1.0, rely=1.0, anchor="se")

    def create_chatgpt_interface(self, parent):
        # Create a Text widget for displaying the conversation
        chat_output = tk.Text(parent, height=10, width=120, bg=self.dominant_color,
                              borderwidth=0, highlightthickness=0)
        chat_output.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Create an Entry widget for the user's question
        question_entry = tk.Entry(parent, width=50)
        question_entry.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Create a Button to submit the question
        ask_button = tk.Button(parent, text="Ask ChatGPT",
                               command=lambda: self.ask_chatgpt(question_entry, chat_output))
        ask_button.pack(side=tk.BOTTOM, padx=5, pady=5)
        

    def handle_chatgpt_request(self, question, chat_output):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Act like an engineering tutor..."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                temperature=1,
                max_tokens=3000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            if response.choices and len(response.choices) > 0 and response.choices[0].message:
                response_text = response.choices[0].message.content
            else:
                response_text = "No response"
            chat_output.insert(tk.END, f"You: {question}\nChatGPT: {response_text}\n")
        except Exception as e:
            chat_output.insert(tk.END, f"Error: {e}\n")
        finally:
            chat_output.see(tk.END)

    def ask_chatgpt(self, question_entry, chat_output):
        question = question_entry.get()
        if question:
            # Start a new thread for handling the ChatGPT request
            threading.Thread(target=self.handle_chatgpt_request, args=(question, chat_output)).start()
            question_entry.delete(0, tk.END)  # Clear the input field

    def exit_fullscreen(self):
        if self.attributes("-fullscreen"):
            self.attributes("-fullscreen", False)
        else:
            for window in self.winfo_children():
                if isinstance(window, tk.Toplevel) and window.attributes("-fullscreen"):
                    window.attributes("-fullscreen", False)
                    break

if __name__ == "__main__":
    app = WelcomePage(background_image_path='PomodoroDall.png')
    app.mainloop()
