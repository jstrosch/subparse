import re
import os
from typing import Any
from src.helpers.logging import SubParserLogger
from src.helpers import Command

# region Imports from oletools
import oletools.oleid
from oletools.olevba import VBA_Parser, TYPE2TAG
from oletools.olemap import *
from oletools.oleobj import OleObject
from oletools.rtfobj import RtfObjParser
from oletools.mraptor import MacroRaptor
from oletools.ooxml import XmlParser
from oletools.oleobj import process_file as is_zipfile, find_external_relationships, \
                            find_ole, get_sane_embedded_filenames, sanitize_filename, OleNativeStream

# endregion

class OLEParser(Command):
    """
    OLE Parser: Collects information using the office documents

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
        self.msword = ['application/msword']
        self.rtf = ['text/rtf']
        self.ole_output_dir = "/Users/zedo/Desktop/ole_found_embedded"
    
    def information(self):
        """
        Compatiblity information for parser

        Returns
        -------
        Dictionary
        """
        # get the file types to use from ftguess.py from oletools : use all of the content_types from the file maybe?? 
        return {
                    "name": "OLEParser",
                    "file_magic": {
                        "short_type": "ole",
                        "other_types": [
                                        "officedocument",
                                        "ms-dos",
                                        "msword",
                                        "vnd.ms-excel",
                                        "text/xml",
                                        "text/rtf",
                                        "text/plain",
                                        'application/rtf', 
                                        'text/rtf',
                                        'application/xml',
                                        'application/msword', 
                                        'application/zip',
                                        'application/vnd.openxmlformats-package.relationships+xml',
                                        'application/vnd.openxmlformats-package.core-properties+xml',
                                        'application/vnd.openxmlformats-officedocument.theme+xml',
                                        'application/vnd.openxmlformats-officedocument.extended-properties+xml',
                                        'application/vnd.ms-office.vbaProject',
                                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                        'application/vnd.ms-excel.sheet.macroEnabled.12',
                                        'application/vnd.ms-excel.sheet.binary.macroEnabled.12',
                                        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml',
                                        'application/vnd.ms-word.document.macroEnabled.main+xml',
                                        'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml',
                                        'application/vnd.ms-word.template.macroEnabledTemplate.main+xml',
                                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml',
                                        'application/vnd.ms-excel.sheet.macroEnabled.main+xml',
                                        'application/vnd.ms-excel.sheet.binary.macroEnabled.main',
                                        'application/vnd.openxmlformats-officedocument.spreadsheetml.template.main+xml',
                                        'application/vnd.ms-excel.template.macroEnabled.main+xml',
                                        'application/vnd.ms-excel.addin.macroEnabled.main+xml',
                                        'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml',
                                        'application/vnd.openxmlformats-officedocument.presentationml.slideshow.main+xml',
                                        'application/vnd.ms-powerpoint.presentation.macroEnabled.main+xml',
                                        'application/vnd.ms-powerpoint.slideshow.macroEnabled.main+xml',
                                        'application/vnd.ms-package.xps-fixeddocumentsequence+xml',
                                        'application/vnd.microsoft.portable-executable',
                                    ]
                    }
                }

    #region OLE Meta
    def _olemeta(self) -> dict:
        _data = {
                    "doc_summary" : {
                        'codepage_doc' : None,
                        'category' : None,
                        'presentation_target' : None,
                        'bytes' : None,
                        'lines' : None,
                        'paragraphs' : None,
                        'slides' : None,
                        'notes' : None,
                        'hidden_slides' : None,
                        'mm_clips' : None,
                        'scale_crop' : None,
                        'heading_pairs' : None,
                        'titles_of_parts' : None,
                        'manager' : None,
                        'company' : None,
                        'links_dirty' : None,
                        'chars_with_spaces' : None,
                        'unused' : None,
                        'shared_doc' : None,
                        'link_base' : None,
                        'hlinks' : None,
                        'hlinks_changed' : None,
                        'version' : None,
                        'dig_sig' : None,
                        'content_type' : None,
                        'content_status' : None,
                        'language' : None,
                        'doc_version' : None
                    },
                    "summary_attribs" : {
                        'codepage': None, 
                        'title': None, 
                        'subject': None, 
                        'author': None,
                        'keywords': None, 
                        'comments': None,
                        'template': None, 
                        'last_saved_by': None, 
                        'revision_number': None, 
                        'total_edit_time': None,
                        'last_printed': None, 
                        'create_time': None, 
                        'last_saved_time': None, 
                        'num_pages': None,
                        'num_words': None, 
                        'num_chars': None, 
                        'thumbnail': None, 
                        'creating_application': None,
                        'security': None
                    }
                }

        self.logger.debug("[OLEPARSER] %s [✔] OLEMETA" % self.name)
        _ole = olefile.OleFileIO(self.path)
        _meta = _ole.get_metadata()

        for prop in _meta.SUMMARY_ATTRIBS:
            value = getattr(_meta, prop)
            if value is not None:
                _data['doc_summary'][prop] = str(value)

        for prop in _meta.DOCSUM_ATTRIBS:
            value = getattr(_meta, prop)
            if value is not None:
                _data['summary_attribs'][prop] = str(value)
        _ole.close()

        return _data
    #endregion

    #region DT to String
    def dt2str(self, dt):
        """
        Convert a datetime object to a string for display, without microseconds

        :param dt: datetime.datetime object, or None
        :return: str, or None
        """
        if dt is None:
            return None
        dt = dt.replace(microsecond=0)
        return str(dt)
    #endregion

    #region OLE Time
    def _oletimes(self) -> list:
        self.logger.debug("[OLEPARSER] %s [✔] OLETIME" % self.name)
        _data = []
        _olefile = olefile.OleFileIO(self.path)
        try:
            for obj in _olefile.listdir(streams=True, storages=True):
                _m = self.dt2str(_olefile.getmtime(obj))
                _c = self.dt2str(_olefile.getctime(obj))
                _tmp = {
                    "name" : '/'.join(obj),
                    "modified_time" : _m if _m != None else 'N/A',
                    "creatiion_time" : _c if _c != None else 'N/A'
                }

                _data.append(_tmp)
        except Exception as e:
            self.logger.error("[OLEPARSER] ERROR (OLETIMES) :: %s :: %s" % (str(e), self.name))

        finally:
            _olefile.close()
        return _data
    #endregion

    #region OLE OBJ
    def _ole_obj(self) -> dict:
        # **********
        # Container: None
        # Filename: ./018367.docx
        # Data: None
        # **********
        _links = {}
        _embedded_files = []
        # err_stream, err_dumping, did_dump = \
        #     OLEObj_process(self.path, None, None)
        err_stream = False
        err_dumping = False
        did_dump = False
        index = 1

        # sanitize filename, leave space for embedded filename part
        sane_fname = sanitize_filename(self.path, max_len=255-5) or\
            'NONAME'

        base_dir = os.path.dirname(self.path)
        output_path = os.path.join(base_dir, ("%s_extracted" % sane_fname.replace(".",'_')))
        fname_prefix = os.path.join(base_dir, sane_fname)

        xml_parser = None
        if is_zipfile(self.path):
            xml_parser = XmlParser(self.path)
            for relationship, target in find_external_relationships(xml_parser):
                did_dump = True
                _tmp = {
                        relationship : target
                    }
                if relationship in _links.keys():
                    _links[relationship].append(_tmp)
                else:
                    _links[relationship] = []
                    _links[relationship].append(_tmp)

        for ole in find_ole(self.path, None, xml_parser):
            if ole is None:    # no ole file found
                continue
            for path_parts in ole.listdir():
                stream_path = '/'.join(path_parts)
                if path_parts[-1].lower() == '\x01ole10native':
                    stream = None
                    try:
                        stream = ole.openstream(path_parts)
                        opkg = OleNativeStream(stream)
                        # leave stream open until dumping is finished
                    except Exception:
                        err_stream = True
                        if stream is not None:
                            stream.close()
                        continue

                    if opkg.is_link:
                        continue

                    for embedded_fname in get_sane_embedded_filenames(
                        opkg.filename, opkg.src_path, opkg.temp_path,
                        255 - len(sane_fname) - 1, index):
                        fname = fname_prefix + '_' + embedded_fname
                        if not os.path.isfile(fname):
                            break
                    _tmp = {
                                'filename' : '',
                                'saved_to' : '',
                                'saved_successful' : ''
                            }
                    try:
                        _output_file = os.path.join(self.ole_output_dir, os.path.basename(fname))

                        _tmp['filename'] = os.path.basename(fname)
                        _tmp['saved_to'] = _output_file
                        _tmp['saved_successful'] = 'True'

                        with open(_output_file, 'wb') as writer:
                            n_dumped = 0
                            next_size = min(4096, opkg.actual_size)
                            while next_size:
                                data = stream.read(next_size)
                                writer.write(data)
                                n_dumped += len(data)
                                if len(data) != next_size:
                                    self.logger.error('{0} :: Wanted to read {1}, got {2}'
                                                .format(self.name, next_size, len(data)))
                                    break
                                next_size = min(4096,
                                                opkg.actual_size - n_dumped)
                        did_dump = True
                    except Exception as exc:
                        err_dumping = True
                        _tmp['saved_successful'] = 'False'
                    finally:
                        stream.close()
                        _embedded_files.append(_tmp)
                index += 1
        return { 'links' : _links, 'embedded' : _embedded_files }

    #endregion

    #region MRAPTOR Start
    def _mraptor(self):
        _codes = {
            "Result_NoMacro" : {
                "exit_code" : "0",
                "color" : 'green',
                "name" : 'No Macro'
            },
            "Result_NotMSOffice" :{
                "exit_code" : "1",
                "color" : 'green',
                "name" : 'Not MS Office'
            },
            "Result_MacroOK" :{
                "exit_code" : "2",
                "color" : 'cyan',
                "name" : 'Macro OK'
            },
            "Result_Suspicious" :{
                "exit_code" : "4",
                "color" : 'red',
                "name" : 'SUSPICIOUS'
            },
            
        }

        try:
            vba_parser = VBA_Parser(filename=self.path, data=None, container=None)
            filetype = TYPE2TAG[vba_parser.type]
            _data = {}
            result = {}
            if vba_parser.detect_vba_macros():
                vba_code_all_modules = ''
                try:
                    vba_code_all_modules = vba_parser.get_vba_code_all_modules()
                except Exception as e:
                    # log.error('Error when parsing VBA macros from file %r' % full_name)
                    result = _codes["Result_Error"]
                    # t.write_row([result.name, '', TYPE2TAG[vba_parser.type], full_name],
                    #             colors=[result.color, None, None, None])
                    # t.write_row(['', '', '', str(e)],
                    #             colors=[None, None, None, result.color])
                    # continue
                if result == {}:
                    mraptor = MacroRaptor(vba_code_all_modules)
                    mraptor.scan()
                    if mraptor.suspicious:
                        result = _codes["Result_Suspicious"]
                    else:
                        result = _codes["Result_MacroOK"]

                    _flags = mraptor.get_flags()
                    _data['macro_type'] = result['name']
                    _data['macro_flags'] = [{
                                            'flags' : _flags,
                                            'auto_exec' : "True" if "A" in _flags else "False",
                                            'write' : "True" if "W" in _flags else "False",
                                            'execute' : "True" if "X" in _flags else "False"
                                        }]
                    _data['file_type'] = filetype.replace(':','')
        except Exception as e:
            self.logger.error("[OLEPARSER] %s VBA Parser :: %s" % (self.name, str(e)))
        finally:
            vba_parser.close()
        return _data
    #endregion MRAPTOR End

    def execute(self) -> Any:
        """
        Collects OLE Information and is executed by the command invoker

        Returns
        -------
        Dictionary
        """
        _data = {}

        try:
            _isOLE = False
            _isRTF = False

            #region OLEID Start
            _indicators = []
            _vba = {}
            _meta = {}
            _times = []
            _rtf = []
            _ole_obj_data = {}
            _mraptor = {}

            _data['meta_data'] = {}
            _data['mraptor'] = {}
            _data['rtf'] = []
            _data['times'] = []
            _data['indicators'] = []
            _data['vba'] = {}
            _data['ole_obj'] = {}

            try:
                oid = oletools.oleid.OleID(self.path)
                indicators = oid.check()
                for i in indicators:
                    _i = i.__dict__
                    del _i['type']
                    _i['value'] = str(_i['value'])
                    _indicators.append(_i)
                    if i.value == 'OLE':
                        _isOLE = True
                    elif i.value == "RTF":
                        _isRTF = True

                self.logger.debug("[OLEPARSER] %s [✔] Collected OLEID data" % self.name)
                _data['indicators'] = _indicators
                #endregion OLEID End

            except Exception as e:
                print(e)
                _isOLE = False
                _isRTF = True

            
            if _isOLE:
                #region Getting Meta Start
                _meta = self._olemeta()
                #endregion Getting Meta End

                #region VBA Start

                vbaparser = VBA_Parser(self.path)
                if vbaparser.detect_vba_macros():
                    self.logger.debug("[OLEPARSER] %s [✔] OLEVBA :: Found Macros" % self.name)
                    _vba['macros'] = {
                                        "macro_abilities" : [],
                                        "general" : {},
                                        "macros" : []
                                    }
                    # _vba['macros']['macros'] = []
                    for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
                        _tmp = {
                            'filename' : vba_filename,
                            'ole_stream' : stream_path,
                            'code' : {
                                'length' : str(len(vba_code)) if vba_code != None else '0',
                                'data' : vba_code
                            }
                        }
                        _vba['macros']['macros'].append(_tmp)

                    results = vbaparser.analyze_macros()
                    
                    self.logger.debug("[OLEPARSER] %s [✔] Collected OLEVBA :: Macro General" % self.name)
                    _vba['macros']['general']['auto_exec'] = vbaparser.nb_autoexec
                    _vba['macros']['general']['suspicious'] = vbaparser.nb_suspicious
                    _vba['macros']['general']['ioc'] = vbaparser.nb_iocs
                    _vba['macros']['general']['hex_obfuscated'] = vbaparser.nb_hexstrings
                    _vba['macros']['general']['base_obfuscated'] = vbaparser.nb_base64strings
                    _vba['macros']['general']['dridex_obfuscated'] = vbaparser.nb_dridexstrings
                    _vba['macros']['general']['vba_obfuscated'] = vbaparser.nb_vbastrings

                    for kw_type, keyword, description in results:
                        _ability = {
                                    "type" : kw_type,
                                    "keyword" : keyword,
                                    "description" : description
                                }
                        _vba['macros']['macro_abilities'].append(_ability)

                    self.logger.debug("[OLEPARSER] %s [✔] Collected OLEVBA :: Macro Abilities" % self.name)
                else:
                    self.logger.debug("[OLEPARSER] %s [X] Collected OLEVBA :: No Macros Found" % self.name)

                vbaparser.close()
                #endregion VBA End

                

                #region Get Times Start
                _times = self._oletimes()
                #endregion Get Times end

                #region OLEObj
                _ole_obj_data = self._ole_obj()
                #endregion

                #region MRAPTOR
                _mraptor = self._mraptor()
                #endregion

            # Will need to use rtfp = RtfObjParser(data)
            if _isRTF:
                rtfdata = open(self.path, 'rb').read()
                rtfp = RtfObjParser(rtfdata)
                rtfp.parse()
                for rtfobj in rtfp.objects:
                    _tmp = {}
                    if rtfobj.is_ole:
                        _tmp['start'] = rtfobj.__dict__['start']
                        _tmp['end'] = rtfobj.__dict__['end']
                        
                        _tmp['format_type'] = None
                        
                        if rtfobj.__dict__['format_id'] == OleObject.TYPE_EMBEDDED:
                            _tmp['format_type'] = '(Embedded)'
                        elif rtfobj.__dict__['format_id'] == OleObject.TYPE_LINKED:
                            _tmp['format_type'] = '(Linked)'
                        else:
                            _tmp['format_type'] = '(Unknown)'

                        _tmp['urls'] = []

                        if rtfobj.__dict__['oledata_size'] is None:
                            _tmp['oledata_size'] = None
                        else:
                            _tmp['oledata_size'] = ("%d" % rtfobj.__dict__['oledata_size'])

                        try: 
                            _tmp['class_name'] = rtfobj.__dict__['class_name'].decode('utf8')
                        except Exception as e:
                            _tmp['class_name'] = str(rtfobj.__dict__['class_name'])[2:-1]

                        if rtfobj.__dict__['class_name'] == b'OLE2Link':
                            _tmp['warning'] = 'Possibly an exploit for the OLE2Link vulnerability (VU#921560, CVE-2017-0199)'
                            urls = []
                            pat = re.compile(b'(?:[\\x20-\\x7E][\\x00]){3,}')
                            words = [w.decode('utf-16le') for w in pat.findall(rtfobj.oledata)]
                            for w in words:
                                if "http" in w:
                                    urls.append(w)
                            urls = sorted(set(urls))
                            _tmp['urls'] = urls
                            if urls:
                                ole_column ='URL extracted: ' + ', '.join(urls)
                        elif rtfobj.__dict__['class_name'].lower().startswith(b'equation.3'):
                            _tmp['warning'] = 'Possibly an exploit for the Equation Editor vulnerability (VU#421280, CVE-2017-11882)'


                        _tmp['is_package'] = str(rtfobj.__dict__['is_package'])
                        _tmp['cve'] = None
                        if rtfobj.__dict__['clsid'] != None:
                            _tmp['clsid'] = rtfobj.__dict__['clsid']
                            _tmp['cve'] = rtfobj.clsid_desc
                        _rtf.append(_tmp)
                #region RTF End

            #region Adding sample to data to return
            _data['meta_data'] = _meta
            _data['mraptor'] = _mraptor
            _data['rtf'] = _rtf
            _data['times'] = _times
            _data['vba'] = _vba
            _data['ole_obj'] = _ole_obj_data
            #endregion

        except Exception as e:
            self.logger.error("[OLEPARSER] ERROR :: %s :: %s" % (str(e), str(self.name)))


        return { "parser" : "OLEParser", "data" : _data }