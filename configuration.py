import os
import constants
import json
import pathlib
from argparse import Namespace


# TODO add a parameter to skip files that already exist
class Configuration:

    #region private properties ################################################
    __configuration: any
    __verbose: bool
    __outputDir: pathlib.Path
    __force: bool
    __generateLilypond: bool
    __generateMusescore: bool
    __process: bool
    __purge: bool
    __regenerate: bool
    __standardPitch: int
    #endregion ################################################################

    #region getters ###########################################################

    @property
    def generateLilypond(self) -> bool:
        return self.__generateLilypond
    # end get lilypond

    @property
    def lilypondExecutable(self) -> str:
        result = None
        if ('lilypond' in self.__configuration):
            result = self.__configuration['lilypond']
        # end if
        return result
    # end get lilypondExecutable

    @property
    def generateMusescore(self) -> bool:
        return self.__generateMusescore
    # end get musescore

    @property
    def musescoreExecutable(self) -> str:
        result = None
        if ('musescore' in self.__configuration):
            result = self.__configuration['musescore']
        # end if
        return result
    # end get musescoreExecutable

    @property
    def verbose(self) -> bool:
        return self.__verbose
    # end get verbose

    @property
    def rootOutput(self) -> str:
        return self.__outputDir.absolute()
    # end get outputDir

    @property
    def lilypondNotesDirectory(self) -> str:
        return '{0}/{1}/{2}'.format(
            self.rootOutput,
            self.__lilypondSubdirectory,
            self.__notesSubdirectory
        )
    # end get lilypondNoten

    @property
    def lilypondScalesDirectory(self) -> str:
        return '{0}/{1}/{2}'.format(
            self.rootOutput,
            self.__lilypondSubdirectory,
            self.__scalesSubdirectory
        )
    # end get lilypondTonleiter

    @property
    def lilypondIntervalsDirectory(self) -> str:
        return '{0}/{1}/{2}'.format(
            self.rootOutput,
            self.__lilypondSubdirectory,
            self.__intervalsSubdirectory
        )
    # end get lilypondIntervalle

    @property
    def musescoreNotesDirectory(self) -> str:
        return '{0}/{1}/{2}'.format(
            self.rootOutput,
            self.__musescoreSubdirectory,
            self.__notesSubdirectory
        )
    # end get musescoreNoten

    @property
    def musescoreScalesDirectory(self) -> str:
        return '{0}/{1}/{2}'.format(
            self.rootOutput,
            self.__musescoreSubdirectory,
            self.__scalesSubdirectory
        )
    # end get musescoreTonleiter

    @property
    def musescoreIntervalsDirectory(self) -> str:
        return '{0}/{1}/{2}'.format(
            self.rootOutput,
            self.__musescoreSubdirectory,
            self.__intervalsSubdirectory)
    # end get musescoreIntervalle

    @property
    def standardPitch(self) -> int:
        return self.__standardPitch
    # end get standardPitch

    @property
    def process(self) -> bool:
        return self.__process
    # end get

    @property
    def lilypondTemplate(self) -> str:
        result: str = 'template.ly'
        if ('templates' in self.__configuration):
            if ('lilypond' in self.__configuration['templates']):
                result = self.__configuration['templates']['lilypond']
            # end if
        # end if
        return result
    # end get lilypondTemplate(self)

    @property
    def musescoreTemplate(self) -> str:
        result: str = 'template.mscx'
        if ('templates' in self.__configuration):
            if ('musescore' in self.__configuration['templates']):
                result = self.__configuration['templates']['musescore']
            # end if
        # end if
        return result
    # end get lilypondTemplate(self)

    @property
    def regenerate(self) -> str:
        return self.__regenerate
    # end get regenerate

    #endregion ################################################################

    # region private getters
    @property
    def __outputRoot(self) -> str:
        result = 'out'
        if ('output' in self.__configuration):
            if ('root' in self.__configuration['output']):
                result = self.__configuration['output']['root']
        return result
    # end get __outputRoot

    @property
    def __lilypondSubdirectory(self) -> str:
        result = 'lilypond'
        if ('output' in self.__configuration):
            if ('lilypond' in self.__configuration['output']):
                result = self.__configuration['output']['lilypond']
        return result
    # end get __lilypondDir

    @property
    def __musescoreSubdirectory(self) -> str:
        result = 'musescore'
        if ('output' in self.__configuration):
            if ('musescore' in self.__configuration['output']):
                result = self.__configuration['output']['musescore']
        return result
    # end get __lilypondDir

    @property
    def __notesSubdirectory(self) -> str:
        result = 'notes'
        if ('output' in self.__configuration):
            if ('notes' in self.__configuration['output']):
                result = self.__configuration['output']['notes']
        return result
    # end get __lilypondDir

    @property
    def __scalesSubdirectory(self) -> str:
        result = 'scales'
        if ('output' in self.__configuration):
            if ('scales' in self.__configuration['output']):
                result = self.__configuration['output']['scales']
        return result
    # end get __lilypondDir

    @property
    def __intervalsSubdirectory(self) -> str:
        result = 'intervals'
        if ('output' in self.__configuration):
            if ('scales' in self.__configuration['output']):
                result = self.__configuration['output']['intervals']
        return result
    # end get __lilypondDir

    #endregion ################################################################

    #region public methods ####################################################

    def initialize(self, parsedArguments: Namespace) -> bool:
        self.__configuration = json.load(parsedArguments.config)
        return self.__setCommandLineToConfig(parsedArguments)
    # endregion

    #region constructor #######################################################
    def __init__(self) -> None:
        self.__purge = False
        self.__regenerate = False
        self.__standardPitch = None
    # end constructor

    #endregion ################################################################

    #region private methods ###################################################

    def __setCommandLineToConfig(self, parsedArguments: Namespace) -> bool:
        result = True
        for name, value in parsedArguments._get_kwargs():
            if (name == constants.argumentVerbose):
                self.__verbose = value
            elif (name == constants.argumentTarget):
                self.__generateLilypond = (value == constants.argumentTargetLilypond) or (
                    value == constants.argumentTargetAll)
                self.__generateMusescore = (value == constants.argumentTargetMusescore) or (
                    value == constants.argumentTargetAll)
            elif (name == constants.argumentOutputDir):
                self.__outputDir = value
            elif (name == constants.argumentForce):
                self.__force = value
            elif (name == constants.argumentToItem(constants.argumentGenerateOnly)):
                self.__process = not value
            elif (name == constants.argumentToItem(constants.argumentStandardPitch)):
                self.__standardPitch = value
            elif (name == constants.argumentRegenerate):
                self.__regenerate = value
            elif (name == constants.argumentPurge):
                self.__purge = value
        # end for

        if (self.__outputDir is None):
            if (self.verbose == True):
                print('No output dir on CLI, using value from configuration file')
            # end if
            self.__outputDir = pathlib.Path(self.__outputRoot)
        # end if

        if (self.__standardPitch is None):
            if ('standardPitch' in self.__configuration):
                self.__standardPitch = self.__configuration['standardPitch']
            else:
                self.__standardPitch = 443
        # end if

        if (self.verbose == True):
            print('Verbose                 : {0}'.format(self.verbose))
            print('Generate lilypond files : {0}'.format(
                self.generateLilypond))
            print('Generate musescore files: {0}'.format(
                self.generateMusescore))
            print('Outputdir               : {0}'.format(
                self.__outputDir.name))
            print('Process generated files : {0}'.format(self.process))
            print('Purge                   : {0}'.format(
                self.__purge))
            print('Lilypond executable     : {0}'.format(
                self.lilypondExecutable))
            print('Lilypond template       : {0}'.format(
                self.lilypondTemplate))
            print('Musescore executable    : {0}'.format(
                self.musescoreExecutable))
            print('Musescore template      : {0}'.format(
                self.musescoreTemplate))
            print('Standard pitch          : {0} Hz'.format(
                self.standardPitch))
        # end if verbose

        if (self.process == True):
            if (self.verbose == True):
                print('Checking executables')

            if (self.generateLilypond == True and self.process == True):
                if (self.lilypondExecutable is None):
                    print('lilypond executable is not set')
                    result = False
                elif (not pathlib.Path(self.lilypondExecutable).exists()):
                    print('Lilypond executable {0} not found'.format(
                        self.lilypondExecutable))
                    result = False
                # end if
            # end if

            if (self.generateMusescore == True and self.process == True):
                if (self.musescoreExecutable is None):
                    print('Musescore executable is not set')
                    result = False
                elif (not pathlib.Path(self.musescoreExecutable).exists()):
                    print('Musescore executable {0} not found'.format(
                        self.musescoreExecutable))
                    result = False
                # end if
            # end if
        # end if

        if (self.verbose == True):
            print('Validating output directory')
        # end if
        if (not self.__outputDir.exists()):
            if (not self.__force):
                print(
                    'Directory {0} does not exist. Please use the --force flag to create it.'.format(self.__outputDir.name))
                result = False
            elif (result == True):
                os.makedirs(self.__outputDir.absolute())
                if (self.verbose == True):
                    print('Created directory {0}'.format(
                        self.__outputDir.absolute()))
                result = True
            # end if-else
        elif (not self.__outputDir.is_dir()):
            print('{0} is not a directory.'.format(self.__outputDir.name))
            result = False
        # end if-elif

        if (self.verbose):
            print('Checking template files')

        if (self.generateLilypond == True and not os.path.exists(self.lilypondTemplate)):
            print('Lilypond template file \'{0}\' does not exist'.format(
                self.lilypondTemplate))
            result = False
        # end if

        if (self.generateMusescore == True and not os.path.exists(self.musescoreTemplate)):
            print('Musescore template file \'{0}\' does not exist'.format(
                self.musescoreTemplate))
            result = False
        # end if

        if (self.__purge == True):
            if (self.generateLilypond):
                self.__rmdir('{0}/{1}'.format(
                    self.rootOutput,
                    self.__lilypondSubdirectory))
            # end if
            if (self.generateMusescore):
                self.__rmdir('{0}/{1}'.format(
                    self.rootOutput,
                    self.__musescoreSubdirectory))
            # end if
        # end if

        if (self.verbose == True):
            print('Creating subdirectories')
        # end if

        if (self.generateLilypond):
            self.__createSubdirectories(
                [self.lilypondIntervalsDirectory, self.lilypondNotesDirectory, self.lilypondScalesDirectory])
        # end if

        if (self.generateMusescore):
            self.__createSubdirectories(
                [self.musescoreIntervalsDirectory, self.musescoreNotesDirectory, self.musescoreScalesDirectory])
        # end if

        return result
    # end __setCommandLineToConfig

    def __createSubdirectories(self, dirs: list) -> None:
        for dir in dirs:
            if (pathlib.Path(dir).exists()):
                if (self.verbose):
                    print('Subdirectory {0} already exists'.format(dir))
                # end if
            else:
                if (self.verbose):
                    print('Creating subdirectory {0}'.format(dir))
                # end if
                os.makedirs(dir)
            # end if
        # end for
    # end __createSubdirectories

    def __rmdir(self, directory) -> None:
        directory = pathlib.Path(directory)
        if (directory.exists()):
            for item in directory.iterdir():
                if item.is_dir():
                    self.__rmdir(item)
                else:
                    item.unlink()
            # end for
            directory.rmdir()
        #end if
    # end __rmdir

# end class
