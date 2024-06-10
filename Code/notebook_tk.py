import tkinter as tk
import string
import time
from tkinter import ttk 
from spellchecker import SpellChecker

spell = SpellChecker()          # Initialize the spell checker

def spell_check(text_box):
    """
    Check for misspelled words in the text box and underline them.
    
    Parameters:
    - text_box: The Tkinter Text widget where text input is being checked.
    """
    text = text_box.get("1.0", 'end-1c')
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    words = text.split()
    misspelled = spell.unknown(words)
    
    text_box.tag_remove("misspelled", "1.0", tk.END)  # Remove previous misspelled tags
    
    for word in misspelled:
        start = 1.0
        idx = text_box.search(word, start, stopindex=tk.END)
        while idx:
            end = f"{idx}+{len(word)}c"
            text_box.tag_add("misspelled", idx, end)
            start = end
            idx = text_box.search(word, start, stopindex=tk.END)

    text_box.tag_config("misspelled", underline=True)  # Underline misspelled words

# New function to show context menu for corrections
def show_context_menu(event, text_box):
    """
    Show a context menu to suggest corrections for a misspelled word when right-clicked.
    
    Parameters:
    - event: The event object containing details of the right-click event.
    - text_box: The Text widget where the right-click occurred.
    """
    word_start = text_box.index(f"@{event.x},{event.y} wordstart")
    word_end = text_box.index(f"@{event.x},{event.y} wordend")
    word = text_box.get(word_start, word_end)
    
    if spell.unknown([word]):
        menu = tk.Menu(text_box, tearoff=0)
        corrections = spell.candidates(word)  # Get corrections
        if corrections:    
            for correction in corrections:
                menu.add_command(label=correction, 
                                command=lambda c=correction: text_box.delete(word_start, word_end) or text_box.insert(word_start, c))
        else:
            menu.add_command(label="N/A", state="disabled")
        menu.post(event.x_root, event.y_root)

        
def open_input_window(initial_text=None, title=None):
    """
    Open a new window for text input with options to set font and size.
    
    Parameters:
    - initial_text: Initial text to display in the text box (default None).
    - title: Initial title for the text input (default None).
    
    Returns:
    - Tuple containing the user's input text and title.
    """

    the_log = []
    global current_font, current_size  # Added: Declare global variables for the current font and size
    current_font = 'Arial'  # Added: Default font
    current_size = 12  # Added: Default size
    
    def submit_text(text_box, root):
        """
        Collects the text and title from the input fields and closes the window.
        
        Parameters:
        - text_box: The text box from which to collect the input text.
        - root: The Tk root window to close after submitting.
        """
        user_input = text_box.get("1.0", 'end-1c')  
        title = title_entry.get()
        the_log.append((user_input,title))
        
        root.destroy()

    def on_focus_in(event):
        """
        Handle the focus-in event for the title entry widget to clear placeholder text.
        
        Parameters:
        - event: The event object containing details about the focus-in event.
        """
        if title_entry.get() == 'Enter your title here':
            title_entry.delete(0, tk.END)
            title_entry.config(fg='black')  # Change text color to black

    def on_focus_out(event):
        """
        Handle the focus-out event for the title entry widget to restore placeholder text if empty.
        
        Parameters:
        - event: The event object containing details about the focus-out event.
        """
        if not title_entry.get():
            title_entry.insert(0, 'Enter your title here')
            title_entry.config(fg='grey')
         
    def apply_font():
        """
        Apply the selected font and size to the selected text in the text box or update global settings.
        This function handles changes triggered by the font and size combobox selections.
        """
        try:
            global current_font, current_size 
            selected_font = font_combobox.get()
            selected_size = size_combobox.get()
            
            if text_box.tag_ranges("sel"):
                start_index = text_box.index(tk.SEL_FIRST)
                end_index = text_box.index(tk.SEL_LAST)

                tag_name = "font" + str(time.time())
                text_box.tag_add(tag_name, start_index, end_index)
                text_box.tag_configure(tag_name, font=(selected_font, int(selected_size)))

            elif selected_font != current_font or int(selected_size) != current_size:
                current_font = selected_font 
                current_size = int(selected_size)
        except ValueError:
          print("Error: Font size must be a number")

    def apply_current_font(event): 
        """
        Apply the current global font and size settings to new text entered in the text box.
        
        Parameters:
        - event: The event object triggered by key press.
        """
        char_index = text_box.index(tk.INSERT)
        start_index = f"{char_index} - 1 chars"
        tag_name = f"font{current_font}size{current_size}"
        text_box.tag_add(tag_name, start_index, char_index)
        text_box.tag_configure(tag_name, font=(current_font, current_size))
    

    root = tk.Tk()
    root.title("Input your content here:")
    root.geometry("600x700") 
    root.resizable(True, True)
    root['bg'] = 'grey43'

    title_entry = tk.Entry(root, font=('Helvetica',16),highlightthickness=7, highlightbackground='DarkOrange3', highlightcolor='DarkOrange3')
    title_entry.grid(row=0, column=0, sticky="ew",
                     padx=20, pady=(0,20))
    if title:  # This checks if title is not None or empty
        title_entry.delete(0, tk.END)  # Delete the placeholder or existing text
        title_entry.insert(0, title)  # Insert the provided title
        title_entry.config(fg='black')  # Change text color to black
    else:
        title_entry.insert(0, 'Enter your title here')
    
    title_entry.bind("<FocusIn>", on_focus_in)
    title_entry.bind("<FocusOut>", on_focus_out)

    toolbar_frame = tk.Frame(root, highlightbackground='DarkOrange3',highlightthickness=7,bg='grey43')
    toolbar_frame.grid(row=1, column=0)#, sticky="ew")
   
    font_label = tk.Label(toolbar_frame, text="Font:")
    font_label.grid(row=1, column=2, sticky="nsew") 
    fonts = ['Arial', 'Helvetica', 'Times', 'Courier']  # Add or remove font types as needed
    font_combobox = ttk.Combobox(toolbar_frame, values=fonts, width=8)
    font_combobox.set('Arial')  # Default value
    font_combobox.grid(row=1, column=3, sticky="nsew") 
    font_combobox.bind("<<ComboboxSelected>>", lambda e: apply_font())  # Apply the font immediately when a selection is made


    _space_lable = tk.Label(toolbar_frame,bg='grey43')
    _space_lable.grid(row=1, column=4, sticky="nsew")

    size_label = tk.Label(toolbar_frame, text="Size:")
    size_label.grid(row=1, column=5, sticky="nsew") 

    sizes = [str(i) for i in range(8, 31)]  # Font sizes from 8 to 30 
    size_combobox = ttk.Combobox(toolbar_frame, values=sizes, width=3)
    size_combobox.set('12')  # Default value
    size_combobox.grid(row=1, column=6, sticky="nsew") 
    size_combobox.bind("<<ComboboxSelected>>", lambda e: apply_font())  # Apply the size immediately when a selection is made


    title_label = tk.Label(root, text="__Write your log here__",
                           font=('Helvetica',14),bg='grey43')
    title_label.grid(row=2, column=0, padx=20, pady=(20,0))

    content_frame = tk.Frame(root, bg='DarkOrange3',highlightbackground='grey43',highlightthickness=2,highlightcolor='grey43')
   
    content_frame.grid(row=3, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(content_frame,bg='DarkOrange3')
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_box = tk.Text(content_frame, wrap=tk.WORD,
                       yscrollcommand=scrollbar.set)  #inte fel testad
    
    text_box.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    text_box.bind("<Button-3>", lambda e: show_context_menu(e, text_box))
    # New - Use tags to style misspelled words
    text_box.tag_configure("misspelled", foreground="red", underline=1,)
    # New - Call spell_check function when text is inserted or deleted
    text_box.bind("<KeyPress>", apply_current_font) 
    # Insert initial text into the text box if provided
    if initial_text is not None:
        text_box.insert("1.0", initial_text)

    scrollbar.config(command=text_box.yview)

    submit_button = tk.Button(root, text="Save", activebackground='green', bg='DarkOrange3',highlightbackground='white',highlightthickness=5,command=lambda: submit_text(text_box, root))
    submit_button.grid(row=4, column=0, sticky="ew", padx=20, pady=20) 

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)


    root.mainloop() # Main loop to run the application

    return the_log[0] if the_log else (None, None)
