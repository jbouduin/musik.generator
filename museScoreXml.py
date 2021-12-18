from typing import Any
import xml.etree.ElementTree as ET

from configuration import Configuration


class MuseScoreXml:

    #region private properties ################################################
    __config: Configuration
    __museScore: ET.ElementTree
    __museScoreRoot: Any
    __museStaff: Any

    #endregion ################################################################

    #region public methods ####################################################

    def addTitle(self, title: str) -> None:
        print('Musescore -> {0}'.format(title))
        museTitle = self.__museStaff.find('./VBox/Text/text')
        museTitle.text = title
    # end addTitle

    def addNewMeasureWithVoice(self) -> ET.Element:
        measure = ET.Element('Measure')
        self.__museStaff.append(measure)
        voice = ET.Element('voice')
        measure.append(voice)
        return voice
    # end addNewMeasureWithVoice

    def addRestToVoice(self, voice: ET.Element, durationType: str) -> ET.Element:
        rest = ET.Element('Rest')
        voice.append(rest)
        self.__addDuration(rest, durationType)
        return rest
    # end addRestToVoice

    def addSingleNoteToVoice(self, voice: ET.Element, pitch: int, tpc: int, durationType: str) -> ET.Element:
        chord = self.__addChordToVoice(voice, durationType)
        note = self.__addNoteToChord(chord, pitch, tpc)
        return note
    # end addSingleNoteToVoice

    def addTimeSignatureToVoice(self, voice: ET.Element, sigN: int, sigD: int) -> ET.Element:
        timeSignature = ET.Element('TimeSig')
        voice.append(timeSignature)
        mSigN = ET.Element('sigN')
        mSigN.text = str(sigN)
        timeSignature.append(mSigN)
        mSigD = ET.Element('sigD')
        mSigD.text = str(sigD)
        timeSignature.append(mSigD)
        return timeSignature
    # end addTimeSignatureToVoice

    def addKeySignaturetoVoice(self, voice: ET.Element, accidentals: int) -> ET.Element:
        keysignature = ET.Element('KeySig')
        voice.append(keysignature)
        accidental = ET.Element('accidental')
        keysignature.append(accidental)
        accidental.text = str(accidentals)
        return keysignature
    # end addKeySignaturetoVoice

    def writeToFile(self, path: str) -> None:
        self.__museScore.write(path, encoding='UTF-8', xml_declaration=True)
    # end writeToFile

    #endregion ################################################################

    #region constructor #######################################################

    def __init__(self, config: Configuration, template: str) -> None:
        self.__config = config
        self.__museScore = ET.parse(template)
        self.__museScoreRoot = self.__museScore.getroot()
        self.__museStaff = self.__museScoreRoot.find("./Score/Staff[@id='1']")
        self.__setStandardPitch()
    # end constructor

    #endregion ################################################################

    #region private methods ###################################################

    def __addChordToVoice(self, voice: ET.Element, durationType: str):
        chord = ET.Element('Chord')
        voice.append(chord)
        self.__addDuration(chord, durationType)
        return chord
    # end addChordToVoice

    def __addDuration(self, parent: ET.Element, durationType: str) -> ET.Element:
        duration = ET.Element('durationType')
        duration.text = durationType
        parent.append(duration)
        return duration
    # end addDuration

    def __addNoteToChord(self, chord: ET.Element, pitch: int, tpc: int) -> ET.Element:
        note = ET.Element('Note')
        chord.append(note)
        mPitch = ET.Element('pitch')
        note.append(mPitch)
        mPitch.text = str(pitch)
        mTpc = ET.Element('tpc')
        note.append(mTpc)
        mTpc.text = str(tpc)
        return note
    # end addNoteToChord

    def __setStandardPitch(self):
        pitchElement = self.__museScoreRoot.find("./Score/Synthesizer/master/val[@id='3']")
        if (self.__config.verbose == True):
            print('setting standard pitch to {0}'.format(
                self.__config.standardPitch))
        #end if
        pitchElement.text = str(self.__config.standardPitch)
    # end __setStandardPitch
    #endregion ################################################################
# end class
