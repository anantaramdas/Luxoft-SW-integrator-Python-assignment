import sys
from classes.Unpacker import Unpacker


def main():
    if len(sys.argv) <= 2 or sys.argv[1] == '--help' or sys.argv[1] == '-h':
        # User did not specified command line arguments or requested help
        if sys.argv[1] != '--help' and sys.argv[1] != '-h':
            print(
                '\033[91mTo run this program please provide path to archive/folder of archives/or space separated '
                'list of archives\033[0m')

        print('Syntax: python main.py [destanation-path] [path-to-archive(-s)/path-to-folder(-s)]')
        print('\t-h --help:\tShow this help')
        print('')

        print('Use following as example:\n')
        print('\tpython \033[1mmain.py\033[0m archive.zip')
        print('\tpython \033[1mmain.py\033[0m \\path\\to\\archieve\\archive.zip')
        print('\tpython \033[1mmain.py\033[0m \\path\\to\\archieve\\folder-with-archives')
        print('\tpython \033[1mmain.py\033[0m archive1.zip archive2.zip archive3.zip')
        print('')
        exit(-1)
    else:
        destination_dir = sys.argv[1]      # Getting path with destination directory
        list_of_archives = sys.argv[2:]    # Getting list of passed arguments to script

        up = Unpacker(list_of_archives)
        up.unpack(destination_dir)


if __name__ == "__main__":
    main()
