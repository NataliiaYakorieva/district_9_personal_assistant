from colorama import init, Fore, Style

init(autoreset=True)

"""Module for colored console messages."""


def fail_message(text: str) -> str:
    """
    Return a failure message in red color.

    Args:
        text: The message to display.

    Returns:
        Colored string.
    """
    return Fore.RED + text + Style.RESET_ALL


def success_message(text: str) -> str:
    """
    Return a success message in green color.

    Args:
        text: The message to display.

    Returns:
        Colored string.
    """
    return Fore.GREEN + text + Style.RESET_ALL


def info_message(text: str) -> str:
    """
    Return an info message in cyan color.

    Args:
        text: The message to display.

    Returns:
        Colored string.
    """
    return Fore.CYAN + text + Style.RESET_ALL
