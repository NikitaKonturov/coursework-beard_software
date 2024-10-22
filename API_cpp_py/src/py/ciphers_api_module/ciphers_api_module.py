import importlib
import importlib.util
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import platform
import sys
import os

#===================================================================================#
#============== Класс обеспечивающий взаимодействие с модулями шифров ==============#
#===================================================================================#

class CppCiphers:
    # путь к папке модулей шифров
    __pathToCiphersDir: str
    # словарь где {название модуля шифра: название шифра на английском для frontend} 
    # для запроса на шифрование в методы передаёться именно "название модуля шифра"
    __cipherTitles: dict[str, str]
 
    # метод импортирования библиотеки находящейся в директории pathToModule
    def __import_module(self, moduleTitle: str, pathToModule:str) -> None:
        try:     
            specModule= importlib.util.spec_from_file_location(moduleTitle, pathToModule) # создаём специализацию для модуля
            newModule = importlib.util.module_from_spec(specModule) # создаём из специализции сам модуль
            specModule.loader.exec_module(newModule) # делаем модуль исполяемым
            
            self.__cipherTitles[newModule.__name__] = newModule.__doc__
 
            sys.modules[newModule.__name__] = newModule # регистрируем новый модуль в текущей сесси python(возможность использовать это модуль будет только локально у этой программы)
            
        except AttributeError as err:
            print(err)    
        
    # метод загрузки всех библиотек из дериктории 
    def __load_moduls(self) -> None:
        filesList: list = os.listdir(self.__pathToCiphersDir)
        extension: str = ""
        # также обеспечение кросплатформенности(может не понадобиться)
        if(platform.system() == "Windows"):
            extension = ".pyd"
        elif(platform.system() == "Darwin"):
            extension = ".dylib"
        else:
            extension = ".so"
        
        # непосредсвено загруска всех модулей 
        for file in filesList:
            baseTitle, fileExtension = os.path.splitext(file)
            if (fileExtension == extension):
                self.__import_module(baseTitle, os.path.join(self.__pathToCiphersDir, file) )
    
    #=========================================================================#
    #============================== Конструктор ==============================#
    #=========================================================================#
    
    def __init__(self, pathToCiphersDir: str):
        if(not os.path.exists(pathToCiphersDir)):
            raise  FileExistsError(f"Path to ciphers directory was not found. Path: {pathToCiphersDir}")
        if(not os.path.isdir(pathToCiphersDir)):
            raise  FileExistsError(f"Path to ciphers is not directory was not found. Path: {pathToCiphersDir}")
        self.__pathToCiphersDir = os.path.abspath(pathToCiphersDir)
        self.__cipherTitles = {}

        self.__load_moduls()

    # Получение словаря шифров где {название модуля шифра в текущей сесси python: название шифра на английском для frontend}
    def get_ciphers_dict(self) -> dict[str, str]:
        return self.__cipherTitles
        
    # Зашифрование телерам по ключам или с генерацией ключей
    # для включения генерации шифров нужно установить keysGeneration флаг в True
    # в keyPropertys должен быть словарь полученый из .json запроса (в fastapi скорее всего Request) на шифрование
    def encript_telegrams(self, cipher: str, openTexts: list[str], keys: list[str] = [], keyPropertys: dict = {}, keysGeneration: bool = False) -> dict[str, str]:
        try:
            if (cipher in sys.modules) :
                if (keysGeneration):
                    keys = sys.modules[cipher].gen_keys(str(keyPropertys), len(openTexts)) 
                if(len(openTexts) <= len(keys)):
                    return sys.modules[cipher].encript(openTexts, keys)
            else:
                raise AttributeError(f"Ciphers {cipher} was not found....")
        except TypeError as err:
            print(err)
            return {}
        except RuntimeError as err:
            print(err)
            return {}
            
    # Функция получения шаблона свойств ключа 
    def get_key_propertys(self, cipher: str) -> JSONResponse:
        try:
            if (cipher in sys.modules):
                res: JSONResponse = JSONResponse("")
                res.body = sys.modules[cipher].get_key_propertys()
                return res
            else:
                raise AttributeError(f"Ciphers {cipher} was not found....")
        except TypeError as err:
            print(err)
            return JSONResponse("Null")
        
    # Функция расшифрования, в keysAndCipherText {ключ расшифровавние: о.т.}
    # cipher назание модуля шифра в текущей сесси python
    def decript_telegrams(self, cipher:str, keusAndCipherText: dict[str, str]) -> dict[str, str]:
        try:
            if(cipher in sys.modules):
                return sys.modules[cipher].decript(keusAndCipherText)
            else:
                raise TypeError(f"Cipher {cipher} was not found....")
        except TypeError as err:
            print(err)
            return ""
    
    
        
        