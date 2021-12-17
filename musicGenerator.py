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

    def generate(self) -> list:
        lilypondResult = []
        musescoreResult = []

        if(self.__configuration.lilypond):
            lilypondGenerator = LilyPondGenerator(
                self.__configuration, self.__helper)
            lilypondResult = [
                *lilypondGenerator.generateIntervalle(),
                *lilypondGenerator.generateNoten(),
                *lilypondGenerator.generateTonleiter()
            ]

        if (self.__configuration.musescore):
            museScoreGenerator = MuseScoreGenerator(
                self.__configuration, self.__helper)
            musescoreResult = [
                *museScoreGenerator.generateIntervalle(),
                *museScoreGenerator.generateNoten(),
                *museScoreGenerator.generateTonleiter()
            ]

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

# end class
