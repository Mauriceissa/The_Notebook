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

def import_txt(folder) -> list: # Imports and returns a list of .txt files from the designated log directory.
    try:
        all_files = os.listdir(folder)
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

import os

def clear_terminal():
    # Function to clear the terminal/console screen
    os.system('cls' if os.name == 'nt' else 'clear')

def choose_or_create_folder(base_directory):
    # Ensure the base directory exists
    if not os.path.exists(base_directory):
        print(f"The directory '{base_directory}' does not exist.")
        return None

    while True:
        # List folders in the base directory
        folders = [f for f in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, f))]
        
        if folders:
            print("Folders in the directory:")
            for i, folder in enumerate(folders, 1):
                print(f"{i}. {folder}")
                
            print(f"{len(folders) + 1}. Create a new folder")
            print('Enter "DELETE" followed by folder name to delete a folder')
            
            # Prompt user to choose a folder or create a new one
            choice = input("Choose a folder by number (or create a new one): ")
            
            try:
                choice = int(choice)  # Convert input to integer if it's a number
            except:
                try:
                    if choice.startswith("DELETE "):
                        # Extract the folder name to delete
                        folder_name_to_delete = choice.split("DELETE ", 1)[1]
                        folder_path_to_delete = os.path.join(base_directory, folder_name_to_delete)
                        clear_terminal()
                        if os.path.exists(folder_path_to_delete) and os.path.isdir(folder_path_to_delete):
                            # List files in the folder to be deleted
                            files_in_folder = os.listdir(folder_path_to_delete)
                            print(f"These are the files in the folder '{folder_name_to_delete}':\n")
                            for file in files_in_folder:
                                print(f"\t- {file}")
                            # Confirm deletion
                            confirm_delete = input(f"\nAre you sure you want to delete the folder '{folder_name_to_delete}'? (yes/no): ")
                            if confirm_delete.lower() == 'yes':
                                # Delete all files in the folder and then the folder itself
                                for file in files_in_folder:
                                    os.remove(os.path.join(folder_path_to_delete, file))
                                os.rmdir(folder_path_to_delete)
                                clear_terminal()
                                print(f"Folder '{folder_name_to_delete}' deleted.")
                                time.sleep(2)
                            else:
                                print("Deletion canceled.")
                                time.sleep(2)
                        else:
                            print(f"Folder '{folder_name_to_delete}' does not exist.")
                        clear_terminal()
                        continue 
                        
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    time.sleep(2)
                    clear_terminal()
                continue
            
            # Handle the creation of a new folder
            if choice == len(folders) + 1:
                folder_name = input("Enter the name of the new folder: ")
                new_folder_path = os.path.join(base_directory, folder_name)
                
                if not os.path.exists(new_folder_path):
                    os.mkdir(new_folder_path)
                    print(f"Folder '{folder_name}' created.")
                    return new_folder_path
                else:
                    print(f"A folder named '{folder_name}' already exists. Please choose a different name.")
            else:
                # Return the chosen folder's path
                chosen_folder = folders[choice - 1]
                chosen_folder_path = os.path.join(base_directory, chosen_folder)
                return chosen_folder_path
        else:
            # Handle the case where no folders exist
            folder_name = input("No folders found. Enter the name of the new folder: ")
            new_folder_path = os.path.join(base_directory, folder_name)
            
            if not os.path.exists(new_folder_path):
                os.mkdir(new_folder_path)
                print(f"Folder '{folder_name}' created.")
                return new_folder_path
            else:
                print(f"A folder named '{folder_name}' already exists. Please choose a different name.")


def create_new_logs(folder):  #Handles the creation of new encrypted log entries.
    print(folder)
    
    the_log, title = open_input_window() 

    if the_log:
        encrypted_log = encrypt(f'{the_log}\n\nLast edited: {date_time}',encryption_key)   

        filename = f'{formatted_date}_{title}'
        the_file = f"{filename}.txt"

        directory = os.path.join(folder, the_file)
    
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

def list_all_logs(folder): 
       #Lists all .txt log files in the log directory.
    txt_files = import_txt(folder)
    if not txt_files:
        print("\t\tThere are no txt files in the current directory.")
        return
    
    print("\t\tList of all logs:\n")
    for index, filename in enumerate(txt_files):
       print(f"\t\t{index + 1}. {filename}:")

def view_log(choice:int, folder):  #Displays the content of a selected log file after decrypting it
    txt_files = import_txt(folder)
    
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

def search_specific_log(user_search:str, folder)->str: #Searches for a log file based on a user-provided date or title.
    txt_files = import_txt(folder)

    match_found = False

    for files in txt_files:
        
        file_to_read = os.path.join(folder, files) 
        
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

def delete_log(file_to_delete:str, folder):  #Deletes a specified log file.
    
    file_path = os.path.join(folder, file_to_delete)
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

def edit_log_content(choice:str,):   #Opens an existing log for editing and saves the changes.
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

def edit_log(folder):  # Provides options to either edit or delete a log entry based on user choice.
    txt_files = import_txt(folder)

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

    list_all_logs(folder)

    log_choice = input("\n\t\tEnter the index number or the name of the file you want to modify.\n\n\t\t->   ").title()
    
    try:                                        # Attempt to convert user input into an integer
        int_choice = int(log_choice)
        file_to_edit = txt_files[int_choice - 1]
    
        if input_edit_delete == 1:
            delete_log(file_to_edit, folder)
        elif input_edit_delete == 2:
            edit_log_content(file_to_edit)

    except:                                     # If conversion fails, treat input as a title or date
        file_to_edit = search_specific_log(log_choice,folder)
        if file_to_edit is not None:
            if input_edit_delete == 1:
                delete_log(file_to_edit, folder)
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
                    folder = choose_or_create_folder(log_folder)
                    print(folder)
                    create_new_logs(folder)
                    continue

                if menu_choice == 2:
                    clear_terminal()
                    folder = choose_or_create_folder(log_folder)
                    clear_terminal()
                    list_all_logs(folder)

                    user_input = input('\n\n\t\tEnter the name, date or index number\n\t\tof the log you want to read!\n\n\t\t->  ')
                    try:
                        is_number = int(user_input)
                        view_log(is_number,folder)
                        time.sleep(5)
                        continue
                    except:
                        search_specific_log(user_input,folder) 
                        time.sleep(1)
                        continue   

                if menu_choice == 3:
                    clear_terminal()
                    folder = choose_or_create_folder(log_folder)
                    clear_terminal()
                    edit_log(folder)
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
