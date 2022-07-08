import click
import inquirer
from os.path import expanduser
import os


class ShowBranchNameInTerminal:
    DEFAULT_COLOR = '1;33'
    FUNCTION_NAME = "git_branch_name_show"
    SHOW_BRANCH_NAME_FUNCTION = r"""
git_branch_name_show() {
  git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
"""

    def __init__(self):
        self.file_path = expanduser("~") + "/.bashrc"
        self.choice = ['Turn off', 'Change Color', 'Reset'] if self.show_branch() \
            else ['Turn on', 'Reset']
        self.action_message = "What do you want do?"
        self.color_message = "What color do you want to set?"
        self.enable_message = "Do you want to enable this extension?"
        self.color = {
            'grey': '1;30',
            'red': '1;31',
            'green': '1;32',
            'blue': '1;34',
            'purple': '1;35',
            'cyan': '1;36',
            'while': '1;37',
            'default': self.DEFAULT_COLOR,
        }

    def execute(self):
        questions = [
            inquirer.List('answer', message=self.action_message, choices=self.choice, ), ]
        command = inquirer.prompt(questions)
        if command['answer'] == self.choice[0]:
            self.turn_on() if "on" in self.choice[0] else self.turn_off()
        if command['answer'] == self.choice[1]:
            color_question = [inquirer.List('color_answer', message=self.color_message, choices=self.color.keys(), ), ]
            color = inquirer.prompt(color_question)
            self.change_color(self.color[color['color_answer']])
        if command['answer'] == "Reset":
            self.reset()
            enable_question = [inquirer.List('enable_answer', message=self.enable_message, choices=['Yes', 'No'], ), ]
            enable = inquirer.prompt(enable_question)
            self.turn_on() if enable['enable_answer'] == "Yes" else self.information()

    def change_color(self, color):
        with open(self.file_path, "r") as bashrc:
            readline = bashrc.readlines()
        with open(self.file_path, "w") as bashrc:
            for line in readline:
                if self.FUNCTION_NAME in line and "PS1" in line:
                    bashrc.write(self.set_color(color))
                else:
                    bashrc.write(line)
        os.system(". " + self.file_path)
        self.information()

    def turn_off(self):
        with open(self.file_path, "r") as bashrc:
            readline = bashrc.readlines()
        with open(self.file_path, "w") as bashrc:
            flags = True
            for line in readline:
                if self.FUNCTION_NAME in line:
                    flags = not flags
                    continue
                if flags:
                    bashrc.write(line)
        os.system(". " + self.file_path)
        self.information()

    def turn_on(self, color=DEFAULT_COLOR):
        with open(self.file_path, "a") as bashrc:
            bashrc.write(self.SHOW_BRANCH_NAME_FUNCTION)
            bashrc.write(self.set_color(color))
        os.system(". " + self.file_path)
        self.information()

    def set_color(self, color):
        return rf'export PS1="\e[1m\e[32m\u@\h\e[0m\e[0m:\e[1m\e[34m\w\e[0m\e[{color}m\$(git_branch_name_show)\e[0m\$ "'

    def information(self):
        click.echo(
            "Reset a terminal to show result or use command " + click.style(f"source {self.file_path}", fg='red'))

    def show_branch(self):
        with open(self.file_path) as bashrc:
            return self.FUNCTION_NAME in bashrc.read()

    def reset(self):
        os.system("cp /etc/skel/.bashrc ~/.bashrc")


def run():
    show_branch_name_in_terminal = ShowBranchNameInTerminal()
    show_branch_name_in_terminal.execute()
