import click

from collect.service import collect_sales


@click.command('collect')
@click.option('--email', type=click.STRING, required=True)
@click.option('--password', type=click.STRING, required=True)
def collect(email: str, password: str):
    collect_sales(email, password)


if __name__ == '__main__':
    collect()
