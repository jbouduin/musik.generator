from collections import Counter

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

    # Generalvorzeichen in den Durtonleitern
    __generalvorzeichenDur = dict([
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

    # Generalvorzeichen in den Moltonleitern
    __generalvorzeichenMol = dict([
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

    # intervalle: Schlüssel ist die Anzahl an Halbtonschritte
    __intervalle = dict([
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

    # intervalle in Halbtöne in den Durtonleiter
    __durtonleiterIntervalle = [2, 2, 1, 2, 2, 2, 1]

    # Noten verwendet um einen Durtonleiter mit Kreuze zu generieren
    __durTonleiterNoten = ['C', 'Cis', 'D', 'Dis', 'E',
                    'F', 'Fis', 'G', 'Gis', 'A', 'Ais', 'B']
    # Fis-Dur soll Eis verwenden statt F
    __durTonleiterNoten6 = ['C', 'Cis', 'D', 'Dis', 'E',
                     'Eis', 'Fis', 'G', 'Gis', 'A', 'Ais', 'B']
    # Noten verwendet um einen Durtonleiter mit bemols zu generieren
    __molTonleiterNoten = ['C', 'Des', 'D', "Es", "E",
                    "F", "Ges", "G", "As", "A", "Bes", "B"]
    # Ges-Dur soll Ces verwenden, statt B
    __molTonleiterNoten6 = ['C', 'Des', 'D', "Es", "E",
                     "F", "Ges", "G", "As", "A", "Bes", "Ces"]

    # chromatische tonleiter mit enharmonische Töne (ohne doppelte Versetzungzeichen)
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

    # halbtone in eine oktave
    __oktave = 12

    #endregion ################################################################

    #region getters ###########################################################

    @property
    def durtonleiterIntervalle(self) -> list:
        return self.__durtonleiterIntervalle
    #end getter durtonleiterIntervalle

    @property
    def generalvorzeichenDur(self) -> dict:
        return self.__generalvorzeichenDur
    #end getter generalvorzeichenDur

    @property
    def generalvorzeichenMol(self) -> dict:
        return self.__generalvorzeichenMol
    #end getter generalvorzeichenMol

    #endregion ################################################################

    #region public methods ####################################################

    def generateDurIntervalle(self, tonleiter: str) -> list:
        result = []
        tonesToUse = self.__getDurTonesToUse(tonleiter)
        firstNoteIndex = self.__getLowestNote(tonesToUse, tonleiter, True)
        firstNote = tonesToUse[firstNoteIndex]
        noteIndex = firstNoteIndex
        totalInterval = 0
        for interval in [0, *self.__durtonleiterIntervalle]:
            noteIndex = noteIndex + interval
            totalInterval = totalInterval + interval
            name = self.__intervalle[totalInterval]
            if (noteIndex <= len(tonesToUse)):
                result.append([name, firstNote, tonesToUse[noteIndex]])
        # end for

        return result
    # end generateIntervalle

    def generateDurTonleiter(self, tonleiter: str, eingestriches: bool = False) -> list:
        tonesToUse = self.__getDurTonesToUse(tonleiter)
        noteIndex = self.__getLowestNote(tonesToUse, tonleiter, eingestriches)
        result = [tonesToUse[noteIndex]]
        # print(noteIndex, tonesToUse[noteIndex], tonesToUse)
        totalInterval = 0
        while True:
            for interval in self.__durtonleiterIntervalle:
                noteIndex = noteIndex + interval
                totalInterval = totalInterval + interval
                if ((noteIndex >= len(tonesToUse)) or (eingestriches == True and totalInterval > 12)):
                    break
                result.append(tonesToUse[noteIndex])
            # end for
            if noteIndex >= len(tonesToUse):
                break
        # end while
        return result
    # end generateDurTonleiter

    def getAllViolinNotes(self) -> list:
        result = []
        amEnde = False
        suffix = ''
        index = self.__chromatic.index([self.__lowestnote.upper()])
        while not amEnde:
            eintrag = []
            for note in self.__chromatic[index]:
                if (note == 'Ces'):
                    suffix = suffix + "'"
                #end if
                resultNote = note.lower() + suffix
                if (resultNote == self.__highestnote):
                    amEnde = True
                #end if
                eintrag.append(resultNote)
            index = index + 1
            if (index == len(self.__chromatic)):
                index = 0

            result.append(eintrag)
        #end while
        return result
    #end getAllViolinNotes

    def getDurtonleiterTitel(self, tonleiter: str, eingestrichenes: bool) -> str:
        if (eingestrichenes == True):
            titel = 'Kurzer Tonleiter in {0}-Dur'.format(
                self.getGermanNotation(tonleiter))
        else:
            titel = 'Ganzer Tonleiter auf der Violine in {0}-Dur'.format(
                self.getGermanNotation(tonleiter))
        return titel
    # end getDurtonleiterTitel

    def getGermanNotation(self, org: str, stripTonleiter: bool = False, oktaveNumerisch: bool = False) -> str:
        result = org
        if (org.startswith('Bes')):
            result = org.replace('Bes', 'B')
        elif (org.startswith('bes')):
            result = org.replace('bes', 'b')
        elif (org.startswith('B')):
            result = org.replace('B', 'H')
        elif (org.startswith('b')):
            result = org.replace('b', 'h')

        if (stripTonleiter == True):
            result = result.strip("'")
        elif (oktaveNumerisch == True):
            result = self.__stricheToNummer(result)

        return result
    # end getGermanNotation

    def getIntervallTitel(self, intervall: str, tonleiter: str) -> str:
        return '{0} in {1}-Dur vom Grundton'.format(
            intervall,
            self.getGermanNotation(tonleiter))
    # end getIntervallTitle

    def getNoteTitel(self, noten: list) -> str:
        result = ''
        if (len(noten) == 1):
            result = 'Note {0}'.format(
                self.getGermanNotation(noten[0], False, True).lower())
        else:
            result = 'Note {0}-{1}'.format(
                self.getGermanNotation(noten[0], False, True).lower(),
                self.getGermanNotation(noten[1], False, True).lower())
        #end if-else
        return result
    #end getNoteTitel

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
            chromaticToUse = self.__durTonleiterNoten6
        else:
            chromaticToUse = self.__durTonleiterNoten
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
    # end fillIsTones

    def __fillEsTones(self, is6: bool) -> list:
        result = []
        toneLoop = 7
        lilypondNote = ''
        suffix = ''
        if (is6 == True):
            chromaticToUse = self.__molTonleiterNoten6
        else:
            chromaticToUse = self.__molTonleiterNoten

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
    # end fillIsTones

    def __getDurTonesToUse(self, tonleiter: str) -> list:
        generalVorzeichen = self.__generalvorzeichenDur[tonleiter]
        if (generalVorzeichen >= 0):
            if (generalVorzeichen == 6):
                tonesToUse = self.__isTones6
            else:
                tonesToUse = self.__isTones
        else:
            if (generalVorzeichen == -6):
                tonesToUse = self.__esTones6
            else:
                tonesToUse = self.__esTones
        # end if-else
        return tonesToUse
    # end getDurTonesToUse

    def __getLowestNote(self, tones: list, tonleiter: str, eingestrichenes: bool = False) -> int:
        result = 0
        low = str(tonleiter).lower()
        if (low in tones):
            result = tones.index(low)
        else:
            result = tones.index(low + "'")
        if (eingestrichenes == True):
            bIndex = 0
            if ('bes' in tones):
                bIndex = tones.index('bes')
            else:
                bIndex = tones.index('b')
            if (result < bIndex):
                result = result + self.__oktave
        # print(tonleiter, low, ':', tones, result)
        return result
    # end getLowestNote

    def __stricheToNummer(self, note: str) -> str:
        result = note
        cnt = Counter(note)
        if ("'" in cnt):
            result = note.replace("'", '') + str(cnt["'"])
        #end if
        return result
    #end stricheToNummer

# end class
