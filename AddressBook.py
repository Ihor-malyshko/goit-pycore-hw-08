from collections import UserDict
import datetime
from colorama import init, Fore

init()

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
		pass

class Birthday(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def validate(self, birthday):
        try:
            if isinstance(birthday, str):
                # Parse the date string in format DD.MM.YYYY
                datetime.datetime.strptime(birthday, "%d.%m.%Y")
            else:
                raise ValueError
        except ValueError:
            raise ValueError(f"{Fore.RED}Error{Fore.RESET}: Birthday must be in format DD.MM.YYYY")

class Phone(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)
    
    def validate(self, phone):
        if not (phone.isdigit() and len(phone) == 10):
            raise ValueError(f"{Fore.RED}Error{Fore.RESET}: короткий номер телефону має містити 10 цифр.")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # реалізація класу
    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
            return True
        except ValueError as e:
            print(e)
            return False
    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone {old_phone} not found in record.")
    def delete_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone {phone} not found in record.")
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def add_birthday(self, birthday):
        try:
            # Validate and store the birthday as a string
            self.birthday = Birthday(birthday)
            return True
        except ValueError as e:
            print(e)
            return False

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value if self.birthday else '---'}"

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        self.data[record.name.value] = record
        
    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            
    def get_upcoming_birthdays(self):
        today = datetime.datetime.today().date()
        upcoming = []
        
        for user in self.data.values():
            # Пропускаємо користувачів без дати народження
            if not user.birthday:
                continue
            try:
                birthday = datetime.datetime.strptime(user.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    continue
                if 0 <= (birthday_this_year - today).days < 7:
                    congratulation_date = birthday_this_year
                    if birthday_this_year.weekday() == 5:  # субота
                        congratulation_date = birthday_this_year + datetime.timedelta(days=2)
                    elif birthday_this_year.weekday() == 6:  # неділя
                        congratulation_date = birthday_this_year + datetime.timedelta(days=1)
                    
                    upcoming.append({
                        "name": user.name.value, 
                        "congratulation_date": congratulation_date.strftime("%d-%m-%Y"),
                        "birthday": user.birthday.value
                    })
                    
            except Exception as e:
                print(f"Error processing birthday for {user.name.value}: {e}")
        
        return upcoming
            
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values()) if self.data else "Address book is empty."