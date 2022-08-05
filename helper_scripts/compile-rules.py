import yara
import os
import argparse

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="")

        parser.add_argument(
            "-i",
            "--index",
            action="store",
            dest="yara_index_file",
            default=None,
            required=False,
            help="yara file that should be used",
        )

        parser.add_argument(
            "-d",
            "--dir",
            action="store",
            dest="yara_directory",
            default=None,
            required=False,
            help="index.yar that should be used",
        )

        parser.add_argument(
            "-o",
            "--output",
            action="store",
            dest="output_name",
            default='all_rules',
            required=False,
            help="output filename",
        )

        _cli_options = parser.parse_args()

        _used = 0
        _errored = 0
        if _cli_options.yara_index_file is None and _cli_options.yara_directory is None:
            raise Exception("[x] ERROR COLLECTING DATA :: option -i or -d need to be used")
        elif _cli_options.yara_index_file is not None:
            print("[-] Compiling rules...")
            rules = yara.compile(_cli_options.yara_index_file)
        elif _cli_options.yara_directory is not None:
            yara_files = {}
            print("[-] Checking yara files...")
            for root, dirs, files in os.walk(_cli_options.yara_directory):
                for file in files:
                    if file.endswith(".yar") or file.endswith(".yara") or file.endswith(".rule"):
                        try:
                            test = yara.compile(os.path.join(root, file))
                            yara_files[file.split('.')[0]] = os.path.join(root, file)
                            _used += 1
                        except Exception as e:
                            print("ERROR PROCESSING FILE: %s" % str(e))
                            _errored += 1
            try:
                print("[-] Compiling rules...")
                rules = yara.compile(filepaths=yara_files)

            except Exception as e:
                raise e
        

        _ouput = os.path.join(os.path.dirname(os.path.abspath(__file__)), str(_cli_options.output_name))
        rules.save(_ouput)
        print("-"*10, end="\n\n")
        print("[-] Done")
        print("[-] Saved To: %s" % str(_ouput))
        print("[-] File Count: %s/%s" % (_used, (_used + _errored)))
        print("[x] Error Count: %s" % _errored)
    except Exception as e:
        print(str(e))
        exit(1)
