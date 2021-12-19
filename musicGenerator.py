from typing import Counter, List
import constants
from configuration import Configuration
from helper import Helper
from lilypondgenerator import LilyPondGenerator
from museScoreGenerator import MuseScoreGenerator


class MusicGenerator:

    #region private properties ################################################
    __helper: Helper
    __configuration: Configuration
    #endregion ################################################################

    #region public methods ####################################################

    def generate(self) -> List[List[str]]:
        lilypondResult = list()
        musescoreResult = list()

        if(self.__configuration.generateLilypond):
            lilypondGenerator = LilyPondGenerator(
                self.__configuration, self.__helper)
            lilypondResult = [
                *lilypondGenerator.generateIntervals(),
                *lilypondGenerator.generateNotes(),
                *lilypondGenerator.generateScales()
            ]

        if (self.__configuration.generateMusescore):
            museScoreGenerator = MuseScoreGenerator(
                self.__configuration, self.__helper)
            musescoreResult = [
                *museScoreGenerator.generateIntervals(),
                *museScoreGenerator.generateNotes(),
                *museScoreGenerator.generateScales()
            ]

        self.__dumpGenerationResults(
            lilypondResult, constants.keySkipped, 'Skipped {0} existing Lilypond file(s)')
        self.__dumpGenerationResults(
            lilypondResult, constants.keyLilipond, 'Generated {0} Lilypond file(s)')
        self.__dumpGenerationResults(
            musescoreResult, constants.keySkipped, 'Skipped {0} existing Musescore file(s)')
        self.__dumpGenerationResults(
            musescoreResult, constants.keyMusescore, 'Generated {0} Musescore file(s)')

        return [
            *lilypondResult,
            *musescoreResult
        ]
    # end generate

    #endregion ################################################################

    #region constructor #######################################################

    def __init__(self, configuration: Configuration, helper: Helper) -> None:
        self.__helper = helper
        self.__configuration = configuration
    # end constructor

    #endregion ################################################################

    #region private methods ###################################################
    def __dumpGenerationResults(self, listValue: list, filterValue: str, message: str) -> None:
        counter = list(
            filter(lambda lst: lst[0] == filterValue, listValue))
        if (len(counter) > 0):
            print(message.format(len(counter)))
    # end __dumpGenerationResults
    # endregion

# end class
