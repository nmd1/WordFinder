import xml.etree.ElementTree as xmlp
from urllib.request import Request, urlopen

testaudio = "heart.wav"


word2 = "hypocrite"
Dcall = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"+word2+"?key=" + DKey2
Tcall = "http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/"+word2+"?key=" + TKey
Audio = "http://media.merriam-webster.com/soundc11/h/"+testaudio
root = xmlp.parse('test.xml').getroot()



exresponse = '<entry id="hypocrite"> ' \
             '<ew>hypocrite</ew> ' \
             '<hw>hyp*o*crite</hw> ' \
             '<sound> <wav>hypocr02.wav</wav> </sound> ' \
             '<pr>ˈhi-pə-ˌkrit</pr> ' \
             '<fl>noun</fl> ' \
             '<et>Middle English <it>ypocrite,</it> from Anglo-French, from Late Latin <it>hypocrita,</it> from Greek <it>hypokritēs</it> actor, hypocrite, from <it>hypokrinesthai</it> </et> ' \
             '<def> <date>13th century</date> <sn>1</sn> <dt>:a person who puts on a false appearance of <d_link>virtue</d_link> or religion</dt> <sn>2</sn> <dt>:a person who acts in contradiction to his or her stated beliefs or feelings</dt> </def> ' \
             '<uro> <ure>hypocrite</ure> <fl>adjective</fl> </uro> ' \
             '</entry>'
root = xmlp.fromstring(exresponse)

root.tag #gets <entry>
root.attrib #gets id=hypocrite as a dictionary
root.text #gets the element [all of the response] in text

def getKeys(choice):
    Keys = []
    try:
        with open("Keys", 'r') as file:
            for line in file:
                Keys.append(line.replace('\n',''))
    except FileNotFoundError:
        print("Error Opening File")
        return "error"
    return Keys[choice]

#=============++Setup Debug Variable++==============
global debug
debug = True

def printd(string):
    if(debug): print(string)


class thedict:
    def __init__(self):
        self.root = ""
        self.requestMade = False
        self.listOfEntries = []
        self.DKey = getKeys(0)
        self.TKey = getKeys(1)
        printd("Object created")

    def requestWord(self, word):
        response = self.__htmlRequest__(word)
        self.root = xmlp.fromstring(response)
        if(not(self.root.tag == 'bad')):
            self.requestMade = True
            printd("Word Successfully obtained")
        else: root = ""


    def __htmlRequest__(self,word):

        request = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"+word+"?key=" + self.DKey
        response = urlopen(request)
        xmlFile = response.read().decode()

        wordresponse = xmlp.fromstring(xmlFile)[0].findall("ew") #[0].tex
        suggestionresponse = xmlp.fromstring(xmlFile).findall("suggestion") #[0].text

        if(not( len(wordresponse) or len(suggestionresponse))): return "<bad>RecievedNeitherSuggestionsNorResponse</bad>"
        if( len(wordresponse) and len(suggestionresponse)): return "<bad>RecievedSuggestionsAndResponse</bad>"

        if(len(wordresponse) and wordresponse[0].text == word):
            return xmlFile

        if(len(wordresponse) and not wordresponse[0].text == word):
            print("Not the same exact word")
            return xmlFile

        if(len(suggestionresponse)):
            printd("Word not found: Suggestions given")
            return xmlFile

        return "<bad>SomethingWentWrong</bad>"

    def saveCurrentEntry(self):
        self.listOfEntries.append(self.root)
        print("The word "+ self.getWord() + "has been saved onto a temperary list")
        return

    def getWord(self, entry = 0):
        if(entry > len(self.root)):
            printd("outofbounds")
            return ""
        return self.__getStuff__("ew", entry)

    def getPron(self, entry = 0):
        return self.__getStuff__("pr", entry)

    def getDef(self,entry = 0):
        definition = []
        count = 0
        for elements in self.root[entry].findall('def')[0]:
            if (count == 0):
                definition.append(elements.text)
                count = count + 1
                continue
            if (elements == ''):
                count = count + 1
                continue
            if (count % 2 == 0): definition.append(elements.text[1:])
            count = count + 1
        return definition

    def getEtom(self,entry = 0):
        return self.__getStuff__("et", entry)

    def getWordType(self,entry = 0):
        return self.__getStuff__("fl", entry)

    def getSound(self, entry = 0):
        return root[entry].findall("sound")[0][4].text

    def getRoot(self):
        return self.root

    def __getStuff__(self, type, entry = 0):
        return self.root[entry].findall(type)[0].text

    def printEverything(self):
        for wordresults in root:
            for wordinfo in wordresults:
                printd(wordinfo)



a = thedict()
apples = a.requestWord('apple')
a.getDef()



