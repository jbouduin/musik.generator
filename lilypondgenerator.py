import pathlib
from typing import List

from configuration import Configuration
import constants
from helper import Helper
from lilypondLy import LilypondLy


class LilyPondGenerator:

    #region private properties ################################################
    __config: Configuration
    __helper: Helper
    #endregion ################################################################

    #region public methods ####################################################

    def generateIntervals(self) -> List[List[str]]:
        result = list()
        for scale in ['G', 'C', 'D', 'A', 'E']:
            intervals = self.__helper.generateMajorIntervals(scale)
            for interval in intervals:
                title = self.__helper.getIntervalTitle(interval[0], scale)
                generatedFile = '{0}/{1}.ly'.format(
                    self.__config.lilypondIntervalsDirectory,
                    title.replace(' ', '-')).lower()
                if (pathlib.Path(generatedFile).exists() == False or self.__config.regenerate == True):
                    lyFile = LilypondLy(self.__config, scale, True, '9/8')
                    lyFile.setTitle(title)
                    lyFile.makeMoment = '1/8'
                    lyFile.addNotes(
                        ['{0}2 r8 {1}2 |'.format(interval[1], interval[2])])
                    lyFile.addLyrics(['{0} {1}'.format(self.__helper.getGermanNotation(
                        interval[1], True), self.__helper.getGermanNotation(interval[2], True))])


                    lyFile.writeToFile(generatedFile)
                    result.append([constants.keyLilipond, generatedFile])
                else:
                    result.append([constants.keySkipped, generatedFile])
            # end for
        # end for
        return result
    # end generateIntervals

    def generateNotes(self) -> List[List[str]]:
        result = list()
        allNotes = self.__helper.getAllViolinNotes()
        for notes in allNotes:
            title = self.__helper.getNoteTitle(notes)
            generatedFile = '{0}/{1}.ly'.format(
                self.__config.lilypondNotesDirectory,
                title.replace(' ', '-')).lower()
            if (pathlib.Path(generatedFile).exists() == False or self.__config.regenerate == True):
                lyFile = LilypondLy(self.__config, 'C', True, '4/4')
                lyFile.setTitle(title)
                if (len(notes) == 2):
                    lyFile.makeMoment = '1/8'
                else:
                    lyFile.makeMoment = '1'
                # end if-else

                for note in notes:
                    noteLength = ''
                    if (len(notes) == 2):
                        noteLength = 2
                    else:
                        noteLength = 1
                    # end if-else
                    lyFile.addNotes(['{0}{1}'.format(note, noteLength)])
                    lyFile.addLyrics(['{0}'.format(
                        self.__helper.getGermanNotation(note, True))])
                # end for
                lyFile.writeToFile(generatedFile)
                result.append([constants.keyLilipond, generatedFile])
            else:
                result.append([constants.keySkipped, generatedFile])
        # end for
        return result
    # end generateNotes

    def generateScales(self) -> List[List[str]]:
        return [
            *self.__generateMajorScales(constants.ScaleGenerationType.Short),
            *self.__generateMajorScales(constants.ScaleGenerationType.FromTonic),
            *self.__generateMajorScales(constants.ScaleGenerationType.Full),
            *self.__generateAllScaleSignatures()
        ]
    # end generateScales

    #endregion ################################################################

    #region constructor #######################################################

    def __init__(self, config: Configuration, helper: Helper) -> None:
        self.__config = config
        self.__helper = helper
    # end constructor

    #endregion ################################################################

    #region private methods ###################################################

    def __generateMajorScales(self, generationType: constants.ScaleGenerationType) -> List[List[str]]:
        result = list()
        for _, scale in enumerate(self.__helper.majorScaleSignatures.keys()):
            title = self.__helper.getMajorScaleTitle(
                scale, generationType)
            generatedFile = '{0}/{1}.ly'.format(
                self.__config.lilypondScalesDirectory,
                title.replace(' ', '-')).lower()
            if (pathlib.Path(generatedFile).exists() == False or self.__config.regenerate == True):
                lyFile = LilypondLy(self.__config, scale, True, '4/4')
                lyFile.setTitle(title)
                lyFile.makeMoment = '1/8'
                melodyLine = []
                noteLine = []
                asString = self.__helper.generateMajorScale(
                    scale, generationType)

                for note in asString:
                    melodyLine.append(note)
                    noteLine.append(self.__helper.getGermanNotation(note, True))
                    if (len(melodyLine) == 4):
                        melodyLine.append('|')
                        lyFile.addNotes(melodyLine)
                        melodyLine = []
                        lyFile.addLyrics(noteLine)
                        noteLine = []
                # end for

                if len(melodyLine) > 0:
                    if len(melodyLine) == 1:
                        melodyLine.append('r4 r2')
                    elif len(melodyLine) == 2:
                        melodyLine.append('r2')
                    elif len(melodyLine) == 3:
                        melodyLine.append('r4')

                    melodyLine.append('|')
                    lyFile.addNotes(melodyLine)
                    lyFile.addLyrics(noteLine)
                # end if
                lyFile.writeToFile(generatedFile)
                result.append([constants.keyLilipond, generatedFile])
            else:
                result.append([constants.keySkipped, generatedFile])
            # end if
        # end for
        return result
    # end __generateMajorScales

    def __generateAllScaleSignatures(self) -> List[List[str]]:
        result = list()
        for _, tonleiter in enumerate(self.__helper.majorScaleSignatures.keys()):
            result.append(self.__generateScaleSignature(tonleiter, True))
        # end for

        for _, tonleiter in enumerate(self.__helper.minorScalesSignatures.keys()):
            result.append(self.__generateScaleSignature(tonleiter, False))
        # end for

        return result
    # end __generateAllScaleSignatures

    def __generateScaleSignature(self, key: str, major: bool) -> List[str]:
        result = []
        if (major == True):
            art = 'Dur'
        else:
            art = 'Mol'
        # end if-else

        title = 'Generalvorzeichen {0}-{1}'.format(key, art)
        generatedFile = '{0}/{1}.ly'.format(
            self.__config.lilypondScalesDirectory,
            title.replace(' ', '-')).lower()

        if (pathlib.Path(generatedFile).exists() == False or self.__config.regenerate == True):
            lyFile = LilypondLy(self.__config, key, major, '4/4')
            lyFile.setTitle(title)
            lyFile.addNotes(['s'])
            lyFile.writeToFile(generatedFile)
            result.append(constants.keyLilipond)
        else:
            result.append(constants.keySkipped)
        # end if
        result.append(generatedFile)
        return result
    # end generateGeneralVorzeichen

    #endregion ################################################################

# end class
