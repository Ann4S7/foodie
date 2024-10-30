## Foodie
The project that prevents food waste.

### Description
The application allows you to add products to the database.\
Used products are removed from the database.

### Installation
Before running the program, you need to install several libraries. 
All of them are contained in the file requirements.txt.\
Use: `pip install -r requirements.txt`

### Tests
Before running the tests, you need to change the value of environment variable (ENV) to "TEST".\
Windows, PowerShell - command: `$Env:ENV="TEST"`\
Run the tests from root project folder.\
Use: `pytest .\tests`\
Instead of the above commands you can run the script in PowerShell: `.\scripts\run_tests.ps1`