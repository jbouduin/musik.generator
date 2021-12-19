from os.path import abspath
from configuration import Configuration
from helper import Helper
from museScoreXml import MuseScoreXml


class MuseScoreGenerator:

    #region private properties ################################################
    __config: Configuration
    __helper: Helper

    # Dictionary of enharmonics, the key is the number of halftones over C
    # also includes the pitchclasses used by Musescore
    __enharmonicsTable = dict([
        (11, dict([('Aisis', 31), ('B', 19), ('Ces', 7)])),
        (10, dict([('Ais',   24), ('Bes', 12), ('Ceses', 0)])),
        (9, dict([('Gisis', 29), ('A', 17), ('Beses', 5)])),
        (8, dict([('Gis', 22), ('As', 10)])),
        (7, dict([('Fisis', 27), ('G', 15), ('Ases', 3)])),
        (6, dict([('Eisis', 32), ('Fis', 20), ('Ges', 8)])),
        (5, dict([('Eis', 25), ('F', 13), ('Geses', 1)])),
        (4, dict([('Disis', 30), ('E', 18), ('Fes', 6)])),
        (3, dict([('Dis', 23), ('Es', 11), ('Feses', -1)])),
        (2, dict([('Cisis', 28), ('D', 16), ('Eses', 4)])),
        (1, dict([('Bisis', 33), ('Cis', 21), ('Des', 9)])),
        (0, dict([('Bis', 26), ('C', 14), ('Deses', 2)])),
    ])

    # mapping of the notes to a pitch and pitchclass
    __pitchTable: dict


    # lowest tone as Musescore value for the violin: G3 (scientific notation) / small g
    __lowestPitch = 55
    # highest tone as Musescore value for the violin in first position: B5 / b''
    # using German notation: H5 / h''
    __highestPitch = 83

    #endregion ################################################################

    #region public methods ####################################################

    def generateIntervals(self) -> list:
        result = []
        for tonleiter in ['G', 'D', 'A', 'E']:
            intervals = self.__helper.generateMajorIntervals(tonleiter)
            for interval in intervals:
                title = self.__helper.getIntervalTitle(interval[0], tonleiter)
                museScore = MuseScoreXml(self.__config)
                museScore.addTitle(title)
                museVoice = museScore.addNewMeasureWithVoice()
                museScore.addTimeSignatureToVoice(museVoice, 9, 8)
                museScore.addKeySignaturetoVoice(
                    museVoice, self.__helper.majorScaleSignatures[tonleiter])
                startPitch = self.__pitchTable[interval[1]]
                endPitch = self.__pitchTable[interval[2]]
                museScore.addSingleNoteToVoice(museVoice, startPitch[0],
                                               startPitch[1], 'half')
                museScore.addRestToVoice(museVoice, 'eighth')
                museScore.addSingleNoteToVoice(museVoice, endPitch[0],
                                               endPitch[1], 'half')

                generatedFile = '{0}/{1}.mscx'.format(
                    self.__config.musescoreIntervalsDirectory,
                    title.replace(' ', '-')).lower()
                museScore.writeToFile(generatedFile)
                result.append(['Musescore', generatedFile])
            # end for
        # end for
        return result
    # end generateIntervals

    def generateNotes(self) -> list:
        result = []
        allNotes = self.__helper.getAllViolinNotes()
        for notes in allNotes:
            museScore = MuseScoreXml(self.__config)
            titel = self.__helper.getNoteTitle(notes)
            museScore.addTitle(titel)
            museVoice = museScore.addNewMeasureWithVoice()
            museScore.addTimeSignatureToVoice(museVoice, 4, 4)
            museScore.addKeySignaturetoVoice(
                museVoice, self.__helper.majorScaleSignatures['C'])
            pitch = self.__pitchTable[notes[0]]
            museScore.addSingleNoteToVoice(
                museVoice, pitch[0], pitch[1], 'whole')
            generatedFile = '{0}/{1}.mscx'.format(
                self.__config.musescoreNotesDirectory,
                titel.replace(' ', '-')).lower()
            museScore.writeToFile(generatedFile)
            result.append(['Musescore', generatedFile])

        # end for

        return result
    # end generateNotes

    def generateScales(self) -> list:
        return [
            *self.__generateMajorScales(True),
            *self.__generateMajorScales(False),
            *self.__generateMinorScales()
        ]
    # end generateScales

    #endregion ################################################################

    #region Constructor #######################################################

    def __init__(self, config: Configuration, helper: Helper) -> None:
        self.__config = config
        self.__helper = helper
        self.__pitchTable = self.__fillPitchTable()
    # end constructor

    #endregion ################################################################

    #region private methods ###################################################

    def __fillPitchTable(self) -> dict:
        result = dict()
        suffix = ''
        # 55 = g => reine quinte über c, also Zeile mit Schlüssel 7 in enharmonicsTable
        toneLoop = self.__lowestPitch
        overC = 7
        # add the pitches
        while (toneLoop <= self.__highestPitch):
            enharmonics = self.__enharmonicsTable[overC]
            for _, (tone, pitchclass) in enumerate(enharmonics.items()):
                if(tone == 'C'):
                    suffix = suffix + "'"
                key = tone.lower() + suffix
                if(tone == 'Ceses' or tone == 'Ces'):
                    key = key + "'"
                result[key] = (toneLoop, pitchclass)

            toneLoop = toneLoop + 1
            overC = overC + 1
            if (overC == 12):
                overC = 0
            # end if
        # end while
        return result
    # end fillPitchTable

    def __generateMajorScales(self, startInSmallOctave: bool) -> list:
        result = list()
        for _, (scale, signature) in enumerate(self.__helper.majorScaleSignatures.items()):
            asString = self.__helper.generateMajorScale(
                scale, startInSmallOctave)
            museScore = MuseScoreXml(self.__config)
            title = self.__helper.getMajorScaleTitle(
                scale, startInSmallOctave)
            museScore.addTitle(title)
            museVoice = museScore.addNewMeasureWithVoice()
            museScore.addTimeSignatureToVoice(museVoice, 4, 4)
            museScore.addKeySignaturetoVoice(museVoice, signature)

            notesWritten = 0
            for note in asString:
                currentPitch = self.__pitchTable[note]
                if (museVoice is None):
                    museVoice = museScore.addNewMeasureWithVoice()
                museScore.addSingleNoteToVoice(museVoice, currentPitch[0],
                                               currentPitch[1], 'quarter')
                notesWritten = notesWritten + 1
                if (notesWritten == 4):
                    notesWritten = 0
                    museVoice = None
            # end for

            if notesWritten > 0:
                if notesWritten == 1:
                    museScore.addRestToVoice(museVoice, 'quarter')
                    museScore.addRestToVoice(museVoice, 'half')
                elif notesWritten == 2:
                    museScore.addRestToVoice(museVoice, 'half')
                elif notesWritten == 3:
                    museScore.addRestToVoice(museVoice, 'quarter')
            #end if
            generatedFile = '{0}/{1}.mscx'.format(
                self.__config.musescoreScalesDirectory,
                title.replace(' ', '-')).lower()

            museScore.writeToFile(generatedFile)
            result.append(['Musescore', generatedFile])
        # end for
        return result
    # end __generateMajorScales

    def __generateMinorScales(self) -> list:
        result = list()
        return result
    # end __generateMinorScales

    #endregion ################################################################

# end class
