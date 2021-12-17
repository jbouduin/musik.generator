from os.path import abspath
from configuration import Configuration
from helper import Helper
from lilypondLy import LilypondLy


class LilyPondGenerator:

    #region private properties ################################################
    __config: Configuration
    __helper: Helper
    #endregion ################################################################

    #region public methods ####################################################

    def generateIntervalle(self) -> list:
        result = []
        for tonleiter in ['G', 'D', 'A', 'E']:
            intervals = self.__helper.generateDurIntervalle(tonleiter)
            for interval in intervals:
                title = self.__helper.getIntervallTitel(interval[0], tonleiter)
                lyFile = LilypondLy(tonleiter, True, '9/8')
                lyFile.setTitle(title)
                lyFile.makeMoment = '1/8'
                lyFile.addNotes(
                    ['{0}2 r8 {1}2 |'.format(interval[1], interval[2])])
                lyFile.addLyrics(['{0} {1}'.format(self.__helper.getGermanNotation(
                    interval[1], True), self.__helper.getGermanNotation(interval[2], True))])

                generatedFile = '{0}/{1}.ly'.format(
                    self.__config.lilypondIntervalle,
                    title.replace(' ', '-')).lower()
                lyFile.writeToFile(generatedFile)
                result.append(['Lilypond', generatedFile])
            # end for
        # end for
        return result
    # end generateIntervals

    def generateNoten(self) -> list:
        result = []
        allNotes = self.__helper.getAllViolinNotes()
        for notes in allNotes:
            titel = self.__helper.getNoteTitel(notes)

            lyFile = LilypondLy('C', True, '4/4')
            lyFile.setTitle(titel)
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

            generatedFile = '{0}/{1}.ly'.format(
                self.__config.lilypondNoten,
                titel.replace(' ', '-')).lower()
            lyFile.writeToFile(generatedFile)
            result.append(['Lilypond', generatedFile])
        # end for
        return result
    # end generateNoten

    def generateTonleiter(self) -> list:
        return [
            *self.__generateDurtonleiter(True),
            *self.__generateDurtonleiter(False),
            *self.__generateAllGeneralVorzeichen()
        ]
    # end generateTonleiter

    #endregion ################################################################

    #region constructor #######################################################

    def __init__(self, config: Configuration, helper: Helper) -> None:
        self.__config = config
        self.__helper = helper
    # end constructor

    #endregion ################################################################

    #region private methods ###################################################

    def __generateDurtonleiter(self, eingestrichenes: bool) -> list:
        result = list()
        for _, tonleiter in enumerate(self.__helper.generalvorzeichenDur.keys()):
            asString = self.__helper.generateDurTonleiter(
                tonleiter, eingestrichenes)
            titel = self.__helper.getDurtonleiterTitel(
                tonleiter, eingestrichenes)
            lyFile = LilypondLy(tonleiter, True, '4/4')
            lyFile.setTitle(titel)
            lyFile.makeMoment = '1/8'
            melodyLine = []
            noteLine = []

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
            generatedFile = '{0}/{1}.ly'.format(
                self.__config.lilypondTonleiter,
                titel.replace(' ', '-')).lower()
            lyFile.writeToFile(generatedFile)
            result.append(['Lilypond', generatedFile])
        # end for
        return result
    # end generateDurTonleiterExt

    def __generateAllGeneralVorzeichen(self) -> list:
        result = []
        for _, tonleiter in enumerate(self.__helper.generalvorzeichenDur.keys()):
            result.append(
                ['Lilypond', self.__generateGeneralVorzeichen(tonleiter, True)])
        # end for

        for _, tonleiter in enumerate(self.__helper.generalvorzeichenMol.keys()):
            result.append(
                ['Lilypond', self.__generateGeneralVorzeichen(tonleiter, False)])
        # end for

        return result
    # end generateGeneralVorzeichen

    def __generateGeneralVorzeichen(self, key: str, major: bool) -> str:
        if (major == True):
            art = 'Dur'
        else:
            art = 'Mol'
        # end if-else
        titel = 'Generalvorzeichen {0}-{1}'.format(key, art)
        lyFile = LilypondLy(key, major, '4/4')
        lyFile.setTitle(titel)
        lyFile.addNotes(['s'])
        generatedFile = '{0}/{1}.ly'.format(
            self.__config.lilypondTonleiter,
            titel.replace(' ', '-')).lower()
        lyFile.writeToFile(generatedFile)

        return generatedFile
    # end generateGeneralVorzeichen

    #endregion ################################################################

# end class
