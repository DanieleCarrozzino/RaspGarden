# Firebase mock-up project

## Instruction

to generate a json key to connect and intialize your firebase project you must to go here "https://console.firebase.google.com/project/smartgarden-d7604/settings/serviceaccounts/adminsdk" and "generate new private key" then take the .json and put it inside your project and define teh reference inside this little snippet code 

to run the script over the raspberry
```bash
pm2 start main.py --interpreter ./garden/bin/python
```

To see the logs run
```bash
pm2 logs 0
```
