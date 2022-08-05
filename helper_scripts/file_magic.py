import magic 
import argparse
from os import listdir
from os.path import isfile, join

class FILEMAGIC():
    def __init__(self, path) -> None:
        self.path = path
    
    def get_magic(self):
        onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        for _file in onlyfiles:
            _full_path = join(self.path, _file)
            _magic_mime = magic.from_file(_full_path, mime=True)
            _magic = magic.from_file(_full_path)

            print("*"*10)
            print("- File: %s" % (_file))
            print("-----")
            print("- Magic: %s" % (_magic))
            print("-----")
            print("- Mime: %s" % (_magic_mime))
            print("*"*10)
            

if __name__ == "__main__":
    try:
        #region Parser Arguments
        parser = argparse.ArgumentParser(description="")

        parser.add_argument(
            "-d",
            "--directory",
            action="store",
            dest="directory",
            default="",
            help="Directory to get file magic(s)",
            required=True
        )

        cli_options = parser.parse_args()

        _magic = FILEMAGIC(cli_options.directory)
        _magic.get_magic()
    except Exception as e:
        print(str(e))


    
