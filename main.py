import click

@click.command()
@click.option('-h', '--help', is_flag=True, help='Show help')
def main(help):
    if help:
        print('Help message')
        return
    print('Hello, world!')

if __name__ == '__main__':
    main()