import pickle
from colorama import init, Fore
from input_error import input_error
from AddressBook import AddressBook, Record
from deepdiff import DeepDiff

init()

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def parse_input():
    user_input = input("Enter a command: ")
    # Handle empty input
    if not user_input.strip():
        print(f"{Fore.RED}Error{Fore.RESET}: Empty input. Please enter a command.")
        return None, []
    
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args
    except Exception:
        print(f"{Fore.RED}Error{Fore.RESET}: Invalid command format.")
        return None, []
  
@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = f"{Fore.YELLOW}updated{Fore.RESET}"
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"{Fore.GREEN}added{Fore.RESET}"
    if phone:
        record.add_phone(phone)
    return f"Contact {message}."

@input_error
def change_contact(args, book):
    name = args[0]
    phone = args[1]
    new_phone = args[2]
    record = book.find(name)
    if record is None:
        return f"{Fore.RED}Error{Fore.RESET}: Contact '{name}' not found."
    try:
        record.edit_phone(phone, new_phone)
    except ValueError as e:
        return str(e)
    return f"Contact '{name}' {Fore.YELLOW}updated{Fore.RESET} to {new_phone}."

@input_error
def delete_contact(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        return f"{Fore.RED}Error{Fore.RESET}: Contact '{name}' not found."
    else:
        book.delete(name)
        return f"Contact '{name}' {Fore.MAGENTA}deleted{Fore.RESET}."

@input_error
def show_contact(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        return f"{Fore.RED}Error{Fore.RESET}: Contact '{name}' not found."
    return f"{Fore.BLUE}{name}{Fore.RESET}: {record}"

@input_error
def add_birthday(args, book):
    name = args[0]
    birthday = args[1]
    record = book.find(name)
    if record is None:
        return f"{Fore.RED}Error{Fore.RESET}: Contact '{name}' not found."
    record.add_birthday(birthday)
    return f"Birthday for {name} {Fore.GREEN}added{Fore.RESET}."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        return f"{Fore.RED}Error{Fore.RESET}: Contact '{name}' not found."
    if record.birthday is None:
        return f"{Fore.YELLOW}No birthday set for {name}.{Fore.RESET}"
    return f"{Fore.BLUE}{name}{Fore.RESET}'s birthday: {record.birthday.value}"

@input_error
def birthdays(book):
    return book.get_upcoming_birthdays()


def show_contacts(book):
    return f'{Fore.BLUE}{"="*10} Book {"="*10}{Fore.RESET}\n{book}\n{Fore.BLUE}{"="*10} end {"="*10}{Fore.RESET}'


def main():
    print("Welcome to the assistant bot!")
    # read file
    # book = AddressBook()
    book = load_data()
    print(show_contacts(book))
    while True:
        command, args = parse_input()
        
        if command is None:
            continue
            
        if command in ["close", "exit"]:
            # save contacts
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "phone":
            print(show_contact(args, book))
        elif command == "all":
            print(show_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


def test_bot(type="test"):
    # Test the bot functionality
    book = AddressBook()
    if type == "test":
      print(f"{Fore.CYAN}Test 1{Fore.RESET} first contact")
      
    add_contact(["Alice", "1234567890"], book)
    show_contacts(book)
    add_birthday(["Alice", "09.07.2000"], book)
    add_contact(["Alice", "5555555555"], book)
    change_contact(["Alice", "5555555555", '2222222222'], book)
    
    if type == "test":
      print(f"{Fore.CYAN}Test 2{Fore.RESET} second and third contact")
    add_contact(["Bob", "1111111111"], book)
    add_birthday(["Bob", "12.07.2000"], book)
    add_contact(["Tom", "2222222222"], book)
    add_birthday(["Tom", "13.07.2000"], book)
    show_contacts(book)
    
    if type == "test":
      print(f"{Fore.CYAN}Test 3{Fore.RESET} birthday show")
    add_contact(["15-07", "3333333333"], book)
    add_birthday(["15-07", "15.07.2000"], book)
    add_contact(["19-07", "4444444444"], book)
    add_birthday(["19-07", "19.07.2000"], book)
    if type == "test":
      print(birthdays(book))

    if type == "test":
      print(f"{Fore.CYAN}Test 4{Fore.RESET} delete contact")
      delete_contact(["Alice"], book)
    
    if type == "test":
      # update the file with test book data
      # save_data(book, "test_data.pkl")
      
      # Test data loading from file
      loaded_book = load_data("test_data.pkl")
      diff = DeepDiff(book.data, loaded_book.data, ignore_order=True)
      if not diff:
        print(f"{Fore.GREEN}All tests passed.{Fore.RESET}")
      else:
        print(f"{Fore.RED}File test failed.{Fore.RESET}")
        print(f"Differences: {diff}")
    
    return book
    
def test_file():
    # використаемо функцію test_bot для генерації даних
    book = test_bot('generate book')
    # Test file saving and loading
    print(f"{Fore.CYAN}Test 5{Fore.RESET} save and load")
    save_data(book, "test_book.pkl")

    loaded_book = load_data("test_book.pkl")
    # Використання DeepDiff для глибокого порівняння
    diff = DeepDiff(book.data, loaded_book.data, ignore_order=True)
    if not diff:
        print(f"{Fore.GREEN}File test passed.{Fore.RESET}")
    else:
        print(f"{Fore.RED}File test failed.{Fore.RESET}")
        print(f"Differences: {diff}")

if __name__ == "__main__":
    test_bot()
    test_file()
    main()