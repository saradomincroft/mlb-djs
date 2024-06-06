import os

def clear():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
        
def heading(text):
    print("*" * 30)
    print(text)
    print("*" * 30)
