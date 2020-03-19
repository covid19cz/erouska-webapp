import bcrypt
import click
from app.db.sql.models.handler import Handler
from app.db.sql.session import Session


def add_handler(username, password):
    session = Session()
    handler = Handler(username=username,
                      password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
    session.add(handler)
    session.commit()
    session.close()


@click.command("add-handler")
@click.argument("username")
@click.argument("password")
def add_handler_cmd(username, password):
    add_handler(username, password)


@click.group()
def cli():
    pass


if __name__ == "__main__":
    cli.add_command(add_handler_cmd)
    cli()
