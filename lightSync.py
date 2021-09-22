import os.path
import xml.etree.ElementTree as xml
from time import sleep

from yeelight import Bulb
from mcrcon import MCRcon

class XML:
    fileName:str
    fileState:bool

    def __init__(self, fileName):
        self.fileName = fileName + ".xml"
        self.openFile()

    def openFile(self):
        if os.path.exists('config.xml') == True:
            self.fileState = True
            file = open(self.fileName, "r")
        else:
            self.fileState = False

    def createFile(self, lampIPs, serverIP, serverPort, serverPass, serverPlayerName):
        rootXML = xml.Element("config")

        list = xml.Element("list")
        rootXML.append(list)

        item: xml.SubElement

        for i in lampIPs:
            item = xml.SubElement(list, "ip")
            item.text = i


        text = xml.Element("serverIP")
        text.text = serverIP
        rootXML.append(text)

        text = xml.Element("serverPort")
        text.text = str(serverPort)
        rootXML.append(text)

        text = xml.Element("serverPass")
        text.text = serverPass
        rootXML.append(text)

        text = xml.Element("serverPlayerName")
        text.text = serverPlayerName
        rootXML.append(text)

        file = open(self.fileName, "w")
        file.write(xml.tostring(rootXML, encoding="utf-8", method="xml").decode(encoding="utf-8"))
        file.close()
        
    def parsingFile(self, elements, text = True):
        tree = xml.ElementTree(file=self.fileName)
        rootXML = tree.getroot()
        for element in rootXML.iter(elements):
            if (text):
                return element.text
            return element

class Config:
    IPs:list
    
    IP:str
    Port:int
    Pass:str
    Nick:str

    def __init__(self, IPs, IP, Port, Pass, Nick):
        
        setting_lampIPs = []
        
        self.IP = IP
        self.Port = Port
        self.Pass = Pass
        self.Nick = Nick
        print('IP сервера: {}\nПорт: {}\nПароль Rcon: {}\nНикнейм: {}\nАктивные лампы:'.format(IP, Port, Pass, Nick))

        for i in IPs:
            setting_lampIPs.append(i.text)
            print(i.text)

        self.IPs = setting_lampIPs
        print('\n==============Настройки успешно загружены==============\n')

class BulbSync:
    Bulbs:list
    BulbsState:bool
    BulbsTimeOut:float

    def __init__(self, IPs):
        print('==============Происходит инициализация ламп==============\n')

        cBulb = []

        for i in IPs:
            inst = Bulb(i)
            inst.set_rgb(255, 136, 0)
            inst.set_brightness(100)
            inst.turn_on()
            cBulb.append(inst)
            print('Лампа {} проинициализирована.'.format(i))

        self.BulbsTimeOut = 1.0
        self.BulbsState = True
        self.Bulbs = cBulb
        sleep(self.BulbsTimeOut)

        print('\n==============Инициализация ламп завершена==============\n')
    
    def SyncBrightness(self, brightness):
        for i in self.Bulbs:
            i.set_brightness(brightness)
            i.set_rgb(255, 136, 0)

        print('Set bulbs brightness to {}'.format(brightness))

    def SyncTurnOFF(self):
        for i in self.Bulbs:
            i.turn_off()

        self.BulbsState = False
        print('Turn off bulbs')

    def SyncTurnON(self):
        for i in self.Bulbs:
            i.turn_on()

        self.BulbsState = True
        print('Turn on bulbs')

settingsFile = XML("config")

if settingsFile.fileState == False:
    print('==============Происходит настройка скрипта==============\n')

    setting_lampIPs = []

    setting_lampAmount = int(input('Введите количество ламп: '))

    while setting_lampAmount != 0:
        setting_lampIPs.append(input('Введите IP лампы: '))
        setting_lampAmount = setting_lampAmount - 1

    setting_ip = input('Введите IP сервера: ')
    setting_port = int(input('Введите порт сервера: '))
    setting_rcon_pass = input('Введите rcon-пароль сервера: ')
    setting_player_name = input('Введите ник игрока: ')

    settingsFile.createFile(setting_lampIPs, setting_ip, setting_port, setting_rcon_pass, setting_player_name)

    print('\n==============Настройка скрипта завершена==============\n')
    input('Перезапустите программу. Для выхода нажмите любую клавишу...\n')
    exit()
else:
    print('==============Происходит загрузка настроек==============\n')
    config = Config(settingsFile.parsingFile("list", False), settingsFile.parsingFile("serverIP"), int(settingsFile.parsingFile("serverPort")), settingsFile.parsingFile("serverPass"), settingsFile.parsingFile("serverPlayerName"))
    bulbs = BulbSync(config.IPs)

    PBrightness = 0.0

    while True:
        with MCRcon(config.IP, config.Pass, config.Port) as mcr:
            
            resp = mcr.command("getlight " + config.Nick)
            
            if resp.find(':') != -1:
                print(resp)
            else:
                MCBrightness = int(resp)

                if MCBrightness < 5:
                    PBrightness = 0
                    
                    if bulbs.BulbsState == True:
                        bulbs.SyncTurnOFF()

                else:
                    MCBrightness = MCBrightness - 5
                    LBrightness = (MCBrightness * 255) / 10

                    if PBrightness != LBrightness:
                        
                        PBrightness = LBrightness

                        if bulbs.BulbsState == False:
                            bulbs.SyncTurnON()

                        bulbs.SyncBrightness(LBrightness)

        sleep(bulbs.BulbsTimeOut)