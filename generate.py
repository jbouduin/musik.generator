import argparse
import pathlib
import constants

from configuration import Configuration
from helper import Helper
from fileProcessor import FileProcessor
from musicGenerator import MusicGenerator


def __buildArgumentParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Generate and process lilypond and musescore files.')

    # use an alternative config file
    parser.add_argument(
        '--config', '-c',
        type=open,
        default='config.json',
        help='The name of the configuration file. [Default = \'json.config\']')

    # positional argument: what to generate musescore files
    parser.add_argument(
        '{0}'.format(constants.argumentTarget),
        choices=['all', 'musescore', 'lilypond'],
        help='Type of files to generate'
    )

    # skip converting files
    parser.add_argument(
        '--{0}'.format(constants.argumentGenerateOnly), '-g',
        action='store_true',
        help='Do not process generated files'
    )

    # output directory
    parser.add_argument(
        '--{0}'.format(constants.argumentOutputDir), '-o',
        type=pathlib.Path,
        help='The output directory. If not provided reading the value from the configuratiomn file. [Default = \'.\out\']'
    )

    # skip converting files
    parser.add_argument(
        '--{0}'.format(constants.argumentForce), '-f',
        action='store_true',
        help='Force creation of the output directory if it does not exist'
    )

    # standard picht (Kammerton)
    parser.add_argument(
        '--{0}'.format(constants.argumentStandardPitch), '-s',
        type=int,
        default=443,
        help='The standard pitch (a.k.a. Kammerton) when generating mp3-files. [Default = 443]'
    )

    # verbose
    parser.add_argument(
        '--{0}'.format(constants.argumentVerbose), '-v',
        action='store_true',
        help='Verbose'
    )

    # TODO add selection noten, tonleiter, intervalle
    return parser

# end __setupArgParser


def main():
    parsed: argparse.Namespace = None
    parser = __buildArgumentParser()
    configOk = False
    try:
        parsed = parser.parse_args()
        config = Configuration()
        configOk = config.initialize(parsed)
        if (configOk != True):
            parser.print_usage()
        # end if
    except OSError as err:
        parser.print_usage()
        print('{0}: error: {1}: {2}'.format(parser.prog, err.strerror, err.filename))
    finally:
        if (parsed is not None and parsed.config is not None):
            parsed.config.close()
    #end try-except-finally

    if (configOk == True):
        try:
            helper = Helper()
            files = MusicGenerator(config, helper).generate()
            if (config.process):
                FileProcessor(config).processFiles(files)
        except BaseException as err:
            print(err)
        #end try except
    #end if
# end main


if __name__ == '__main__':
    main()
    exit(0)
