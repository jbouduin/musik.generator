import os
import constants
import json
import pathlib
from argparse import Namespace

# TODO add CLI parameter outputdir to config.json and merge CLI args with config
# TODO add a parameter for the standardpicht, default = 443
# TODO add a parameter to skip files that already exist
class Configuration:

    #region private properties ################################################
    __configuration: any
    __verbose: bool
    __outputDir: pathlib.Path
    __force: bool
    __lilypond: bool
    __musescore: bool
    __process: bool
    __standardPitch: int
    # TODO output subdir's should go into config.json + CLI args
    __lilypondDir = 'lilypond'
    __musescoreDir = 'musescore'
    __notenDir = 'noten'
    __tonleiterdir = 'tonleiter'
    __intervalledir = 'intervalle'
    #endregion ################################################################

    #region getters ###########################################################

    @property
    def lilypond(self) -> bool:
        return self.__lilypond
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
    def musescore(self) -> bool:
        return self.__musescore
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
    def lilypondNoten(self) -> str:
        return '{0}/{1}/{2}'.format(self.rootOutput, self.__lilypondDir, self.__notenDir)
    # end get lilypondNoten

    @property
    def lilypondTonleiter(self) -> str:
        return '{0}/{1}/{2}'.format(self.rootOutput, self.__lilypondDir, self.__tonleiterdir)
    # end get lilypondTonleiter

    @property
    def lilypondIntervalle(self) -> str:
        return '{0}/{1}/{2}'.format(self.rootOutput, self.__lilypondDir, self.__intervalledir)
    # end get lilypondIntervalle

    @property
    def musescoreNoten(self) -> str:
        return '{0}/{1}/{2}'.format(self.rootOutput, self.__musescoreDir, self.__notenDir)
    # end get musescoreNoten

    @property
    def musescoreTonleiter(self) -> str:
        return '{0}/{1}/{2}'.format(self.rootOutput, self.__musescoreDir, self.__tonleiterdir)
    # end get musescoreTonleiter

    @property
    def musescoreIntervalle(self) -> str:
        return '{0}/{1}/{2}'.format(self.rootOutput, self.__musescoreDir, self.__intervalledir)
    # end get musescoreIntervalle

    @property
    def standardPitch(self) -> int:
        return self.__standardPitch
    #end get standardPitch

    @property
    def process(self) -> bool:
        return self.__process
    # end get

    #endregion ################################################################

    #region public methods ####################################################

    def initialize(self, parsedArguments: Namespace) -> bool:
        self.__configuration = json.load(parsedArguments.config)
        return self.__setCommandLineToConfig(parsedArguments)
    # endregion

    #region constructor #######################################################

    # end constructor

    #endregion ################################################################

    #region private methods ###################################################

    def __setCommandLineToConfig(self, parsedArguments: Namespace) -> bool:
        result = True
        for name, value in parsedArguments._get_kwargs():
            if (name == constants.argumentVerbose):
                self.__verbose = value
            elif (name == constants.argumentTarget):
                self.__lilypond = (value == constants.argumentTargetLilypond) or (
                    value == constants.argumentTargetAll)
                self.__musescore = (value == constants.argumentTargetMusescore) or (
                    value == constants.argumentTargetAll)
            elif (name == constants.argumentOutputDir):
                self.__outputDir = value
            elif (name == constants.argumentForce):
                self.__force = value
            elif (name == constants.argumentToItem(constants.argumentGenerateOnly)):
                self.__process = not value
            elif (name == constants.argumentToItem(constants.argumentStandardPitch)):
                self.__standardPitch = value
        # end for

        if (self.verbose == True):
            print('Verbose                 : {0}'.format(self.verbose))
            print('Generate lilypond files : {0}'.format(self.lilypond))
            print('Generate musescore files: {0}'.format(self.musescore))
            print('Outputdir               : {0}'.format(
                self.__outputDir.name))
            print('Process generated files : {0}'.format(self.process))
            print('Lilypond executable     : {0}'.format(
                self.lilypondExecutable))
            print('Musescore executable    : {0}'.format(
                self.musescoreExecutable))
            print('Standard pitch          : {0} Hz.'.format(
                self.standardPitch))
        # end if verbose

        if (self.process == True):
            if (self.verbose == True):
                print('Checking executables')

            if (self.lilypond == True and self.process == True):
                if (self.lilypondExecutable is None):
                    print('lilypond executable is not set')
                    result = False
                elif (not pathlib.Path(self.lilypondExecutable).exists()):
                    print('Lilypond executable {0} not found'.format(
                        self.lilypondExecutable))
                    result = False
                # end if
            # end if

            if (self.musescore == True and self.process == True):
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
            print('Creating subdirectories')
        # end if

        if (self.lilypond):
            self.__createSubdirectories(
                [self.lilypondIntervalle, self.lilypondNoten, self.lilypondTonleiter])
        # end if

        if (self.musescore):
            self.__createSubdirectories(
                [self.musescoreIntervalle, self.musescoreNoten, self.musescoreTonleiter])
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

    # endregion
# end class
