import os, sys, time
from colorama import Fore, Style, Back
# import emoji

def heading(text):
    BOLD = Style.BRIGHT
    BLUE = Fore.BLUE
    WHITE_BG = Back.WHITE
    RESET_COLOR = Style.RESET_ALL
    print(f"{BOLD}{BLUE}{WHITE_BG}🎧🔊{text}🔊🎧{RESET_COLOR}")

def subheading(text):
    BOLD = Style.BRIGHT
    CYAN = Fore.CYAN
    RESET_COLOR = Style.RESET_ALL
    print(f"{BOLD}{CYAN}{text}{RESET_COLOR}\n")

def error_message(msg):
    print(f"{Fore.RED}{msg}{Fore.RESET}")
    time.sleep(1)
    clear_prev_two_line()

def success_message(msg):
    print(f"{Fore.GREEN}{msg}{Fore.RESET}")
    time.sleep(1)

def clear_prev_line():
    print('\033[F\033[K', end='', flush=True)

def clear_prev_two_line():
    print('\033[F\033[K\033[F\033[K', end='', flush=True)

def check_quit(input_str):
    return input_str.lower() == "quit"