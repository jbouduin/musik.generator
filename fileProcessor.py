import os
import sys
import subprocess

from configuration import Configuration

# TODO parameterized (default: false) delete of ly and mscx files after processing them
class FileProcessor:

    #region private properties ################################################

    __config: Configuration

    #endregion ################################################################

    #region public methods ####################################################

    def processFiles(self, files: list) -> None:
        if (self.__config.lilypondExecutable is not None):
            self.__processLilyFiles(list(
                filter(lambda lst: lst[0] == 'Lilypond', files)))
        # end if
        if (self.__config.musescoreExecutable is not None):
            self.__processMuseFiles(list(
                filter(lambda lst: lst[0] == 'Musescore', files)))
    # end processFiles

    #endregion ################################################################

    #region constructor #######################################################

    def __init__(self, config: Configuration) -> None:
        self.__config = config
    # end constructor

    #endregion ################################################################

    #region private methods ###################################################

    def __returnCodeToString(self, code: int) -> str:
        result: str
        if (code == 0):
            result = 'OK'
        else:
            result = 'ERROR'
        return result
    # end returnCodeToString

    def __processLilyFiles(self, files: list) -> None:
        for f in files:
            print('Processing {0}-file {1}'.format(f[0], f[1]), end=' ')
            # check if it works without this f[1] = f[1].replace('\\', '/')
            finished = subprocess.run(
                [self.__config.lilypondExecutable, '-o', os.path.dirname(f[1]), f[1]], capture_output=True)
            print('->', self.__returnCodeToString(finished.returncode))
            if (finished.returncode != 0):
                print(finished.stderr)
                print(finished.stdout)
            #end if
            if (self.__config.verbose and finished.returncode == 0):
                print(finished.stdout)
            #end if
            pdfFile = f[1].replace(".ly", ".pdf")
            self.__deleteFile(pdfFile)
            croppedPdfFile = f[1].replace(".ly", ".cropped.pdf")
            self.__deleteFile(croppedPdfFile)
        # end for
    # end processLilyFiles

    def __processMuseFiles(self, files: list) -> None:
        for f in files:
            print('Processing {0}-file {1}'.format(f[0], f[1]), end=' ')
            mp3 = f[1].replace('\\', '/').replace('mscx', 'mp3')
            sys.stdout.flush()
            # leider funktioniert 'musescore -j' nicht wenn es aus python gestartet wird
            # also machen wir eine nach dem anderen
            finished = subprocess.run(
                [self.__config.musescoreExecutable, '-o', mp3, f[1]])
            print('->', self.__returnCodeToString(finished.returncode))
            if (self.__config.verbose):
                print(finished.stdout)
        # end for
    # end processMuseFiles

    def __deleteFile(self, filename: str):
        if (self.__config.verbose):
            print('Deleting {0}'.format(filename))
        #end if
        try:
            os.remove(filename)
        except OSError as err:
            print('Error deleting {0}'.format(filename))
            print(err)
        if (self.__config.verbose):
            print('{0} deleted'.format(filename))
        #end if
    #end deleteFile
    #endregion ################################################################

# end class
