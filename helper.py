from collections import Counter
from typing import List

from constants import ScaleGenerationType

# TODO Split into a musical helper and a text helper


class Helper:

    #region private properties ################################################

    # Liste der Töne in gewohnte Notation: a, b, c, d, e, f, g
    # Die listen werde befüllt von g bis b'' (Violine)
    __isTones: list
    __isTones6: list
    __esTones: list
    __esTones6: list

    # lowest pitch for a violin is G3 (wissenschäftlich) / g (in der kleinen Octave)
    __lowestnote = 'g'
    # highest pitch in first position on a violin is B5 / b'' (in der zweigestrichenen Oktave)
    # auf Deutsch H5 / h''
    __highestnote = "b''"

    # Key signatures for Major scales
    __majorScalesSignatures = dict([
        ('C', 0),
        ('G', 1),
        ('D', 2),
        ('A', 3),
        ('E', 4),
        ('B', 5),  # Deutsch: H
        ('Fis', 6),
        ('Ges', -6),
        ('Des', -5),
        ('As', -4),
        ('Es', -3),
        ('Bes', -2),  # Deutsch: B
        ('F', -1)
    ])

    # Key signatures for Major scales
    __minorScalesSignatures = dict([
        ('A', 0),
        ('E', 1),
        ('B', 2),  # Deutsch: H
        ('Fis', 3),
        ('Cis', 4),
        ('Gis', 5),
        ('Dis', 6),
        ('Es', -6),
        ('Bes', -5),  # Deutsch: B
        ('F', -4),
        ('C', -3),
        ('G', -2),  # Deutsch: B
        ('D', 1)
    ])

    # intervals dictionary: Key is the number of halftones
    __intervals = dict([
        (0, 'Reine Prim'),
        (1, 'Kleine Sekunde'),
        (2, 'Große Sekunde'),
        (3, 'Kleine Terz'),
        (4, 'Große Terz'),
        (5, 'Reine Quarte'),
        (7, 'Reine Quinte'),
        (8, 'Kleine Sexte'),
        (9, 'Große Sexte'),
        (10, 'Kleine Septe'),
        (11, 'Große Septe'),
        (12, 'Reine Oktave')
    ])

    # intervals from the Major scale
    __majorScaleIntervals: List[int] = [2, 2, 1, 2, 2, 2, 1]

    # Notes used to generate a major scale with 0 to 5 ♯'s
    __majorScaleNotes0to5Sharps: List[str] = ['C', 'Cis', 'D', 'Dis', 'E',
                                              'F', 'Fis', 'G', 'Gis', 'A', 'Ais', 'B']
    # Fis-Major (6♯) should use Eis instead of F
    __majorScaleNotes6Sharps: List[str] = ['C', 'Cis', 'D', 'Dis', 'E',
                                           'Eis', 'Fis', 'G', 'Gis', 'A', 'Ais', 'B']
    # Notes used to generate a major scale with 0 to 5 ♭'s
    __majorScaleNotes0to5Flats: List[str] = ['C', 'Des', 'D', "Es", "E",
                                             "F", "Ges", "G", "As", "A", "Bes", "B"]
    # Ges-Dur (6♭) soll Ces verwenden, statt B
    __majorScaleNotes6Flats: List[str] = ['C', 'Des', 'D', "Es", "E",
                                          "F", "Ges", "G", "As", "A", "Bes", "Ces"]

    # chromatic scale with enharmonics, but without double sharp and double flats
    __chromatic = [
        ['C'],
        ['Cis', 'Des'],
        ['D'],
        ['Dis', 'Es'],
        ['E', 'Fes'],
        ['Eis', 'F'],
        ['Fis', 'Ges'],
        ['G'],
        ['Gis', 'As'],
        ['A'],
        ['Ais', 'Bes'],
        ['B', 'Ces']
    ]

    # halftones in an octave
    __octave = 12

    #endregion ################################################################

    #region getters ###########################################################

    @property
    def majorScaleIntervals(self) -> List[int]:
        return self.__majorScaleIntervals
    # end getter majorScaleIntervals

    @property
    def majorScaleSignatures(self) -> dict:
        return self.__majorScalesSignatures
    # end getter majorScaleSignatures

    @property
    def minorScalesSignatures(self) -> dict:
        return self.__minorScalesSignatures
    # end getter minorScalesSignatures

    #endregion ################################################################

    #region public methods ####################################################

    def generateMajorIntervals(self, scale: str) -> list:
        result = []
        tonesToUse = self.__getMajorTonesToUse(scale)
        firstNoteIndex = self.__getLowestNote(
            tonesToUse, scale, ScaleGenerationType.Short)
        firstNote = tonesToUse[firstNoteIndex]
        noteIndex = firstNoteIndex
        totalInterval = 0
        for interval in [0, *self.__majorScaleIntervals]:
            noteIndex = noteIndex + interval
            totalInterval = totalInterval + interval
            name = self.__intervals[totalInterval]
            if (noteIndex <= len(tonesToUse)):
                result.append([name, firstNote, tonesToUse[noteIndex]])
        # end for

        return result
    # end generateMajorIntervals

    def generateMajorScale(self, scale: str, scaleGenerationType: ScaleGenerationType) -> list:
        tonesToUse = self.__getMajorTonesToUse(scale)
        noteIndex = self.__getLowestNote(
            tonesToUse, scale, scaleGenerationType)
        result = [tonesToUse[noteIndex]]
        # print(noteIndex, tonesToUse[noteIndex], tonesToUse)
        totalInterval = 0

        if (scaleGenerationType == ScaleGenerationType.Full):
            # TODO calculate
            signature = self.__majorScalesSignatures[scale]
            shift = 4
            if (signature == 1):
                shift = 0
            elif (signature == 2):
                shift = 3
            elif (signature == 3 or signature == -4):
                shift = 6
            elif (signature == 4 or signature == -3):
                shift = 2
            elif (signature == 5 or signature == -2):
                shift = 5
            elif (signature == 6 or signature == -1):
                shift = 1
            elif (signature == -5):
                shift = 4
            elif (signature == -6):
                shift = 1

            intervalsToUse = [
                *self.__majorScaleIntervals[shift::],
                *self.__majorScaleIntervals[0:shift]
            ]
            # print(signature, shift, self.__majorScaleIntervals, '->', intervalsToUse)
        else:
            intervalsToUse = self.__majorScaleIntervals
        # end if
        while True:
            for interval in intervalsToUse:
                noteIndex = noteIndex + interval
                totalInterval = totalInterval + interval
                if ((noteIndex >= len(tonesToUse)) or (scaleGenerationType == ScaleGenerationType.Short and totalInterval > 12)):
                    break
                result.append(tonesToUse[noteIndex])
            # end for
            if noteIndex >= len(tonesToUse):
                break
        # end while
        return result
    # end generateMajorScale

    def getAllViolinNotes(self) -> list:
        result = []
        finished = False
        suffix = ''
        index = self.__chromatic.index([self.__lowestnote.upper()])
        while not finished:
            entry = []
            for note in self.__chromatic[index]:
                if (note == 'Ces'):
                    suffix = suffix + "'"
                # end if
                resultNote = note.lower() + suffix
                if (resultNote == self.__highestnote):
                    finished = True
                # end if
                entry.append(resultNote)
            index = index + 1
            if (index == len(self.__chromatic)):
                index = 0

            result.append(entry)
        # end while
        return result
    # end getAllViolinNotes

    def getMajorScaleTitle(self, scale: str, generationType: ScaleGenerationType) -> str:
        if (generationType == ScaleGenerationType.Short):
            titel = 'Kurzer Tonleiter in {0}-Dur'.format(
                self.getGermanNotation(scale))
        elif (generationType == ScaleGenerationType.FromTonic):
            titel = 'Tonleiter ab dem Grundton in {0}-Dur'.format(
                self.getGermanNotation(scale))
        else:
            titel = 'Ganzer Tonleiter auf der Violine in {0}-Dur'.format(
                self.getGermanNotation(scale))
        return titel
    # end getMajorScaleTitle

    def getGermanNotation(self, org: str, stripOctave: bool = False, oktaveNumeric: bool = False) -> str:
        result = org
        if (org.startswith('Bes')):
            result = org.replace('Bes', 'B')
        elif (org.startswith('bes')):
            result = org.replace('bes', 'b')
        elif (org.startswith('B')):
            result = org.replace('B', 'H')
        elif (org.startswith('b')):
            result = org.replace('b', 'h')

        if (stripOctave == True):
            result = result.strip("'")
        elif (oktaveNumeric == True):
            result = self.__toNumericOctave(result)

        return result
    # end getGermanNotation

    def getIntervalTitle(self, interval: str, scale: str) -> str:
        return '{0} in {1}-Dur vom Grundton'.format(
            interval,
            self.getGermanNotation(scale))
    # end getIntervalTitle

    def getNoteTitle(self, notes: list) -> str:
        result = ''
        if (len(notes) == 1):
            result = 'Note {0}'.format(
                self.getGermanNotation(notes[0], False, True).lower())
        else:
            result = 'Note {0}-{1}'.format(
                self.getGermanNotation(notes[0], False, True).lower(),
                self.getGermanNotation(notes[1], False, True).lower())
        # end if-else
        return result
    # end getNoteTitle

    #endregion ################################################################

    #region constructor #######################################################

    def __init__(self) -> None:
        self.__isTones = self.__fillIsTones(False)
        self.__isTones6 = self.__fillIsTones(True)
        self.__esTones = self.__fillEsTones(False)
        self.__esTones6 = self.__fillEsTones(True)
    # end constructor

    #endregion ################################################################

    #region private methods ###################################################
    def __fillIsTones(self, is6: bool) -> list:
        result = []
        toneLoop = 7
        lilypondNote = ''
        suffix = ''
        if (is6 == True):
            chromaticToUse = self.__majorScaleNotes6Sharps
        else:
            chromaticToUse = self.__majorScaleNotes0to5Sharps
        while lilypondNote != "b''":
            increment = toneLoop % 12
            note = chromaticToUse[increment].lower()
            if (note == 'c'):
                suffix = suffix + "'"
            lilypondNote = note + suffix
            result.append(lilypondNote)
            toneLoop = toneLoop + 1
        # end while

        # print('istones:', len(result), result)
        return result
    # end __fillIsTones

    def __fillEsTones(self, is6: bool) -> list:
        result = []
        toneLoop = 7
        lilypondNote = ''
        suffix = ''
        if (is6 == True):
            chromaticToUse = self.__majorScaleNotes6Flats
        else:
            chromaticToUse = self.__majorScaleNotes0to5Flats

        while lilypondNote != "b''" and lilypondNote != "ces'''":
            increment = toneLoop % 12
            note = chromaticToUse[increment].lower()
            if (is6 == False and note == 'c') or (is6 == True and note == 'ces'):
                suffix = suffix + "'"
            lilypondNote = note + suffix
            # print(lilypondNote)
            result.append(lilypondNote)
            toneLoop = toneLoop + 1
        # end while

        # print('estones:', len(result), result)
        return result
    # end __fillEsTones

    def __getMajorTonesToUse(self, scale: str) -> list:
        signature = self.__majorScalesSignatures[scale]
        if (signature >= 0):
            if (signature == 6):
                tonesToUse = self.__isTones6
            else:
                tonesToUse = self.__isTones
        else:
            if (signature == -6):
                tonesToUse = self.__esTones6
            else:
                tonesToUse = self.__esTones
        # end if-else
        return tonesToUse
    # end __getMajorTonesToUse

    def __getLowestNote(self, tones: list, scale: str, generationType: ScaleGenerationType) -> int:
        result = 0
        if (generationType == ScaleGenerationType.Full):
            # check if we have g or gis in the scal
            signature = self.__majorScalesSignatures[scale]
            if (signature >= 3):
                low = 'gis'
            elif (signature <= -5):
                low = 'as'
            else:
                low = 'g'
            # end if-else
            result = tones.index(low)
        else:
            low = str(scale).lower()
            if (low in tones):
                result = tones.index(low)
            else:
                result = tones.index(low + "'")
            if (generationType == ScaleGenerationType.Short):
                bIndex = 0
                if ('bes' in tones):
                    bIndex = tones.index('bes')
                else:
                    bIndex = tones.index('b')
                if (result < bIndex):
                    result = result + self.__octave
            # end if
        # end if-else

        # print('{0} {1} {2} ({3}): {4}'.format(
        #     str(generationType),
        #     scale,
        #     low,
        #     result,
        #     ' - '.join(tones).strip(' - '))
        # )
        return result
    # end __getLowestNote

    def __toNumericOctave(self, note: str) -> str:
        result = note
        cnt = Counter(note)
        if ("'" in cnt):
            result = note.replace("'", '') + str(cnt["'"])
        # end if
        return result
    # end __toNumericOctave

# end class
