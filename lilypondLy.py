from os.path import abspath

from configuration import Configuration


class LilypondLy:

    #region private properties ################################################
    __config: Configuration
    __melody = []
    __lyrics = []
    __key = 'c'
    __keyArt: str
    __timeSignature: str
    __makeMoment: str

    #endregion ################################################################

    #region getter/setter #####################################################

    @property
    def makeMoment(self) -> str:
        return self.__makeMoment
    # end makeMoment getter

    @makeMoment.setter
    def makeMoment(self, value: str):
        self.__makeMoment = value
    # end makeMoment setter

    #endregion ################################################################

    #region publlic methods ###################################################

    def addNotes(self, notes: list) -> None:
        notes.insert(0, ' ')
        self.__melody.append(' '.join(notes))
    # end addNotes

    def addLyrics(self, lyrics: list) -> None:
        lyrics.insert(0, ' ')
        self.__lyrics.append(' '.join(lyrics))
    # end addNotes

    def setTitle(self, titel: str) -> None:
        print('Lilypond -> {0}'.format(titel))
    # end setTitle

    def writeToFile(self, filename: str) -> None:

        with open(self.__config.lilypondTemplate) as template:
            contents = template.read()
            template.close()
        # end with
        contents = contents + '\n' + \
            '\n'.join(self.__buildContents())

        fileHandle = open(filename, 'w')
        fileHandle.write(contents)
        fileHandle.close()
    # end writeToFile

    #endregion ################################################################

    #region constructor #######################################################

    def __init__(self, config: Configuration, key: str, major: bool, timeSignature: str) -> None:
        self.__config = config
        self.__key = key.lower()
        self.__timeSignature = timeSignature
        self.makeMoment = None
        self.__melody = []
        self.__lyrics = []
        if (major == True):
            self.__keyArt = '\major'
        else:
            self.__keyArt = '\minor'
    # end constructor

    #endregion ################################################################

    #region private methods ###################################################

    def __buildMelody(self) -> list:
        head = [
            'melody = {',
            '  \key {0} {1}'.format(self.__key, self.__keyArt),
            '  \\numericTimeSignature',
            '  \\time {0}'.format(self.__timeSignature)
        ]
        if (self.__makeMoment is not None):
            head.append(
                '  \set Score.proportionalNotationDuration = #(ly:make-moment {0})'.format(self.makeMoment))
        return [
            *head,
            *self.__melody,
            '  \\bar "|."',
            '}'
        ]
    # end buildMelodyString

    def __buildLyrics(self) -> list:
        result = []
        if (len(self.__lyrics) > 0):
            result = [
                'names = \lyricmode {',
                *self.__lyrics,
                '}'
            ]
        return result
    # end buildLyricsString

    def __buildScore(self) -> list:
        result = [
            '\score {',
            '  <<',
            '    \\new Staff {',
            '      \\new Voice = "mel" \melody',
            '    }'
        ]
        if (len(self.__lyrics) > 0):
            result.append('    \\new Lyrics \lyricsto mel { \\names }')
        return [
            *result,
            '  >>',
            '}'
        ]
    # end buildScore

    def __buildContents(self) -> list:
        return [
            *self.__buildMelody(),
            '',
            *self.__buildLyrics(),
            '',
            *self.__buildScore()
        ]
    # end buildcontents

    #endregion ################################################################

# end class
