from firebase_admin import messaging
from configuration import reader_conf as reader
from firebase import main_firebase as firebase

class Messaging:

    def __init__(self) -> None:
        # init firebase
        firebase.initialize_firebase()

        self.reader = reader.ConfReader() 
        pass

    def sendMessage(self, title, body, tokens):
        for token in tokens:
            # Message data
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                token=token,
            )


            # Send the message
            response = messaging.send(message)
            print('Message response:', response)
        pass

'''
    def sendMessage(self, title, body):

        for token in self.reader.get_tokens():
            # Message data
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                token=token,
            )


            # Send the message
            response = messaging.send(message)
            print('Message response:', response)
        pass
'''

