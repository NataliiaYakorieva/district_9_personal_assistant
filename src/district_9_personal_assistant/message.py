from colorama import init, Fore, Style

init(autoreset=True)


def fail_message(text):
    return Fore.RED + text + Style.RESET_ALL


def success_message(text):
    return Fore.GREEN + text + Style.RESET_ALL
