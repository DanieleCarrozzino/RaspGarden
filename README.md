# Firebase mock-up project

## Instruction

to generate a json key to connect and intialize your firebase project you must to go here "https://console.firebase.google.com/project/smartgarden-d7604/settings/serviceaccounts/adminsdk" and "generate new private key" then take the .json and put it inside your project and define teh reference inside this little snippet code 

var admin = require("firebase-admin");

var serviceAccount = require("path/to/serviceAccountKey.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://smartgarden-d7604-default-rtdb.europe-west1.firebasedatabase.app"
});


to run the script, activate the env with source garden_env/bin/activate