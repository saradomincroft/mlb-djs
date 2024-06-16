import os, sys
from colorama import Fore, Style, Back
# import emoji

def clear():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
        
def heading(text):
    BOLD = Style.BRIGHT
    BLUE = Fore.BLUE
    WHITE_BG = Back.WHITE
    RESET_COLOR = Style.RESET_ALL
    print("🎧" * 6)
    print(f"{BOLD}{BLUE}{WHITE_BG}{text}{RESET_COLOR}")
    print("📢" * 6)

def error_message(msg):
    print(f"{Fore.RED}{msg}{Fore.RESET}")

def success_message(msg):
    print(f"{Fore.GREEN}{msg}{Fore.RESET}")

def clear_prev_line():
    print('\033[F\033[K', end='', flush=True)

def clear_prev_two_line():
    print('\033[F\033[K\033[F\033[K', end='', flush=True)