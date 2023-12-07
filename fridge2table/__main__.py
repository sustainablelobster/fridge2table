"""Provides program entry point"""
import argparse

from . import create_app

arg_parser = argparse.ArgumentParser(prog="fridge2table")
arg_parser.add_argument(
    "--host",
    help="The hostname/IP address to listen on (default: localhost)",
    type=str,
    default="localhost",
)
arg_parser.add_argument(
    "--port", help="The port to listen on (default: 5000)", type=int, default=5000
)
args = arg_parser.parse_args()
create_app().run(host=args.host, port=args.port)
