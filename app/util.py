class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
import click

class Output:
    @staticmethod
    def info(message):
        print(message)
    
    @staticmethod
    def debug(message):
        print(message)

    @staticmethod
    def error(message):
        print(message)

class ClickOutput(Output):
    @staticmethod
    def info(message):
        click.echo(click.style(message, fg="white"))

    @staticmethod
    def success(message):
        click.echo(click.style(message, fg="green"))
    
    @staticmethod
    def debug(message):
        click.echo(click.style(message, fg="blue"))

    @staticmethod
    def error(message):
        click.echo(click.style(message, fg="red"))
