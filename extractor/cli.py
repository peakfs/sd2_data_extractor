import click
import pathlib


class Config(object):
    def __init__(self):
        self.is_verbose = False


config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True)
@config
def cli(config, verbose):

    if verbose:
        config.is_verbose = True


@cli.command()
@click.argument(
    'source',
    type=click.Path(
        exists=True,
        file_okay=False,
        readable=True,
        path_type=pathlib.Path
    )
)
@click.argument(
    'destination',
    type=click.Path(
        exists=True,
        file_okay=False,
        writable=True,
        path_type=pathlib.Path
    )
)
@config
def extract(config, source, destination):
    click.echo('hello')
    click.echo(config.is_verbose)
    click.echo(source.__repr__())
    click.echo(destination.__repr__())

@cli.command()
@click.argument(
    'source',
    type=click.Path(
        exists=True,
        file_okay=False,
        readable=True,
        path_type=pathlib.Path
    )
)
@config
def check_files(config, source):
    click.echo('checking files')
    click.echo(source.__repr__())
