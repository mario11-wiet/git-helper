import sys
import inquirer

from Configurate.show_branch_name_in_terminal import run

questions = [inquirer.List('command', message="What do you want do?", choices=['Configurate', "Information","add"], ), ]
command = inquirer.prompt(questions)

if command['command'] == 'Configurate':
    run()

if command['command'] == "add":
    questions1 = [
        inquirer.List('command1', message="Which file do you want add?", choices=['all', "mk.py", "siema.bats"], ), ]
    command1 = inquirer.prompt(questions1)