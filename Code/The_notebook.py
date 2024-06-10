from datetime import date, datetime
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from notebook_tk import open_input_window, spell_check, show_context_menu
from termcolor import colored
import pyinputplus as pyip
import os
import time


# Retrieve current date and time, formatted for display and filenames
current_date = date.today()
formatted_date = current_date.strftime("%d-%m-%Y")
current_datetime = datetime.now()
date_time = current_datetime.strftime("%d/%m kl:%H:%M")

# Load sensitive configuration from environment variables
encoded_key = os.environ.get('encryption_key')
log_folder = os.environ.get('LOG_DIRECTORY')
password = os.environ.get('THE_PASSWORD')

# Ensure the encryption key is available and decode it
if not encoded_key:
    raise Exception(colored("Encryption_key environment variable not set"),"red")
encryption_key = b64decode(encoded_key)


def clear_terminal():                                   #Clears the terminal screen to maintain a clean UI. 
    os.system('cls' if os.name == 'nt' else 'clear')    #Uses different commands based on the operating system.

def import_txt() -> list: # Imports and returns a list of .txt files from the designated log directory.
    try:
        all_files = os.listdir(log_folder)
    except Exception as e:
        print(colored(f"Failed to list directory: {e}", "red"))
        return
    txt_files = [f for f in all_files if f.endswith('.txt')]
    if not txt_files:
        print(colored("\t\tERROR! There are no txt files in the current directory.", "red"))
        return
    return txt_files

def encrypt(text:str,key:str=encryption_key)->str:  #Encrypts a given string using AES encryption.
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(text.encode())
    return b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

def decrypt(text:str,key:str=encryption_key)->str:   #Decrypts a previously encrypted string using AES decryption.
    decoded = b64decode(text)
    nonce, tag, ciphertext = decoded[:16], decoded[16:32], decoded[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')

def create_new_logs():  #Handles the creation of new encrypted log entries.
    print(log_folder)
    
    the_log, title = open_input_window() 

    if the_log:
        encrypted_log = encrypt(f'{the_log}\n\nLast edited: {date_time}',encryption_key)   

        filename = f'{formatted_date}_{title}'
        the_file = f"{filename}.txt"

        directory = os.path.join(log_folder, the_file)
    
        dir_name = os.path.dirname(directory)  # Get the directory name (without the file)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"\t\tDirectory {dir_name} created")

        with open(directory, 'w') as f:
            f.write(encrypted_log)

        print(f'\n\t\tSaving "{title}".....\n')
        time.sleep(1)
        print(colored('\t\tSuccess!','green'))
        time.sleep(1)
        print(f'\t\tThe log "{title}" has been saved ')
    else:
        print(colored('\n\t\tThere where no entery so nothing was saved.', 'yellow'))
    time.sleep(2)

def list_all_logs():    #Lists all .txt log files in the log directory.
    txt_files = import_txt()
    if not txt_files:
        print("\t\tThere are no txt files in the current directory.")
        return
    
    print("\t\tList of all logs:\n")
    for index, filename in enumerate(txt_files):
       print(f"\t\t{index + 1}. {filename}:")

def view_log(choice:int):  #Displays the content of a selected log file after decrypting it
    txt_files = import_txt()
    
    if 0 < choice <= len(txt_files):
        filename = txt_files[choice - 1]
        directory = os.path.join(log_folder, filename)  # Changed to directory using os.path.join()

        with open(directory, 'r') as f:  # Changed to directory
            encrypted_content = f.read()

            decrypted_log = decrypt(encrypted_content)
            print(f"\t\tCurrent content of {filename}:")
            print(f'\t\t{decrypted_log}')
            input('\t\tPress ENTER to go back to the menu.')
    else:
        print(colored("\t\tInvalid selection.","red"))
        time.sleep(2)

def search_specific_log(user_search:str)->str: #Searches for a log file based on a user-provided date or title.
    txt_files = import_txt()

    match_found = False

    user_search = user_search.title() # Normalize the search query to title case to match title formatting

    for files in txt_files:
        
        file_to_read = os.path.join(log_folder, files) 
        
        file_names = files.split('.')[0]
        
        date, title = file_names.split('_')[0], file_names.split('_')[1]  # Split filename to extract date and title
   
      
        if user_search == date or user_search == title:
            match_found = True
            file_to_return = file_to_read

            with open(file_to_return, 'r') as f:
                encrypted_content = f.read()

            decrypted_log = decrypt(encrypted_content)
            print(f"\t\tCurrent content of {file_to_return}:")
            print(f'\t\t{decrypted_log}')
            input('\t\tPress ENTER to continue')
           
    if not match_found:
        print(colored(f"\t\tInvalid selection.\n\t\tThere is no log with the title or date {user_search}","red"))
        time.sleep(2)
        return None 

    return file_to_return

def delete_log(file_to_delete:str):  #Deletes a specified log file.
    
    file_path = os.path.join(log_folder, file_to_delete)
    print(colored(f"\t\tAre you sure you want to delete {file_to_delete}?", "red"),end='')
    confirm = input(' (Yes/No) ').lower()
    if confirm == 'yes':
        os.remove(file_path)
        time.sleep(1)
        print(colored('\t\tSUCCESS!', 'green'))
        time.sleep(1)
        print(f"\t\t{file_to_delete} has been deleted.")
        time.sleep(2)
    else:
        print("\n\t\tFile not deleted.")
        time.sleep(2)

def edit_log_content(choice:str):   #Opens an existing log for editing and saves the changes.
    print('success you made it here')
    time.sleep(1)
    filename = choice
    file_to_edit = os.path.join(log_folder, filename)

    with open(file_to_edit, 'r') as f:
        current_content = f.read()

    log_names = filename.split('.')[0]
    
    title_name = log_names.split('_')[1]

    decrypted_content = decrypt(current_content)
    the_log, title = open_input_window(decrypted_content,title=title_name)   

    

    the_content = f'{the_log}\n\nLast edited: {date_time}'
    
    encrypted_log = encrypt(the_content,encryption_key)     
    
    new_file_name = file_to_edit.split('.')[0] 
    file = f"{new_file_name}.txt"

    directory = os.path.join(log_folder, file)
    with open(directory, 'w') as f:
        f.write(encrypted_log)

    print(f'\n\t\tSaving the new version of "{filename}".....\n')
    time.sleep(1)
    print(colored('\t\tSuccess!','green'))
    time.sleep(1)
    print(f'\t\tThe new version of "{filename}" has been saved ')
    time.sleep(2)

def edit_log():  # Provides options to either edit or delete a log entry based on user choice.
    txt_files = import_txt()

    input_edit_delete = int(input('\t\tDo you want to edit or delete a log?\n\t\tPress (1) to delete\n\t\tPress (2) to edit\n\t\tPress (3) to return to menu\n\n\t\tAnswer here -> '))
    
    if input_edit_delete not in [1, 2, 3]:
        print(colored("\t\tInvalid selection!","red"))
        time.sleep(2)
        clear_terminal()
        print(colored('\t\tTRY AGAIN!\n'))
        return edit_log()
    if input_edit_delete == 3:
        print('\t\tGoing back to the menu')
        return True

    list_all_logs()

    log_choice = input("\n\t\tEnter the index number or the name of the file you want to modify.\n\n\t\t->   ").title()
    
    try:                                        # Attempt to convert user input into an integer
        int_choice = int(log_choice)
        file_to_edit = txt_files[int_choice - 1]
    
        if input_edit_delete == 1:
            delete_log(file_to_edit)
        elif input_edit_delete == 2:
            edit_log_content(file_to_edit)

    except:                                     # If conversion fails, treat input as a title or date
        file_to_edit = search_specific_log(log_choice)
        if file_to_edit is not None:
            if input_edit_delete == 1:
                delete_log(file_to_edit)
            elif input_edit_delete == 2:
                edit_log_content(file_to_edit)
        else:
            print(f'\t\tThere is no log with the title or date: {log_choice}')



password_guesses = 3

while password_guesses >0:   # Main execution loop for user authentication and menu navigation
    
    user_password = pyip.inputPassword(f'\n\t\tEnter your password to continue to the menu\t\tNumber of guesses left:{password_guesses}\n\n\t\t->  ',
        mask='*')    
    if user_password == password:

        while True:
            clear_terminal()
            print(colored('\t\tWelcome to your notebook!', 'blue'))
            print("\n\t\t\tMenu Options:")
            print(colored("\t\t1. Write a new log entry", "yellow"))
            print(colored("\t\t2. View existing log entries", "yellow"))
            print(colored("\t\t3. Edit or delete a log entry\n", "yellow"))
            print(colored("\t\t4. Exit", "red"))
            
            try: 
                menu_choice = int(input('\n\t\tEnter your choice here: -> '))
                if menu_choice not in range(1, 5):
                    raise ValueError("Menu choice is out of range.")
                
                if menu_choice == 1:
                    clear_terminal()
                    create_new_logs()
                    continue

                if menu_choice == 2:
                    clear_terminal()
                    list_all_logs()

                    user_input = input('\n\n\t\tEnter the name, date or index number\n\t\tof the log you want to read!\n\n\t\t->  ')
                    try:
                        is_number = int(user_input)
                        view_log(is_number)
                        time.sleep(1)
                        continue
                    except:
                        search_specific_log(user_input) 
                        time.sleep(1)
                        continue   

                if menu_choice == 3:
                    clear_terminal()
                    edit_log()
                    time.sleep(1)
                    continue

                if menu_choice == 4:
                    print("\t\tExiting program.")
                    password_guesses = -1
                    break  # Exit the loop and end the program

                else:
                    print(colored(f'\t\t{menu_choice} is out of range, there is only the menu options 1-4'),'red')
                    raise ValueError

            except ValueError as e:
                print(colored(f"\t\tError: {e}.Invalid input. Please enter a number.","red"))
                time.sleep(2)
    
    else:
        password_guesses -=1  # Decrement the guess count
        print(colored('\t\tIncorrect password, try again.', 'red'))

if password_guesses ==-1:
    print(colored('\t\tGoodbye','green'))
    time.sleep(3)
    

elif password_guesses == 0:
    print(colored('\t\tFuck off!', 'red'))
    time.sleep(3)
