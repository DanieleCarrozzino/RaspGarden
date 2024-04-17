import datetime

class logger:

    def __init__(self) -> None:
        self.filename = "log.txt"
        pass

    def d(self, text):
        print(text)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(self.filename, 'a') as file:
            # Write text to the file
            file.write(f"{current_time} | {text}\n")