from sys import argv
import toml


class Pake:

    def __init__(self):
        self._PROJECT_NAME = 'Test'
        self._SOURCES = None
        self._SOURCES_STR = ''
        self._EXEC_NAME = 'test'
        self._LANGUAGE = 'cpp'
        self._SOURCES_DIR = None
        self._PARSED_CONFIG = None
        self._LIBRARY_NAME = None
        self._LIBRARY_TYPE = None

    def groupData(self, exe=False, lib=False):
        """
           Parse Toml For Executable or Library Project
        """

        appType = self._PARSED_CONFIG['executable' if exe else 'library']

        if 'name' in appType.keys():
            self._PROJECT_NAME = appType['name'].strip()

        if 'sources' in appType.keys():
            self._SOURCES_STR = appType['sources'].strip()
            self._SOURCES = appType['sources'].split()
        else:
            raise Exception('Sources Not Found 404!')

        if exe:
            if 'exec_name' in appType.keys():
                self._EXEC_NAME = appType['exec_name'].strip()
        else:
            if 'lib_name' in appType.keys():
                self._LIBRARY_NAME = appType['lib_name'].strip()
            else:
                self._LIBRARY_NAME = 'lib' + self._PROJECT_NAME.lower()

        if 'language' in appType.keys():
            self._LANGUAGE = appType['language'].strip()

        if 'sources_dir' in appType.keys():
            self._SOURCES_DIR = appType['sources_dir'].strip()

        if lib:
            if 'type' in appType.keys():
                self._LIBRARY_TYPE = appType['type'].strip()
            else:
                self._LIBRARY_TYPE = 'static'

    def getName(self, text):
        """
            Get filename from path without extention
        """

        text = text.split('/')
        if len(text) <= 1:
            return text[0][0:-len(self._LANGUAGE.strip()) - 1]
        else:
            return text[-1][0:-len(self._LANGUAGE.strip()) - 1]

    def generateMakefile(self, lib=None):
        """
            Generate's MakeFile
        """

        print('generating')
        with open('./makefile', 'w') as mfile:
            mfile.write(
                f"COMPILER = {'g++' if self._LANGUAGE == 'cpp' else 'gcc'}\n")

            mfile.write(f"SOURCES = ")
            for i in self._SOURCES:
                mfile.write(f"{i} ")
            mfile.write('\n')

            if self._SOURCES_DIR is not None:
                mfile.write(f"SOURCES_DIR = {self._SOURCES_DIR}\n")

            if lib is None:
                mfile.write(f"BINARY = {self._EXEC_NAME}\n")

            mfile.write(f"PROJECT_NAME = {self._PROJECT_NAME}\n\n")

            for i in self._SOURCES:
                mfile.write(f"{self.getName(i)}.o: ")
                mfile.write(f"{i}\n")
                mfile.write('\t${COMPILER} -c ' +
                            ('-fPIC' if lib == 'shared' else '') + i + '\n')
                mfile.write(
                    f'\tcp {self.getName(i)}.o build/objs/{self.getName(i)}.o\n\n')

            names = [self.getName(i) + '.o' for i in self._SOURCES]

            mfile.write(f"{self._PROJECT_NAME}: ")
            for i in names:
                mfile.write(i + ' ')

            if lib is None:
                mfile.write("\n\t${COMPILER} -o build/${BINARY} ")
                for i in names:
                    mfile.write(i + ' ')
            else:
                if lib == 'static':
                    mfile.write(
                        f"\n\tar rcs build/static/{self._LIBRARY_NAME}.a ")
                    for i in names:
                        mfile.write(i + ' ')
                else:
                    mfile.write("\n\t${COMPILER} -shared ")
                    for i in names:
                        mfile.write(i + ' ')
                    mfile.write(f'-o build/shared/{self._LIBRARY_NAME}.so')

            mfile.write(f'\n\trm *.{self._LANGUAGE}\n\n')

            mfile.write(f'all: {self._PROJECT_NAME}')

    def parseConfig(self):
        """
            ParseData from .toml Config File in Object Fields
        """
        file_str = ""

        with open('./pakeConf.toml') as tomlFile:
            for i in tomlFile.readlines():
                file_str += i

        if file_str != '':
            self._PARSED_CONFIG = toml.loads(file_str)
        else:
            raise Exception('Your Config Is Empty!')

        if 'executable' in self._PARSED_CONFIG.keys():
            self.groupData(exe=True)
            self.generateMakefile()
        elif 'library' in self._PARSED_CONFIG.keys():
            self.groupData(lib=True)
            self.generateMakefile(lib=self._LIBRARY_TYPE)
        else:
            self.groupData(exe=True)
            self.generateMakefile()

    def start(self):
        """
            Start Pake
        """
        self.parseConfig()
        # print(self._PARSED_CONFIG)


if __name__ == '__main__':
    pake = Pake()
    pake.start()
