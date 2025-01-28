import datetime

class logger:

    def __init__(self) -> None:
        self.filename = "log.txt"
        pass

    def d(self, text):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        text_to_print = f"{current_time} | {text}" 
        print(text_to_print)
        with open(self.filename, 'a') as file:
            # Write text to the file
            file.write(f"{text_to_print}\n")