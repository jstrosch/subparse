import datetime
import os
import py7zr
import shutil
from logging import Logger

class Zip(object):
    def __init__(self, directory: str, path: str, passwd: str, rm_orig: bool, logger: Logger) -> None:
        self.logger = logger
        self.path = path
        self.passwd = passwd
        self.rm_orig = rm_orig
        self.directory = directory

    def zip(self):
        self.logger.info("Starting zip creation")
        if(os.path.exists(self.path) == False):
            self.logger.info("Creating zip directory")
            os.makedirs(self.path)
            if(os.path.exists(self.path)):
                self.logger.info("Zip directory created")
            else:
                self.logger.warning("Issue creating zip directory :: Failed to create parent zip directory")
                raise Exception("Issue with creating zip directory :: Failed to create parent folder")
        
        _zip_time = datetime.datetime.now()
        _zip_name = os.path.join(self.path, ("infected-" + _zip_time.strftime("%Y-%m-%H-%X-%M-%S") + ".7z"))
        
        try:
            with py7zr.SevenZipFile(_zip_name, 'w', password=self.passwd) as archive:
                archive.set_encrypted_header(True)
                archive.writeall(self.directory, os.path.basename(self.directory))

        except Exception as e:
            self.logger.critical("ZIPPING ERROR :: " + str(e))

        if(self.rm_orig):
            try:
                self.logger.info("Deleting original samples submitted")
                shutil.rmtree(self.directory)
            except OSError as e:
                self.logger.critical("Error: %s : %s" % (self.directory, e.strerror))
        else:
            self.logger.info("Keeping original samples submitted")