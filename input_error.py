from colorama import init, Fore
init()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return f"{Fore.RED}Error{Fore.RESET}: Enter the argument for the command."
        except KeyError:
            return f"{Fore.RED}Error{Fore.RESET}: Contact not found. Please check the name."
        except ValueError:
            return f"{Fore.RED}Error{Fore.RESET}: Enter the argument for the command."

    return inner