import requests
import time
import os
from colorama import Fore, Style, init
from platform import system

# Initialize colorama
init(autoreset=True)

# Clear the terminal based on OS
def cls():
    if system() == 'Linux' or system() == 'Darwin':
        os.system('clear')
    elif system() == 'Windows':
        os.system('cls')

# Constants for colors and formatting
CLEAR_SCREEN = '\033[2J'
RED = '\033[1;31m'
RESET = '\033[0m'
BLUE = "\033[1;34m"
WHITE = "\033[1;37m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"
GREEN = "\033[1;32m"
BOLD = '\033[1;1m'

cls()
time.sleep(1)
os.system('clear')
logo = ("""
[1;70m██╗    ██╗ █████╗ ██╗     ███████╗███████╗██████╗ 
[1;70m██║    ██║██╔══██╗██║     ██╔════╝██╔════╝██╔══██╗
[1;91m██║ █╗ ██║███████║██║     █████╗  █████╗  ██║  ██║
[1;93m██║███╗██║██╔══██║██║     ██╔══╝  ██╔══╝  ██║  ██║
[1;80m╚███╔███╔╝██║  ██║███████╗███████╗███████╗██████╔╝
 [1;80m╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═════╝ 
 \033[1;33m<<═══════════════════════════════════════════════>>
\033[1;33m[*] \033[1;93m𝐎𝐖𝐍𝐄𝐑             \033[1;33m━▷ \033[1;93mWALEED XD            \033[1;33m[*]
\033[1;33m[*] \033[1;93m𝐆𝐈𝐓𝐇𝐔𝐁            \033[1;33m━▷ \033[1;93mWALEEDX4.0           \033[1;33m[*]
\033[1;33m[*] \033[1;93m𝐑𝐔𝐋𝐄𝐗             \033[1;33m━▷ \033[1;93mWALEED 𝙓𝘿 007        \033[1;33m[*]
\033[1;33m[*] \033[1;93m𝐓𝐎𝐎𝐋              \033[1;33m━▷ \033[1;93m𝐓𝐎𝐊𝐄𝐍 𝐂𝐇𝐄𝐂𝐊𝐄𝐑        \033[1;33m[*]
\033[1;33m[*] \033[1;93m𝐅𝐀𝐂𝐄𝐁𝐎𝐊           \033[1;33m━▷ \033[1;93mWALEEDXD             \033[1;33m[*]
\033[1;33m<<═══════════════════════════════════════════════>>

""" )
# Print the logo
print(Fore. CYAN + logo +  Style.RESET_ALL)

# Start time
print('\u001b[37m' + '\x1b[1;37m======================================================>>')
print("\033[92mStart Time:", time.strftime("%Y-%m-%d %H:%M:%S"))
print('\u001b[37m' + '\x1b[1;37m======================================================>>')

# Function to check a single token
def check_single_token(token):
    url = f'https://graph.facebook.com/me?access_token={token}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            user_id = data.get('id')
            name = data.get('name')
            email = data.get('email', 'Email not available')

            result = (
                f"{CYAN}[+] User ID: {user_id}\n"
                f"{CYAN}[+] Name: {name}\n"
                f"{CYAN}[+] Email: {email}\n"
                f"{CYAN}[+] Token Valid: Yes{RESET}\n"
            )
            print(result)
            save_result(result)
            save_valid_token(token, user_id, name, email)  # Save valid token details
            return True
        else:
            result = f"{RED}[+] Error: {response.status_code}\n[+] Token Expired or Invalid{RESET}"
            print(result)
            save_result(result)
            return False
    except requests.exceptions.RequestException as e:
        result = f"{RED}[+] Network Error: {e}{RESET}"
        print(result)
        save_result(result)
        return False

# Function to check tokens from a file
def check_tokens_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            tokens = file.read().splitlines()

        total_tokens = len(tokens)
        valid_tokens = 0
        print(f"{MAGENTA}[+] Total tokens to check: {total_tokens}{RESET}")

        for index, token in enumerate(tokens, start=1):
            print(f"\n{CYAN}[+] Checking Token {index}/{total_tokens}: {token[:10]}...{RESET}")
            if check_single_token(token):
                valid_tokens += 1
            time.sleep(1)  # Rate limiting to avoid API limits

        print(f"\n{GREEN}[+] Total valid tokens: {valid_tokens}/{total_tokens}{RESET}")
    except FileNotFoundError:
        print(f"{RED}[+] Error: File not found at {file_path}{RESET}")
    except Exception as e:
        print(f"{RED}[+] Error: {e}{RESET}")

# Function to get Facebook Page Access Token
def get_page_token(user_token):
    url = f'https://graph.facebook.com/v19.0/me/accounts?fields=access_token,name,id&access_token={user_token}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pages = data.get('data', [])
            if not pages:
                print(f"{RED}[+] No pages found for this user.{RESET}")
                return

            print(f"{CYAN}[+] Pages managed by this user:{RESET}")
            for index, page in enumerate(pages, start=1):
                print(f"{CYAN}[{index}] Page Name: {page.get('name')}")
                print(f"{CYAN}[{2}] Page ID: {page.get('id')}")
                print(f"{CYAN}[{3}] Page Token: {page.get('access_token')}{RESET}")

            # Save page tokens to a file
            with open("page_tokens.txt", "a") as file:
                for page in pages:
                    file.write(
                        f"Page Name: {page.get('name')}\n"
                        f"Page ID: {page.get('id')}\n"
                        f"Page Access Token: {page.get('access_token')}\n"
                        f"{'-' * 40}\n"
                    )
            print(f"{GREEN}[+] Page tokens saved to 'page_tokens.txt'.{RESET}")
        else:
            print(f"{RED}[+] Error: {response.status_code}\n[+] Failed to retrieve page tokens.{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}[+] Network Error: {e}{RESET}")

# Function to save results to a file
def save_result(result):
    with open("results.txt", "a") as file:
        file.write(result + "\n\n")

# Function to save valid tokens and their details
def save_valid_token(token, user_id, name, email):
    with open("valid_tokens.txt", "a") as file:
        file.write(
            f"Token: {token}\n"
            f"User ID: {user_id}\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"{'-' * 40}\n"
        )

# Main function
def main():
    cls()
    print(logo)
    print(f"{YELLOW}\n[1] Check Single Token")
    print(f"{YELLOW}\n[2] Check Tokens from File")
    print(f"{YELLOW}\n[3] Get Facebook Page Access Token{RESET}")
    choice = input(f"{WHITE}\n[+] Enter your choice (1, 2, or 3): {RESET}")

    if choice == '1':
        token = input(f"{CYAN}[+] Enter the token to check: {RESET}")
        check_single_token(token)
    elif choice == '2':
        file_path = input(f"{CYAN}[+] Enter the file path (e.g., tokens.txt): {RESET}")
        check_tokens_from_file(file_path)
    elif choice == '3':
        user_token = input(f"{CYAN}[+] Enter your Facebook User Access Token: {RESET}")
        get_page_token(user_token)
    else:
        print(f"{RED}[+] Invalid choice! Please select 1, 2, or 3.{RESET}")

if __name__ == "__main__":
    main()