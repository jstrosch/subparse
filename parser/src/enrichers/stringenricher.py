import re
import mmap
import contextlib
import floss.main as floss
from src.helpers import Command
from src.helpers.logging import SubParserLogger
from src.config.configuration import Configuration

class STRINGEnricher(Command):
    """
    String Enricher Command - Collects data from the strings

    Attributes
    ----------
        - md5: str
                Samples MD5 hash

        - data: dict
                Collected data from the Abuse API call

        - logger: SubParserLogger
                SubParserLogger Object for output to console and file 
    
    Methods
    -------
        - execute(self): dict
                Used by the Commands Invoker to execute the underlying Abuse Enrichers collection process

        - information(self): dict
                Enricher information for compatible file types

    """
    def __init__(self, md5: str, path: str):
        """
        Constructor for abstract enricher

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
        self.md5 = md5
        self.path = path
        self._config = Configuration()
        self.logger = SubParserLogger("STRING-ENRICHER")
        self.min_length = 6
        self.data = {
            'audio' : [],
            'code' : [],
            'command_line_arguments' : [],
            'compressed' : [],
            'exec_files' : [],
            'misc_files' : [],
            'images' : [],
            'ip' : [],
            'ip_port' : [],
            'web' : [],
            'work' : []
        }

        self.regex_strings = {
            'audio' : [
                r"(?:[^<>:\"\*\/\\\|\?\n]+\.)(?:mp4|mpg|mpeg|avi|mp3|wav|aac|adt|adts|aif|aifc|aiff|cda|flv|m4a)(?:\b)"
            ],
            'images' : [
                r"(?:[^<>:\"\*\/\\\|\?\n]+\.)(?:jpg|gid|gmp|jpeg|png|tif|gif|bmp|tiff|svg)(?:\b)"
            ],
            'exec_files' : [
                r"(?:[^<>:\"\*\/\\\|\?]+\.)(?:bin|log|exe|dll|txt|ini|ico|lnk|tmp|bak|cfg|config|msi|dat|rtf|cer|sys|cab|iso|db|asp|aspx|html|htm|rdp|temp)(?:\b)"
            ],
            'code' : [
                r"(?:[^<>:\"\*\/\\\|\?\n]+\.)(?:cpp|java|js|php|py|bat|c|pyc|py3|pyw|jar|eps|vbs|scr|cs|ps1|ps1xml|ps2|ps2xml|psc1|psc2|r|rb|php3|vbx)(?:\b)"
            ],
            'compressed' : [
                r"(?:[^<>:\"\*\/\\\|\?\n]+\.)(?:7z|zip|rar|tar|tar\.gz|gzip|bzip2|wim|xz)(?:\b)"
            ],
            'work' : [
                r"(?:[^<>:\"\*\/\\\|\?\n]+\.)(?:xls|xlsm|xlsx|ppt|pptx|doc|docx|pdf|wpd|odt|dodp|pps|key|diff|docm|eml|email|msg|pst|pub|sldm|sldx|wbk|xll|xla|xps|dbf|accdb|accde|accdr|accdt|sql|sqlite|mdb)(?:\b)"
            ],
            'misc_files' : [
                r"(?:[^<>:\"\*\/\\\|\?\n]+\.)(?:reg|inf|application|gadget|msp|hta|cpl|msc|vb|vbe|jse|ws|wsf|wsc|wsh|scf|sh|csv|vmdk|cmx|vdi|yaml|raw|msh|msh1|msh1xml|msh2|msh2xml|mshxml|mst|ops|osd|pcd|pl|plg|prf|prg|printerexport|psd1|psdm1|pssc|pyo)(?:\b)", # find_misc1
                r"(?:[^<>:\"\*\/\\\|\?\n]+\.)(?:swf|aru|shs|pgm|pif|vba|hlp|apk|dotm|xltm|xlam|pptm|potm|ppam|ppsm|css|chm|drv|vxd|isp|its|jnlp|ksh|mad|maf|mag|mam|maq|mar|mas|mat|mau|mav|maw|mcf|mda|mde|mdt|mdw|mdz|msu)(?:\b)", # find_misc2
                r"(?:[^<>:\"\*\/\\\|\?\n]+\.)(?:md|info|epub|tga|url|sym|a\.out|btm|lua|ade|adp|app|appcontent-ms|appref-ms|bas|cdxml|cmd|cnt|crt|csh|der|diagcab|fxp|grp|hpj|ins|settingcontent-ms|shb|theme|udl|vbp|vsmacros|vsw|webpnp|website|wsb|xbap|xnk|pyz|sct|pyzw)(?:\b)" # find_misc3
            ],
            'ip' : [
                r'''\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b''',
                r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
            ],
            'ip_port' : [
                r'[0-9]+(?:\.[0-9]+){3}:[0-9]+'
            ],
            'web' : [
                r"(?:(?:(?:http|https):\/\/|www)(?:[^\s\'\",]+))",
                r"(?:www)?(?:[^\\\s\'\",])+\.(?:cn|bd|it|ul|cd|ch|br|ml|ga|us|pw|eu|cf|uk|ws|zw|ke|am|vn|tk|gq|pl|ca|pe|su|de|me|au|fr|be|pk|th|it|nid|tw|cc|ng|tz|lk|sa|ru)",
                r"(?:www)?(?:[^\\\s\'\",])+\.(?:xyz|top|bar|cam|sbs|org|win|arn|moe|fun|uno|mail|stream|club|vip|ren|kim|mom|pro|gdn|biz|ooo|xin|cfd|men|com|net|edu|gov|mil|org|int)",
                r"(?:www)?(?:[^\\\s\'\",])+\.(?:host|rest|shot|buss|cyou|surf|info|help|life|best|live|archi|acam|load|part|mobi|loan|asia|jetzt|email|space|site|date|want|casa|link|bond|store|click|work|mail)",
                r"(?:www)?(?:[^\\\s\'\",])+\.(?:monster|name|reset|quest|finance|cloud|kenya|accountants|support|solar|online|yokohama|ryukyu|country|download|website|racing|digital|tokyo|world)",
                r"(?:(?:ftp):\/\/(?:[\S]+))"
            ],
            'command_line_arguments' : [
                r"(?:(?:cmd(?:\.exe)?)(?:\s+(?:\/[cCkKaAuUdDxXqQ]|\/[eEfFvV]:..|\/[tT]:[0-9a-fA-F])+)+)",
                r"(?:powershell(?:\.exe)?)",
                r"(?:reg(?:\.exe)?(?:\s+(?:add|compare|copy|delete|export|import|load|query|restore|save|unload))+)",
                r"(?:net(?:\.exe)?(?:\s+(?:accounts|computer|config|continue|file|group|help|helpmsg|localgroup|name|pause|print|send|session|share|start|statistics|stop|time|use|user|view))+)",
                r"(?:schtasks(?:\.exe)?\s+)(?:\/(?:change|create|delete|end|query|run))",
                r"(?:netsh(?:\.exe)?\s+(?:abort|add|advfirewall|alias|branchcache|bridge|bye|commit|delete|dhcpclient|dnsclient|dump|exec|exit|firewall|help|http|interface|ipsec|ipsecdosprotection|lan|namespace|netio|offline|online|popd|pushd|quit|ras|rpc|set|show|trace|unalias|    wfp|winhttp|winsock))"
            ],

        }

    def information(self):
        """
        Compatiblity information for enricher

        Returns
        -------
        Dictionary
        """
        return {"name": "STRINGEEnricher"}
        

    def execute(self) -> dict:
        """
        Requests information about the malwares hash and returns the json request back to the invoker

        Returns
        -------
        Dictionary
        """
        try:
            self._pull_strings()
        except Exception as e:
            self.logger.exception(str(e))
            self.data = None
        return {"enricher": "STRINGEnricher", "data": self.data} 

    def _pull_strings(self):

        try:
            analysis = floss.Analysis(
                enable_static_strings=floss.is_string_type_enabled(floss.StringType.STATIC, [], [t.value for t in floss.StringType]),
                enable_stack_strings=floss.is_string_type_enabled(floss.StringType.STACK, [], [t.value for t in floss.StringType]),
                enable_tight_strings=floss.is_string_type_enabled(floss.StringType.TIGHT, [], [t.value for t in floss.StringType]),
                enable_decoded_strings=floss.is_string_type_enabled(floss.StringType.DECODED, [], [t.value for t in floss.StringType])
            )
            
            results = floss.ResultDocument(metadata=floss.Metadata(file_path=self.path, min_length=self.min_length), analysis=analysis)

            with open(self.path, "rb") as f:
                with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
                    static_strings = list(floss.extract_ascii_unicode_strings(buf))

                results.strings.static_strings = static_strings

            _cleanedStrings = []
            for _ss in results.strings.static_strings:
                if len(_ss.string) >= self.min_length:
                    _cleanedStrings.append(_ss)

            for key, regex_list in self.regex_strings.items():
                for r in regex_list:
                    for i in _cleanedStrings:
                        newlist = re.findall(r, i.string)
                        if newlist != []:
                            for found in newlist:
                                if found not in self.data[key] and found != '':
                                    self.data[key].append(found)                            

        except Exception as e:
            self.logger.exception("Error opening file : %s" % str(e))
