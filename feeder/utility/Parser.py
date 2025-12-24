import argparse
from argparse import Namespace

from utility.Logger import Logger


class Parser:
    __logger = Logger.get_logger()
    __parser = argparse.ArgumentParser()

    @classmethod
    def get_origin_trigger(cls):
        """Method to decide whether to fetch from origin or not default true"""
        arguments = cls.__parse_arguments()
        if arguments.fetch_from_origin:
            return arguments.fetch_from_origin == 'true'
        else:
            cls.__logger.info("no arguments provided. defaulting to fetch_from_origin = true")
        return True

    @classmethod
    def __parse_arguments(cls) -> Namespace:
        """Method to parse arguments from commandline"""
        cls.__logger.info("parsing arguments from commandline")
        cls.__parser.add_argument('-fo', '--fetch_from_origin',  metavar='',  help='enable or disable fetching data from origin(polygon.io)')
        arguments = cls.__parser.parse_args()
        return arguments