from colorama import init, Fore, Style

init(autoreset=True)

"""Module for colored console messages."""


def fail_message(text):
    return Fore.RED + text + Style.RESET_ALL


def success_message(text):
    return Fore.GREEN + text + Style.RESET_ALL


def info_message(text):
    return Fore.CYAN + text + Style.RESET_ALL
