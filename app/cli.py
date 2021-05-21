import click
from .dns_checker import DnsChecker
from .util import ClickOutput

@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

@cli.command()
@click.argument("hostname", required=True)
@click.option("-l", "--country", multiple=True, default=[])
@click.option("-c", "--dnsconfig", type=click.File("rb"), required=True)
@click.option("-t", "--record-type", default="A", type=click.Choice(DnsChecker.dns_types))
def check_hostname(hostname, country, dnsconfig, record_type):
    countries = []
    for country_item in country:
        countries = countries + country_item.split(",")
    countries = list(set(countries))
    countries.sort()
    dnschk = DnsChecker(dnsconfig, output=ClickOutput)
    dnschk.check_host(hostname=hostname, countries=countries, record_type=record_type)

if __name__ == "__main__":
    cli()