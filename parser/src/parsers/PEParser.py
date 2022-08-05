import hashlib
import os
import string
from src.helpers.logging import SubParserLogger
from pefile import PE, SECTION_CHARACTERISTICS, retrieve_flags
from typing import Any
from src.helpers import Command

class PEParser(Command):
    """
    PE Parser: Collects information using the pefile library 

    Attributes
    ----------
        - name: str
                MD5 of the sample

        - path: str
                Path to the samples location

        - logger: SubParserLogger
                SubParserLogger Object for output to console and file 

    Methods
    -------
        - convert_char(self, char): char
                Converts a char into a readable char

        - convert_to_printable(self, s): str
                Converts chars into a readable string

        - check_verinfo(self, pe): str
                Returns the examined PE's version information

        - execute(self): dict
                Collects PE Information and is executed by the command invoker

        - information(self): dict
                Parser information for compatible file types
    """
    def __init__(self, md5: str = None, path: os.path = None) -> None:
        """
        Constructor for pe parser

        Parameters
        ----------
            - md5: str
                    MD5 hash of the sample
            
            - logger: SubParserLogger
                    SubParserLogger Object for output to console and file

            - path: str
                    Full path to the location of the sample
        """
        super().__init__()
        self.name = md5
        self.path = path
        self.logger = SubParserLogger()
        
        
    def information(self):
        """
        Compatiblity information for parser

        Returns
        -------
        Dictionary
        """
        return {
                "name": "PEParser",
                "file_magic": {
                    "short_type": "pe",
                    "other_types": [
                        "pe32",
                        "ms-dos",
                        "application/x-dosexec"
                    ]
                }
            }

    # region Convert Char
    def convert_char(self, char):
        """ 
        Converts a char into a readable char

        Returns
        -------
        Char
        """
        if (char in string.ascii_letters or
           char in string.digits or
           char in string.punctuation or
           char in string.whitespace):
            return char
        else:
            return r'\x%02x' % ord(char)
    # endregion

    # region Convert To Printable
    def convert_to_printable(self, s):
        """
        Converts chars into a readable string

        Returns
        -------
        String
        """
        return ''.join([self.convert_char(c) for c in s])
    # endregion 

    # region Check Version Info
    def check_verinfo(self, pe):
        """
        Returns the examined PE's version information

        Returns
        -------
        String
        """
        ret = []

        if hasattr(pe, 'VS_VERSIONINFO'):
            if hasattr(pe, 'FileInfo'):
                for entry in pe.FileInfo:
                    if hasattr(entry, 'StringTable'):
                        for st_entry in entry.StringTable:
                            for str_entry in st_entry.entries.items():
                                ret.append(self.convert_to_printable(str_entry[0]) +
                                           ': ' +
                                          self.convert_to_printable(str_entry[1]))
                    elif hasattr(entry, 'Var'):
                        for var_entry in entry.Var:
                            if hasattr(var_entry, 'entry'):
                                ret.append(self.convert_to_printable(var_entry.entry.keys()[0]) + ': ' + var_entry.entry.values()[0])
        return '\n'.join(ret)
    # endregion

    # region Execute ( For Command Object )
    def execute(self) -> Any:
        """
        Collects PE Information and is executed by the command invoker

        Returns
        -------
        Dictionary
        """

        _pe = PE(self.path)

        with open(self.path,"rb") as sample:
            _data = {
                "md5": hashlib.md5(sample.read()).hexdigest(),
                "sha256": hashlib.sha256(sample.read()).hexdigest(),
                "number_sections": _pe.FILE_HEADER.NumberOfSections,
                "entry_point": hex(_pe.OPTIONAL_HEADER.AddressOfEntryPoint),
                "image_base": hex(_pe.OPTIONAL_HEADER.ImageBase),
                "pe_signature": hex(_pe.NT_HEADERS.Signature),
                "sections": None,
            }

        # region PE file metadata

        _file_version = self.check_verinfo(_pe)
        _data["file_version"] = ("none" if _file_version == "" else _file_version)

        # endregion

        # region Section Collection
        sections = []
        for section in _pe.sections:
            section_data = {}
            section_read = False
            section_write = False
            section_execute = False
            contains_code = False
            contains_init = False

            for permission in sorted(
                retrieve_flags(SECTION_CHARACTERISTICS, "IMAGE_SCN_")
            ):
                if getattr(section, permission[0]):
                    if permission[0] == "IMAGE_SCN_MEM_READ":
                        section_read = True
                    if permission[0] == "IMAGE_SCN_MEM_WRITE":
                        section_write = True
                    if permission[0] == "IMAGE_SCN_MEM_EXECUTE":
                        section_execute = True
                    if permission[0] == "IMAGE_SCN_CNT_CODE":
                        contains_code = True
                    if permission[0] == "IMAGE_SCN_CNT_INITIALIZED_DATA":
                        contains_init = True

            section_data = {
                "name": (section.Name.decode("utf-8").replace("\x00", "") if not section.Name is None else "<EMPTY>"),
                "virtual_address": hex(section.VirtualAddress),
                "virtual_size": hex(section.Misc_VirtualSize),
                "section_raw_size": hex(section.SizeOfRawData),
                "read": section_read,
                "write": section_write,
                "execute": section_execute,
                "contains_code": contains_code,
                "contains_init": contains_init,
                "entropy": section.get_entropy(),
            }

            sections.append(section_data)

        _data["sections"] = sections
        # endregion

        # region Atter/Import Collection
        cnt = 0

        imports = {}
        if hasattr(_pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in _pe.DIRECTORY_ENTRY_IMPORT:
                library_name = (entry.dll.decode("utf-8").replace("\x00", "") if not entry.dll is None else "<EMPTY>")
                functions = {}

                for func in entry.imports:
                    imp_name = func.name
                    if not imp_name:
                        imp_name = str(func.ordinal)
                    else:
                        imp_name = (imp_name.decode("utf-8").replace("\x00", "") if not imp_name is None else "<EMPTY>")
                    
                    functions[imp_name] = hex(func.address)

                imports[library_name] = [functions]


            _data["imports"] = imports

        _data["total_imports"] = cnt

        cnt = 0
        export_data = []
        if hasattr(_pe, "DIRECTORY_ENTRY_EXPORT"):
            for entry in _pe.DIRECTORY_ENTRY_EXPORT.symbols:
                exp_name = (entry.name.decode("utf-8") if not entry.name is None else "<EMPTY>")

                if not exp_name:
                    exp_name = str(entry.ordinal)
                else:
                    exp_name = exp_name.replace("\x00", "")

                export_data.append({exp_name: hex(entry.address)})
                cnt = cnt + 1

            _data["exports"] = export_data

        _data["total_exports"] = cnt
        # endregion
        
        return {"parser" : "PEParser", "data" : _data}
    # endregion
