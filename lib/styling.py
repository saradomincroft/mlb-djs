import os, sys
from colorama import Fore, Style

def clear():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
        
def heading(text):
    print("*" * 30)
    print(text)
    print("*" * 30)

def error_message(msg):
    print(f"{Fore.RED}{msg}{Fore.RESET}")

def success_message(msg):
    print(f"{Fore.GREEN}{msg}{Fore.RESET}")

def clear_prev_line():
    print('\033[F\033[K', end='', flush=True)

def clear_prev_two_line():
    print('\033[F\033[K\033[F\033[K', end='', flush=True)