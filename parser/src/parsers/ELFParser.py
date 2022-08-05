import os
import traceback
from src.helpers.logging import SubParserLogger
from src.helpers import Command

# Needed imports for functions from the pyelftools developer helpers
import itertools
# Note: zip has different behaviour between Python 2.x and 3.x.
# - Using izip ensures compatibility.
try:
    from itertools import izip
except:
    izip = zip
from elftools import __version__
from elftools.common.exceptions import ELFParseError
from elftools.common.py3compat import (
        ifilter, byte2int, bytes2str, itervalues, iterbytes)
from elftools.elf.elffile import ELFFile
from elftools.elf.dynamic import DynamicSection
from elftools.elf.enums import ENUM_D_TAG
from elftools.elf.segments import InterpSegment
from elftools.elf.sections import (
    NoteSection, SymbolTableIndexSection
)
from elftools.elf.gnuversions import (
    GNUVerSymSection, GNUVerDefSection,
    GNUVerNeedSection,
    )
from elftools.elf.relocation import RelocationSection
from elftools.elf.descriptions import (
    describe_ei_class, describe_ei_data, describe_ei_version,
    describe_ei_osabi, describe_e_type, describe_e_machine,
    describe_e_version_numeric, describe_p_flags,
    describe_rh_flags, describe_sh_type, describe_sh_flags,
    describe_reloc_type, describe_dyn_tag,
    describe_dt_flags, describe_dt_flags_1, describe_ver_flags, describe_note,
    describe_attr_tag_arm
    )
from elftools.elf.constants import E_FLAGS
from elftools.elf.constants import E_FLAGS_MASKS
from elftools.elf.constants import SH_FLAGS
from elftools.elf.constants import SHN_INDICES
from elftools.dwarf.descriptions import (
    describe_reg_name, describe_attr_value, set_global_machine_arch,
    describe_CFI_instructions, describe_CFI_register_rule,
    describe_CFI_CFA_rule, describe_DWARF_expr
    )
from elftools.dwarf.constants import (
    DW_LNS_copy, DW_LNS_set_file, DW_LNE_define_file)
from elftools.dwarf.locationlists import LocationParser, LocationEntry
from elftools.dwarf.callframe import CIE, FDE, ZERO
from elftools.ehabi.ehabiinfo import GenericEHABIEntry
# end of pyelftools developer helpers imports 


class ELFParser(Command):
    def __init__(self, md5: str = None, path: os.path = None) -> None:
        """
        Constructor for pe parser

        Parameters
        ----------
            - md5: str
                    MD5 hash of the sample
            
            - logger: Logger
                    Logger Object for output to console and file

            - path: str
                    Full path to the location of the sample
        """
        super().__init__()
        self.name = md5
        self.path = path
        self.logger = SubParserLogger()
        self.elffile = None
        self._dwarfinfo = None
        self._versioninfo = None
        self._shndx_sections = None
        self.data = {}

    def information(self):
        """
        Compatiblity information for parser

        Returns
        -------
        Dictionary
        """
        return {
                    "name": "ELFParser",
                    "file_magic": {
                        "short_type": "elf",
                        "other_types": [
                            "elf",
                            "application/x-executable"
                        ]
                    }
                }

    def execute(self) -> dict:
        """
        Collects ELF Information and is executed by the command invoker

        Returns
        -------
        Dictionary
        """

        try:
            _elfFile = ELFFile(open(self.path, 'rb'))
            self.elffile = _elfFile

        except ELFParseError as elfe:
            self.logger.critical("ERROR WITH UNPACKING FILE! COULD BE PACKED :: " + str(elfe))
            return {"parser" : "ELFParser", "data" : {"ERROR": "ERROR WITH UNPACKING FILE! COULD BE PACKED"}}
        except Exception as e:
            self.logger.critical(str(e))
            return {"parser" : "ELFParser", "data" : {"ERROR": str(e)}}


        self.data['general_info'] = {}
        self.data['program_headers'] = { 'segments' : {}, 'sections' : {}}
        self.data['section_headers'] = []
        self.data['notes'] = []
        self.data['arch_specific'] = {}
        self.data['version_info'] = {}
        self.data['arm_unwind_info'] = {}
        self.data['relocation_data'] = []
        self.data['dynamic_tags'] = []

        try:
            self.logger.debug("[ELFParser] Collecing General Information")
            self.collect_general_information()
        except Exception as e:
            self.logger.warning("[ELFPARSER] ERROR COLLECTING GENERAL INFO :: " + str(e))
            traceback.print_exc()

        try:
            self.logger.debug("[ELFParser] Collecing Program Header Information")
            self.collect_program_header_data()
        except Exception as e:
            self.logger.warning("[ELFPARSER] ERROR COLLECTING PROGRAM HEADER INFO :: " + str(e))
            traceback.print_exc()

        try:
            self.logger.debug("[ELFParser] Collecing Section Header Information")
            self.collect_section_header_data()
        except Exception as e:
            self.logger.warning("[ELFPARSER] ERROR COLLECTING SECTION HEADER INFO :: " + str(e))
            traceback.print_exc()

        try:
            self.logger.debug("[ELFParser] Collecing Note Information")
            self.collect_notes_data()
        except Exception as e:
            self.logger.warning("[ELFPARSER] ERROR COLLECTING NOTE INFO :: " + str(e))
            traceback.print_exc()

        try:
            self.logger.debug("[ELFParser] Collecing Architecture Specific Information")
            self.collect_arch_specific_data()
        except Exception as e:
            self.logger.warning("[ELFPARSER] ERROR COLLECTING ARCH. SPEC. INFO :: " + str(e))
            traceback.print_exc()

        try:
            self.logger.debug("[ELFParser] Collecing Version Information")
            self.collect_version_info()
        except Exception as e:
            self.logger.warning("[ELFPARSER] ERROR COLLECTING VERSION INFO :: " + str(e))
            traceback.print_exc()

        try:
            self.logger.debug("[ELFParser] Collecing ARM Unwind Information")
            self.collect_arm_unwind()
        except Exception as e:
            self.logger.warning("[ELFPARSER] ERROR COLLECTING ARM UNWIND INFO :: " + str(e))
            traceback.print_exc()

        try:
            self.logger.debug("[ELFParser] Collecing RELOCATION(S) Information")
            self.display_relocations()
        except Exception as e:
            self.logger.warning("[ELFPARSER] ERROR COLLECTING RELOCATION(S) INFO :: " + str(e))
            traceback.print_exc()


        try:
            self.logger.debug("[ELFParser] Collecing DYNAMIC TAGS Information")
            self.display_dynamic_tags()
        except Exception as e:
            self.logger.warning("[ELFPARSER] ERROR DYNAMIC TAGS INFO :: " + str(e))


        return {"parser" : "ELFParser", "data" : self.data}


    # region Collect General ELF Information
    def collect_general_information(self):
        """ Display the ELF file header
        """
        self.data['general_info']['magic_bytes'] = ''.join('%2.2x' % byte2int(b)
                   for b in self.elffile.e_ident_raw)

        header = self.elffile.header
        e_ident = header['e_ident']
        self.data['general_info']['ei_data'] = describe_ei_data(e_ident['EI_DATA'])
        self.data['general_info']['ei_version'] = describe_ei_version(e_ident['EI_VERSION'])
        self.data['general_info']['ei_osabi'] = describe_ei_osabi(e_ident['EI_OSABI'])
        self.data['general_info']['ei_abiversion'] = e_ident['EI_ABIVERSION']
        self.data['general_info']['e_type'] = "None" if self.elffile.get_section_by_name('.dynamic') is None else describe_e_type(header['e_type'], self.elffile)
        self.data['general_info']['e_machine'] = describe_e_machine(header['e_machine'])
        self.data['general_info']['e_version_numeric'] = describe_e_version_numeric(header['e_version'])
        self.data['general_info']['entry_point'] = self._format_hex(header['e_entry'])
        self.data['general_info']['program_headers_start'] = str(header['e_phoff']) + " (bytes into file)"
        self.data['general_info']['program_sections_start'] = str(header['e_shoff']) + " (bytes into file)"
        self.data['general_info']['flags_hex'] = self._format_hex(header['e_flags'])
        self.data['general_info']['flags_decoded'] = self._decode_flags(header['e_flags'])
        self.data['general_info']['e_ehsize'] = header['e_ehsize']
        self.data['general_info']['e_pheadersize'] = header['e_phentsize']
        self.data['general_info']['e_phnum'] = header['e_phnum']
        self.data['general_info']['e_sheadersize'] = header['e_shentsize']
        self.data['general_info']['e_shnum'] = header['e_shnum']
        self.data['general_info']['e_numsections'] = self.elffile.num_sections()
        self.data['general_info']['e_shstrndx'] = header['e_shstrndx']
        self.data['general_info']['shstrndx'] = self.elffile.get_shstrndx()
    # endregion 
        
    # region Collect Header ELF Information
    def collect_program_header_data(self, show_heading=True):
        """ Display the ELF program headers.
            If show_heading is True, displays the heading for this information
            (Elf file type is...)
        """
        if self.elffile.num_segments() == 0:
            self.data['program_headers'] = None
            return

        # Now the entries
        for segment in self.elffile.iter_segments():
            self.data['program_headers']['segments'][segment['p_type']] = []

        for segment in self.elffile.iter_segments():
            _segment = {}

            if self.elffile.elfclass == 32:
                _segment['offset'] = self._format_hex(segment['p_offset'], fieldsize=6)
                _segment['physical_address'] = self._format_hex(segment['p_paddr'], fullhex=True)
                _segment['virtual_address'] = self._format_hex(segment['p_vaddr'], fullhex=True)
                _segment['file_size'] = self._format_hex(segment['p_filesz'], fieldsize=5)
                _segment['memory_size'] = self._format_hex(segment['p_memsz'], fieldsize=5)
                _segment['flags'] = describe_p_flags(segment['p_flags'])
                _segment['align'] = self._format_hex(segment['p_align'])
            else: # 64
                _segment['offset'] = self._format_hex(segment['p_offset'], fullhex=True)
                _segment['physical_address'] = self._format_hex(segment['p_paddr'], fullhex=True)
                _segment['virtual_address'] = self._format_hex(segment['p_vaddr'], fullhex=True)
                _segment['file_size'] = self._format_hex(segment['p_filesz'], fieldsize=5)
                _segment['memory_size'] = self._format_hex(segment['p_memsz'], fieldsize=5)
                _segment['flags'] = describe_p_flags(segment['p_flags'])
                _segment['align'] = self._format_hex(segment['p_align'], lead0x=False)

            if isinstance(segment, InterpSegment):
                _segment['interpreter'] = segment.get_interp_name()

            self.data['program_headers']['segments'][segment['p_type']].append(_segment)

        # Sections to segments mapping
        if self.elffile.num_sections() == 0:
            self.data['program_headers']['sections'] = None
            # No sections? We're done
            return

        for nseg, segment in enumerate(self.elffile.iter_segments()):
            self.data['program_headers']['sections']['%2.2d' % nseg] = []

            for section in self.elffile.iter_sections():
                if (    not section.is_null() and
                        not ((section['sh_flags'] & SH_FLAGS.SHF_TLS) != 0 and
                             section['sh_type'] == 'SHT_NOBITS' and
                             segment['p_type'] != 'PT_TLS') and
                        segment.section_in_segment(section)):
                    _section = {'section_name' : section.name}
                    self.data['program_headers']['sections']['%2.2d' % nseg].append(_section)
    # endregion

    # region Collect Section Header Data
    def collect_section_header_data(self, show_heading=True):
        """ Display the ELF section headers
        """
        if self.elffile.num_sections() == 0:
            self.data['section_headers'] = None
            return

        # Now the entries
        for nsec, section in enumerate(self.elffile.iter_sections()):
            _section = {'section_name' : section.name}
            _section['type'] = describe_sh_type(section['sh_type'])

            if self.elffile.elfclass == 32:
                _section['sh_addr'] = self._format_hex(section['sh_addr'], fieldsize=8, lead0x=False)
                _section['sh_offset'] = self._format_hex(section['sh_offset'], fieldsize=6, lead0x=False)
                _section['sh_size'] = self._format_hex(section['sh_size'], fieldsize=6, lead0x=False)
                _section['sh_entsize'] = self._format_hex(section['sh_entsize'], fieldsize=2, lead0x=False)
                _section['sh_flags'] = describe_sh_flags(section['sh_flags'])
                _section['sh_link'] = section['sh_link']
                _section['sh_info'] = section['sh_info']
                _section['sh_addralign'] = section['sh_addralign']

            else: # 64
                _section['sh_addr'] = self._format_hex(section['sh_addr'], fullhex=True, lead0x=False)
                _section['sh_offset'] = self._format_hex(section['sh_offset'],
                        fieldsize=16 if section['sh_offset'] > 0xffffffff else 8,
                        lead0x=False)
                _section['sh_size'] = self._format_hex(section['sh_size'], fullhex=True, lead0x=False)
                _section['sh_entsize'] = self._format_hex(section['sh_entsize'], fullhex=True, lead0x=False)
                _section['sh_flags'] = describe_sh_flags(section['sh_flags'])
                _section['sh_link'] = section['sh_link']
                _section['sh_info'] = section['sh_info']
                _section['sh_addralign'] = section['sh_addralign']

            self.data['section_headers'].append(_section)       
    # endregion

    # region Collect Notes
    def collect_notes_data(self):
        """ Display the notes contained in the file
        """
        _notes = []
        for section in self.elffile.iter_sections():
            if isinstance(section, NoteSection):
                for note in section.iter_notes():
                    _note = {}
                    _note['name'] = section.name
                    _note['owner'] = note['n_name']
                    _note['data_size'] = self._format_hex(note['n_descsz'], fieldsize=8)
                    _note['note'] = describe_note(note).replace("\n","")
                    _notes.append(_note)

        if len(_notes) == 0:
            self.data['notes'] = None
        else:
            self.data['notes'] = _notes
    # endregion

    # region Collect Architecture Specific Data
    def collect_arch_specific_data(self):
        """ Display the architecture-specific info contained in the file.
        """
        if self.elffile['e_machine'] == 'EM_ARM':
            attr_sec = self.elffile.get_section_by_name('.ARM.attributes')
            # _arch = []

            try:

                _sub_sections = {}
                if hasattr(attr_sec, "iter_subsections"):
                    for s in attr_sec.iter_subsections():
                        _sub_sections[s.header['vendor_name']] = []

                        for ss in s.iter_subsubsections():
                            _sub_data = {}    

                            h_val = "" if ss.header.extra is None else " ".join("%d" % x for x in ss.header.extra)
                            
                            _sub_data['tag'] = describe_attr_tag_arm(ss.header.tag, h_val, None)
                            _sub_data['attributes'] = []
                            for attr in ss.iter_attributes():
                                _attr = {
                                    "tag" : str(attr.tag),
                                    "value" : str(attr.value),
                                    "extra" : str(attr.extra)
                                    }
                                _sub_data['attributes'].append(_attr)
                            _sub_sections[s.header['vendor_name']].append(_sub_data)
                        # _arch.append(_sub_sections)
                    self.data['arch_specific'] = _sub_sections
            except Exception as e:
                self.data['arch_specific'] = None
                self.logger.error(e)
                # print("Error with arch")
                # print(e)
        else:
            self.data['arch_specific'] = None
    # endregion

    # region Collect Version Information
    def collect_version_info(self):
        """ Display the version info contained in the file
        """
        self._init_versioninfo()

        if not self._versioninfo['type']:
            self.data['version_info'] = None
            return

        
        _version_info = {}
        for section in self.elffile.iter_sections():
            # setting up version info
            if isinstance(section, GNUVerSymSection) or isinstance(section, GNUVerDefSection) or isinstance(section, GNUVerNeedSection):
                name_cleaned = section.name.strip(".").replace(".", "_")
                _version_info[name_cleaned] = {}
                _version_info[name_cleaned]['type'] = None
                _version_info[name_cleaned]['entry_count'] = None
                _version_info[name_cleaned]['entries'] = None
                _version_info[name_cleaned]['addr'] = None
                _version_info[name_cleaned]['offset'] = None
                _version_info[name_cleaned]['link'] = None
                _version_info[name_cleaned]['link_name'] = None
                _version_info[name_cleaned]['symbols'] = None


                if isinstance(section, GNUVerSymSection):

                    # number of entries
                    num_symbols = section.num_symbols()
                    name = section.name
                    
                    _version_info[name_cleaned]['type'] = "GNUVerSymSection"
                    _version_info[name_cleaned]['entry_count'] = num_symbols

                    _version_info[name_cleaned]['addr'] = self._format_hex(
                    section['sh_addr'], fieldsize=16, lead0x=True)

                    _version_info[name_cleaned]['offset'] = self._format_hex(
                    section['sh_offset'], fieldsize=6, lead0x=True)
                    
                    _version_info[name_cleaned]['link'] = str(section['sh_link'])
                    _version_info[name_cleaned]['link_name'] = self.elffile.get_section(section['sh_link']).name
                
                    _version_info[name_cleaned]['symbols'] = []
                    # Symbol version info are printed four by four entries
                    for idx_by_4 in range(0, num_symbols, 4):
                        _symbol = {}

                        _symbol['addr'] = '%03x' % idx_by_4

                        for idx in range(idx_by_4, min(idx_by_4 + 4, num_symbols)):

                            symbol_version = self._symbol_version(idx)
                            symbol_version['index'] = str(symbol_version['index'])
                        
                            if symbol_version['index'] == 'VER_NDX_LOCAL':
                                version_index = 0
                                version_name = '(*local*)'
                            elif symbol_version['index'] == 'VER_NDX_GLOBAL':
                                version_index = 1
                                version_name = '(*global*)'
                            else:
                                version_index = symbol_version['index']
                                version_name = '(%(name)s)' % symbol_version

                            visibility = 'h' if symbol_version['hidden'] else ' '
                        
                            _version_info[name_cleaned]['symbols'].append(symbol_version)

                elif isinstance(section, GNUVerDefSection):

                    offset = 0
                    for verdef, verdaux_iter in section.iter_versions():
                        verdaux = next(verdaux_iter)

                        name = verdaux.name
                        if verdef['vd_flags']:
                            flags = describe_ver_flags(verdef['vd_flags'])
                            # Mimic exactly the readelf output
                            flags += ' '
                        else:
                            flags = 'none'


                        verdaux_offset = (
                                offset + verdef['vd_aux'] + verdaux['vda_next'])
                        for idx, verdaux in enumerate(verdaux_iter, start=1):
                            verdaux_offset += verdaux['vda_next']

                        offset += verdef['vd_next']

                elif isinstance(section, GNUVerNeedSection):
                    name_cleaned = section.name.strip(".").replace(".", "_")

                    _version_info[name_cleaned]['type'] = "GNUVerNeedSection"
                    _version_info[name_cleaned]['entry_count'] = num_symbols
                    _version_info[name_cleaned]['entries'] = []

                    offset = 0
                    for verneed, verneed_iter in section.iter_versions():
                        _symbol = {}
                        _symbol.update(verneed.__dict__)
                        _symbol['entry'] = verneed.entry.__dict__

                        
                        vernaux_offset = offset + verneed['vn_aux']
                        _symbol['vernaux'] = []
                        for idx, vernaux in enumerate(verneed_iter, start=1):
                            _vernaux = {}
                            _vernaux.update(vernaux.__dict__)
                            _vernaux['entry'] = vernaux.entry.__dict__
                            _vernaux['vernaux_offset'] = vernaux_offset
                            if vernaux['vna_flags']:
                                flags = describe_ver_flags(vernaux['vna_flags'])
                                # Mimic exactly the readelf output
                                flags += ' '
                            else:
                                flags = 'none'

                            _symbol['vernaux'].append(_vernaux)
                            vernaux_offset += vernaux['vna_next']

                        offset += verneed['vn_next']
                        _version_info[name_cleaned]['entries'].append(_symbol)
        self.data['version_info'] = _version_info
        

    # endregion

    # region Collect Arm Unwind Information
    def collect_arm_unwind(self):
        
        if not self.elffile.has_ehabi_info():
            self.data['arm_unwind_info'] = None
            return
        for ehabi_info in self.elffile.get_ehabi_infos():
            _key = str(ehabi_info.section_name()).replace('.', '')
            self.data['arm_unwind_info'][_key] = {}
            self.data['arm_unwind_info'][_key]['overview'] = {
                "name" : ehabi_info.section_name(),
                "offset" : ehabi_info.section_offset(),
                "count" : ehabi_info.num_entry()
            }
            
            self.data['arm_unwind_info'][_key]['entries'] = {}

            for i in range(ehabi_info.num_entry()):
                entry = ehabi_info.get_entry(i)
                self.data['arm_unwind_info'][_key]['entries'][i] = ehabi_info.get_entry(i).__dict__

                self.data['arm_unwind_info'][_key]['entries'][i]['personality'] = {}
                self.data['arm_unwind_info'][_key]['entries'][i]['personality']['index'] = entry.personality
                self.data['arm_unwind_info'][_key]['entries'][i]['personality']['values'] = None if isinstance(entry, GenericEHABIEntry) or entry.mnmemonic_array() is None else list(map(str, entry.mnmemonic_array()))

    # endregion

    def display_dynamic_tags(self):
        """ 
        Display the dynamic tags contained in the file
        """
        _all_tags = []
        for section in self.elffile.iter_sections():
            if not isinstance(section, DynamicSection):
                continue
            
            for tag in section.iter_tags():
                _tag = {"tag" : None, "type" : None, "name" : None}

                if tag.entry.d_tag == 'DT_NEEDED':
                    parsed = 'Shared library: [%s]' % tag.needed
                elif tag.entry.d_tag == 'DT_RPATH':
                    parsed = 'Library rpath: [%s]' % tag.rpath
                elif tag.entry.d_tag == 'DT_RUNPATH':
                    parsed = 'Library runpath: [%s]' % tag.runpath
                elif tag.entry.d_tag == 'DT_SONAME':
                    parsed = 'Library soname: [%s]' % tag.soname
                elif tag.entry.d_tag.endswith(('SZ', 'ENT')):
                    parsed = '%i (bytes)' % tag['d_val']
                elif tag.entry.d_tag == 'DT_FLAGS':
                    parsed = describe_dt_flags(tag.entry.d_val)
                elif tag.entry.d_tag == 'DT_FLAGS_1':
                    parsed = 'Flags: %s' % describe_dt_flags_1(tag.entry.d_val)
                elif tag.entry.d_tag.endswith(('NUM', 'COUNT')):
                    parsed = '%i' % tag['d_val']
                elif tag.entry.d_tag == 'DT_PLTREL':
                    s = describe_dyn_tag(tag.entry.d_val)
                    if s.startswith('DT_'):
                        s = s[3:]
                    parsed = '%s' % s
                elif tag.entry.d_tag == 'DT_MIPS_FLAGS':
                    parsed = describe_rh_flags(tag.entry.d_val)
                elif tag.entry.d_tag in ('DT_MIPS_SYMTABNO',
                                        'DT_MIPS_LOCAL_GOTNO'):
                    parsed = str(tag.entry.d_val)
                else:
                    parsed = '%#x' % tag['d_val']
                
                _tag['tag'] = str(self._format_hex(ENUM_D_TAG.get(tag.entry.d_tag, tag.entry.d_tag),
                        fullhex=True, lead0x=True))
                _tag['type'] = str(tag.entry.d_tag[3:])
                _tag['name'] = parsed
                _all_tags.append(_tag)

        self.data['dynamic_tags'] = _all_tags

    def display_relocations(self):
        """ Display the relocations contained in the file
        """
        relocation_data = []
        for section in self.elffile.iter_sections():
            if not isinstance(section, RelocationSection):
                continue

            # The symbol table section pointed to in sh_link
            symtable = self.elffile.get_section(section['sh_link'])

            for rel in section.iter_relocations():

                # also will have x64type1 and x64type2 if the binary is x64
                single_relocation = {"offset" : None, "info" : None, "type" : None, "value" : None, "name" : None}
                
                hexwidth = 8 if self.elffile.elfclass == 32 else 12

                single_relocation['offset'] = self._format_hex(rel['r_offset'],
                        fieldsize=hexwidth, lead0x=False)

                single_relocation['info'] = self._format_hex(rel['r_info'],
                        fieldsize=hexwidth, lead0x=False)

                single_relocation['type'] = describe_reloc_type(
                        rel['r_info_type'], self.elffile)
                

                if rel['r_info_sym'] == 0:
                    if section.is_RELA():
                        fieldsize = 8 if self.elffile.elfclass == 32 else 16
                        addend = self._format_hex(rel['r_addend'], lead0x=False)
                        
                        single_relocation['value'] = str(fieldsize)
                        single_relocation['name'] = str(addend)

                else:
                    symbol = symtable.get_symbol(rel['r_info_sym'])
                    # Some symbols have zero 'st_name', so instead what's used
                    # is the name of the section they point at. Truncate symbol
                    # names (excluding version info) to 22 chars, similarly to
                    # readelf.
                    if symbol['st_name'] == 0:
                        symsecidx = self._get_symbol_shndx(symbol,
                                                           rel['r_info_sym'],
                                                           section['sh_link'])
                        symsec = self.elffile.get_section(symsecidx)
                        symbol_name = symsec.name
                        version = ''
                    else:
                        symbol_name = symbol.name
                        version = self._symbol_version(rel['r_info_sym'])
                        version = (version['name']
                                   if version and version['name'] else '')
                    symbol_name = '%.22s' % symbol_name
                
                    if version:
                        symbol_name += '@' + version
                    
                    single_relocation['value'] = self._format_hex(
                            symbol['st_value'],
                            fullhex=True, lead0x=False)

                    if section.is_RELA():
                        if rel['r_addend'] >= 0:
                            single_relocation['name'] = symbol_name + '+' + str(abs(rel['r_addend']))
                        else:
                            single_relocation['name'] = symbol_name + '-' + str(abs(rel['r_addend']))
                    else:
                        single_relocation['name'] = str(symbol_name)

                # Emit the two additional relocation types for ELF64 MIPS
                # binaries.
                if (self.elffile.elfclass == 64 and
                    self.elffile['e_machine'] == 'EM_MIPS'):
                    for i in (2, 3):
                        rtype = rel['r_info_type%s' % i]
                        single_relocation['x64type1'] = i
                        single_relocation['x64type2'] = describe_reloc_type(rtype, self.elffile)

                relocation_data.append(single_relocation)

        self.data['relocation_data'] = relocation_data

    def display_string_dump(self, section_spec):
        """ Display a strings dump of a section. section_spec is either a
            section number or a name.
        """

        _strings = {}

        section = self._section_from_spec(section_spec)

        data = section.data()
        dataptr = 0

        while dataptr < len(data):
            while ( dataptr < len(data) and
                    not (32 <= byte2int(data[dataptr]) <= 127)):
                dataptr += 1

            if dataptr >= len(data):
                break

            endptr = dataptr
            while endptr < len(data) and byte2int(data[endptr]) != 0:
                endptr += 1

            _strings[str(dataptr)] = str(bytes2str(data[dataptr:endptr]))
            
            dataptr = endptr
        _cleaned_name = str(section_spec).replace('.','',1) if str(section_spec)[0] == '.' else str(section_spec)
        self.data['strings'][_cleaned_name] = _strings
        

    def display_debug_dump(self, dump_what):
        """ Dump a DWARF section
        """
        self._init_dwarfinfo()
        if self._dwarfinfo is None:
            return

        set_global_machine_arch(self.elffile.get_machine_arch())

        if dump_what == 'info':
            self._dump_debug_info()
        elif dump_what == 'decodedline':
            self._dump_debug_line_programs()
        elif dump_what == 'frames':
            self._dump_debug_frames()
        elif dump_what == 'frames-interp':
            self._dump_debug_frames_interp()
        elif dump_what == 'aranges':
            self._dump_debug_aranges()
        elif dump_what in { 'pubtypes', 'pubnames' }:
            self._dump_debug_namelut(dump_what)
        elif dump_what == 'loc':
            self._dump_debug_locations()
        else:
            self._emitline('debug dump not yet supported for "%s"' % dump_what)

    #region Helper Functions
    def _decode_flags(self, flags):
        description = ""
        if self.elffile['e_machine'] == "EM_ARM":
            eabi = flags & E_FLAGS.EF_ARM_EABIMASK
            flags &= ~E_FLAGS.EF_ARM_EABIMASK

            if flags & E_FLAGS.EF_ARM_RELEXEC:
                description += ', relocatable executabl'
                flags &= ~E_FLAGS.EF_ARM_RELEXEC

            if eabi == E_FLAGS.EF_ARM_EABI_VER5:
                EF_ARM_KNOWN_FLAGS = E_FLAGS.EF_ARM_ABI_FLOAT_SOFT|E_FLAGS.EF_ARM_ABI_FLOAT_HARD|E_FLAGS.EF_ARM_LE8|E_FLAGS.EF_ARM_BE8
                description += ', Version5 EABI'
                if flags & E_FLAGS.EF_ARM_ABI_FLOAT_SOFT:
                    description += ", soft-float ABI"
                elif flags & E_FLAGS.EF_ARM_ABI_FLOAT_HARD:
                    description += ", hard-float ABI"

                if flags & E_FLAGS.EF_ARM_BE8:
                    description += ", BE8"
                elif flags & E_FLAGS.EF_ARM_LE8:
                    description += ", LE8"

                if flags & ~EF_ARM_KNOWN_FLAGS:
                    description += ', <unknown>'
            else:
                description += ', <unrecognized EABI>'

        elif self.elffile['e_machine'] == 'EM_PPC64':
            if flags & E_FLAGS.EF_PPC64_ABI_V2:
                description += ', abiv2'

        elif self.elffile['e_machine'] == "EM_MIPS":
            if flags & E_FLAGS.EF_MIPS_NOREORDER:
                description += ", noreorder"
            if flags & E_FLAGS.EF_MIPS_PIC:
                description += ", pic"
            if flags & E_FLAGS.EF_MIPS_CPIC:
                description += ", cpic"
            if (flags & E_FLAGS.EF_MIPS_ABI2):
                description += ", abi2"
            if (flags & E_FLAGS.EF_MIPS_32BITMODE):
                description += ", 32bitmode"
            if (flags & E_FLAGS_MASKS.EFM_MIPS_ABI_O32):
                description += ", o32"
            elif (flags & E_FLAGS_MASKS.EFM_MIPS_ABI_O64):
                description += ", o64"
            elif (flags & E_FLAGS_MASKS.EFM_MIPS_ABI_EABI32):
                description += ", eabi32"
            elif (flags & E_FLAGS_MASKS.EFM_MIPS_ABI_EABI64):
                description += ", eabi64"
            if (flags & E_FLAGS.EF_MIPS_ARCH) == E_FLAGS.EF_MIPS_ARCH_1:
                description += ", mips1"
            if (flags & E_FLAGS.EF_MIPS_ARCH) == E_FLAGS.EF_MIPS_ARCH_2:
                description += ", mips2"
            if (flags & E_FLAGS.EF_MIPS_ARCH) == E_FLAGS.EF_MIPS_ARCH_3:
                description += ", mips3"
            if (flags & E_FLAGS.EF_MIPS_ARCH) == E_FLAGS.EF_MIPS_ARCH_4:
                description += ", mips4"
            if (flags & E_FLAGS.EF_MIPS_ARCH) == E_FLAGS.EF_MIPS_ARCH_5:
                description += ", mips5"
            if (flags & E_FLAGS.EF_MIPS_ARCH) == E_FLAGS.EF_MIPS_ARCH_32R2:
                description += ", mips32r2"
            if (flags & E_FLAGS.EF_MIPS_ARCH) == E_FLAGS.EF_MIPS_ARCH_64R2:
                description += ", mips64r2"
            if (flags & E_FLAGS.EF_MIPS_ARCH) == E_FLAGS.EF_MIPS_ARCH_32:
                description += ", mips32"
            if (flags & E_FLAGS.EF_MIPS_ARCH) == E_FLAGS.EF_MIPS_ARCH_64:
                description += ", mips64"

        return "N/A" if description == "" else description

    def _format_hex(self, addr, fieldsize=None, fullhex=False, lead0x=True,
                    alternate=False):
        """ Format an address into a hexadecimal string.

            fieldsize:
                Size of the hexadecimal field (with leading zeros to fit the
                address into. For example with fieldsize=8, the format will
                be %08x
                If None, the minimal required field size will be used.

            fullhex:
                If True, override fieldsize to set it to the maximal size
                needed for the elfclass

            lead0x:
                If True, leading 0x is added

            alternate:
                If True, override lead0x to emulate the alternate
                hexadecimal form specified in format string with the #
                character: only non-zero values are prefixed with 0x.
                This form is used by readelf.
        """
        if alternate:
            if addr == 0:
                lead0x = False
            else:
                lead0x = True
                fieldsize -= 2

        s = '0x' if lead0x else ''
        if fullhex:
            fieldsize = 8 if self.elffile.elfclass == 32 else 16
        if fieldsize is None:
            field = '%x'
        else:
            field = '%' + '0%sx' % fieldsize
        return s + field % addr

    def _print_version_section_header(self, version_section, name, lead0x=True,
                                      indent=1):
        """ Print a section header of one version related section (versym,
            verneed or verdef) with some options to accomodate readelf
            little differences between each header (e.g. indentation
            and 0x prefixing).
        """
        if hasattr(version_section, 'num_versions'):
            num_entries = version_section.num_versions()
        else:
            num_entries = version_section.num_symbols()

        self._emitline("\n%s section '%s' contains %d %s:" % (
            name, version_section.name, num_entries,
            'entry' if num_entries == 1 else 'entries'))
        self._emitline('%sAddr: %s  Offset: %s  Link: %i (%s)' % (
            ' ' * indent,
            self._format_hex(
                version_section['sh_addr'], fieldsize=16, lead0x=lead0x),
            self._format_hex(
                version_section['sh_offset'], fieldsize=6, lead0x=True),
            version_section['sh_link'],
                self.elffile.get_section(version_section['sh_link']).name
            )
        )

    def _init_versioninfo(self):
        """ Search and initialize informations about version related sections
            and the kind of versioning used (GNU or Solaris).
        """
        if self._versioninfo is not None:
            return

        self._versioninfo = {'versym': None, 'verdef': None,
                             'verneed': None, 'type': None}

        for section in self.elffile.iter_sections():
            if isinstance(section, GNUVerSymSection):
                self._versioninfo['versym'] = section
            elif isinstance(section, GNUVerDefSection):
                self._versioninfo['verdef'] = section
            elif isinstance(section, GNUVerNeedSection):
                self._versioninfo['verneed'] = section
            elif isinstance(section, DynamicSection):
                for tag in section.iter_tags():
                    if tag['d_tag'] == 'DT_VERSYM':
                        self._versioninfo['type'] = 'GNU'
                        break

        if not self._versioninfo['type'] and (
                self._versioninfo['verneed'] or self._versioninfo['verdef']):
            self._versioninfo['type'] = 'Solaris'

    def _symbol_version(self, nsym):
        """ Return a dict containing information on the
                   or None if no version information is available
        """
        self._init_versioninfo()

        symbol_version = dict.fromkeys(('index', 'name', 'filename', 'hidden'))

        if (not self._versioninfo['versym'] or
                nsym >= self._versioninfo['versym'].num_symbols()):
            return None

        symbol = self._versioninfo['versym'].get_symbol(nsym)
        index = symbol.entry['ndx']
        if not index in ('VER_NDX_LOCAL', 'VER_NDX_GLOBAL'):
            index = int(index)

            if self._versioninfo['type'] == 'GNU':
                # In GNU versioning mode, the highest bit is used to
                # store whether the symbol is hidden or not
                if index & 0x8000:
                    index &= ~0x8000
                    symbol_version['hidden'] = True

            if (self._versioninfo['verdef'] and
                    index <= self._versioninfo['verdef'].num_versions()):
                _, verdaux_iter = \
                        self._versioninfo['verdef'].get_version(index)
                symbol_version['name'] = next(verdaux_iter).name
            else:
                verneed, vernaux = \
                        self._versioninfo['verneed'].get_version(index)
                symbol_version['name'] = vernaux.name
                symbol_version['filename'] = verneed.name

        symbol_version['index'] = index
        return symbol_version

    def _section_from_spec(self, spec):
        """ Retrieve a section given a "spec" (either number or name).
            Return None if no such section exists in the file.
        """
        try:
            num = int(spec)
            if num < self.elffile.num_sections():
                return self.elffile.get_section(num)
            else:
                return None
        except ValueError:
            # Not a number. Must be a name then
            return self.elffile.get_section_by_name(spec)

    def _get_symbol_shndx(self, symbol, symbol_index, symtab_index):
        """ Get the index into the section header table for the "symbol"
            at "symbol_index" located in the symbol table with section index
            "symtab_index".
        """
        symbol_shndx = symbol['st_shndx']
        if symbol_shndx != SHN_INDICES.SHN_XINDEX:
            return symbol_shndx

        # Check for or lazily construct index section mapping (symbol table
        # index -> corresponding symbol table index section object)
        if self._shndx_sections is None:
            self._shndx_sections = {sec.symboltable: sec for sec in self.elffile.iter_sections()
                                    if isinstance(sec, SymbolTableIndexSection)}
        return self._shndx_sections[symtab_index].get_section_index(symbol_index)

    def _note_relocs_for_section(self, section):
        """ If there are relocation sections pointing to the givne section,
            emit a note about it.
        """
        for relsec in self.elffile.iter_sections():
            if isinstance(relsec, RelocationSection):
                info_idx = relsec['sh_info']
                if self.elffile.get_section(info_idx) == section:
                    self._emitline('  Note: This section has relocations against it, but these have NOT been applied to this dump.')
                    return

    def _init_dwarfinfo(self):
        """ Initialize the DWARF info contained in the file and assign it to
            self._dwarfinfo.
            Leave self._dwarfinfo at None if no DWARF info was found in the file
        """
        if self._dwarfinfo is not None:
            return

        if self.elffile.has_dwarf_info():
            self._dwarfinfo = self.elffile.get_dwarf_info()
        else:
            self._dwarfinfo = None

    def _dump_debug_info(self):
        """ Dump the debugging info section.
        """
        if not self._dwarfinfo.has_debug_info:
            return
        self._emitline('Contents of the %s section:\n' % self._dwarfinfo.debug_info_sec.name)

        # Offset of the .debug_info section in the stream
        section_offset = self._dwarfinfo.debug_info_sec.global_offset

        for cu in self._dwarfinfo.iter_CUs():
            self._emitline('  Compilation Unit @ offset %s:' %
                self._format_hex(cu.cu_offset))
            self._emitline('   Length:        %s (%s)' % (
                self._format_hex(cu['unit_length']),
                '%s-bit' % cu.dwarf_format()))
            self._emitline('   Version:       %s' % cu['version']),
            self._emitline('   Abbrev Offset: %s' % (
                self._format_hex(cu['debug_abbrev_offset']))),
            self._emitline('   Pointer Size:  %s' % cu['address_size'])

            # The nesting depth of each DIE within the tree of DIEs must be
            # displayed. To implement this, a counter is incremented each time
            # the current DIE has children, and decremented when a null die is
            # encountered. Due to the way the DIE tree is serialized, this will
            # correctly reflect the nesting depth
            #
            die_depth = 0
            current_function = None
            for die in cu.iter_DIEs():
                if die.tag == 'DW_TAG_subprogram':
                    current_function = die
                self._emitline(' <%s><%x>: Abbrev Number: %s%s' % (
                    die_depth,
                    die.offset,
                    die.abbrev_code,
                    (' (%s)' % die.tag) if not die.is_null() else ''))
                if die.is_null():
                    die_depth -= 1
                    continue

                for attr in itervalues(die.attributes):
                    name = attr.name
                    # Unknown attribute values are passed-through as integers
                    if isinstance(name, int):
                        name = 'Unknown AT value: %x' % name

                    attr_desc = describe_attr_value(attr, die, section_offset)

                    if 'DW_OP_fbreg' in attr_desc and current_function and not 'DW_AT_frame_base' in current_function.attributes:
                        postfix = ' [without dw_at_frame_base]'
                    else:
                        postfix = ''

                    self._emitline('    <%x>   %-18s: %s%s' % (
                        attr.offset,
                        name,
                        attr_desc,
                        postfix))

                if die.has_children:
                    die_depth += 1

        self._emitline()

    def _dump_debug_line_programs(self):
        """ Dump the (decoded) line programs from .debug_line
            The programs are dumped in the order of the CUs they belong to.
        """
        if not self._dwarfinfo.has_debug_info:
            return
        self._emitline('Contents of the %s section:' % self._dwarfinfo.debug_line_sec.name)
        self._emitline()

        for cu in self._dwarfinfo.iter_CUs():
            lineprogram = self._dwarfinfo.line_program_for_CU(cu)

            cu_filename = bytes2str(lineprogram['file_entry'][0].name)
            if len(lineprogram['include_directory']) > 0:
                dir_index = lineprogram['file_entry'][0].dir_index
                if dir_index > 0:
                    dir = lineprogram['include_directory'][dir_index - 1]
                else:
                    dir = b'.'
                cu_filename = '%s/%s' % (bytes2str(dir), cu_filename)

            self._emitline('CU: %s:' % cu_filename)
            self._emitline('File name                            Line number    Starting address    Stmt')

            # Print each state's file, line and address information. For some
            # instructions other output is needed to be compatible with
            # readelf.
            for entry in lineprogram.get_entries():
                state = entry.state
                if state is None:
                    # Special handling for commands that don't set a new state
                    if entry.command == DW_LNS_set_file:
                        file_entry = lineprogram['file_entry'][entry.args[0] - 1]
                        if file_entry.dir_index == 0:
                            # current directory
                            self._emitline('\n./%s:[++]' % (
                                bytes2str(file_entry.name)))
                        else:
                            self._emitline('\n%s/%s:' % (
                                bytes2str(lineprogram['include_directory'][file_entry.dir_index - 1]),
                                bytes2str(file_entry.name)))
                    elif entry.command == DW_LNE_define_file:
                        self._emitline('%s:' % (
                            bytes2str(lineprogram['include_directory'][entry.args[0].dir_index])))
                elif lineprogram['version'] < 4 or self.elffile['e_machine'] == 'EM_PPC64':
                    self._emitline('%-35s  %11s  %18s    %s' % (
                        bytes2str(lineprogram['file_entry'][state.file - 1].name),
                        state.line if not state.end_sequence else '-',
                        '0' if state.address == 0 else self._format_hex(state.address),
                        'x' if state.is_stmt and not state.end_sequence else ''))
                else:
                    self._emitline('%-35s  %11d  %18s[%d] %s' % (
                        bytes2str(lineprogram['file_entry'][state.file - 1].name),
                        state.line if not state.end_sequence else '-',
                        '0' if state.address == 0 else self._format_hex(state.address),
                        state.op_index,
                        'x' if state.is_stmt and not state.end_sequence else ''))
                if entry.command == DW_LNS_copy:
                    # Another readelf oddity...
                    self._emitline()

    def _dump_frames_info(self, section, cfi_entries):
        """ Dump the raw call frame info in a section.

        `section` is the Section instance that contains the call frame info
        while `cfi_entries` must be an iterable that yields the sequence of
        CIE or FDE instances.
        """
        self._emitline('Contents of the %s section:' % section.name)

        for entry in cfi_entries:
            if isinstance(entry, CIE):
                self._emitline('\n%08x %s %s CIE' % (
                    entry.offset,
                    self._format_hex(entry['length'], fullhex=True, lead0x=False),
                    self._format_hex(entry['CIE_id'], fieldsize=8, lead0x=False)))
                self._emitline('  Version:               %d' % entry['version'])
                self._emitline('  Augmentation:          "%s"' % bytes2str(entry['augmentation']))
                self._emitline('  Code alignment factor: %u' % entry['code_alignment_factor'])
                self._emitline('  Data alignment factor: %d' % entry['data_alignment_factor'])
                self._emitline('  Return address column: %d' % entry['return_address_register'])
                if entry.augmentation_bytes:
                    self._emitline('  Augmentation data:     {}'.format(' '.join(
                        '{:02x}'.format(ord(b))
                        for b in iterbytes(entry.augmentation_bytes)
                    )))
                self._emitline()

            elif isinstance(entry, FDE):
                self._emitline('\n%08x %s %s FDE cie=%08x pc=%s..%s' % (
                    entry.offset,
                    self._format_hex(entry['length'], fullhex=True, lead0x=False),
                    self._format_hex(entry['CIE_pointer'], fieldsize=8, lead0x=False),
                    entry.cie.offset,
                    self._format_hex(entry['initial_location'], fullhex=True, lead0x=False),
                    self._format_hex(
                        entry['initial_location'] + entry['address_range'],
                        fullhex=True, lead0x=False)))
                if entry.augmentation_bytes:
                    self._emitline('  Augmentation data:     {}'.format(' '.join(
                        '{:02x}'.format(ord(b))
                        for b in iterbytes(entry.augmentation_bytes)
                    )))

            else: # ZERO terminator
                assert isinstance(entry, ZERO)
                self._emitline('\n%08x ZERO terminator' % entry.offset)
                continue

            self._emit(describe_CFI_instructions(entry))
        self._emitline()

    def _dump_debug_frames(self):
        """ Dump the raw frame info from .debug_frame and .eh_frame sections.
        """
        if self._dwarfinfo.has_EH_CFI():
            self._dump_frames_info(
                    self._dwarfinfo.eh_frame_sec,
                    self._dwarfinfo.EH_CFI_entries())
        self._emitline()

        if self._dwarfinfo.has_CFI():
            self._dump_frames_info(
                    self._dwarfinfo.debug_frame_sec,
                    self._dwarfinfo.CFI_entries())

    def _dump_debug_namelut(self, what):
        """
        Dump the debug pubnames section.
        """
        if what == 'pubnames':
            namelut = self._dwarfinfo.get_pubnames()
            section = self._dwarfinfo.debug_pubnames_sec
        else:
            namelut = self._dwarfinfo.get_pubtypes()
            section = self._dwarfinfo.debug_pubtypes_sec

        # readelf prints nothing if the section is not present.
        if namelut is None or len(namelut) == 0:
            return

        self._emitline('Contents of the %s section:' % section.name)
        self._emitline()

        cu_headers = namelut.get_cu_headers()

        # go over CU-by-CU first and item-by-item next.
        for (cu_hdr, (cu_ofs, items)) in izip(cu_headers, itertools.groupby(
            namelut.items(), key = lambda x: x[1].cu_ofs)):

            self._emitline('  Length:                              %d'   % cu_hdr.unit_length)
            self._emitline('  Version:                             %d'   % cu_hdr.version)
            self._emitline('  Offset into .debug_info section:     0x%x' % cu_hdr.debug_info_offset)
            self._emitline('  Size of area in .debug_info section: %d'   % cu_hdr.debug_info_length)
            self._emitline()
            self._emitline('    Offset  Name')
            for item in items:
                self._emitline('    %x          %s' % (item[1].die_ofs - cu_ofs, item[0]))
        self._emitline()

    def _dump_debug_aranges(self):
        """ Dump the aranges table
        """
        aranges_table = self._dwarfinfo.get_aranges()
        if aranges_table == None:
            return
        # seems redundent, but we need to get the unsorted set of entries to match system readelf
        unordered_entries = aranges_table._get_entries()

        if len(unordered_entries) == 0:
            self._emitline()
            self._emitline("Section '.debug_aranges' has no debugging data.")
            return

        self._emitline('Contents of the %s section:' % self._dwarfinfo.debug_aranges_sec.name)
        self._emitline()
        prev_offset = None
        for entry in unordered_entries:
            if prev_offset != entry.info_offset:
                if entry != unordered_entries[0]:
                    self._emitline('    %s %s' % (
                        self._format_hex(0, fullhex=True, lead0x=False),
                        self._format_hex(0, fullhex=True, lead0x=False)))
                self._emitline('  Length:                   %d' % (entry.unit_length))
                self._emitline('  Version:                  %d' % (entry.version))
                self._emitline('  Offset into .debug_info:  0x%x' % (entry.info_offset))
                self._emitline('  Pointer Size:             %d' % (entry.address_size))
                self._emitline('  Segment Size:             %d' % (entry.segment_size))
                self._emitline()
                self._emitline('    Address            Length')
            self._emitline('    %s %s' % (
                self._format_hex(entry.begin_addr, fullhex=True, lead0x=False),
                self._format_hex(entry.length, fullhex=True, lead0x=False)))
            prev_offset = entry.info_offset
        self._emitline('    %s %s' % (
                self._format_hex(0, fullhex=True, lead0x=False),
                self._format_hex(0, fullhex=True, lead0x=False)))

    def _dump_frames_interp_info(self, section, cfi_entries):
        """ Dump interpreted (decoded) frame information in a section.

        `section` is the Section instance that contains the call frame info
        while `cfi_entries` must be an iterable that yields the sequence of
        CIE or FDE instances.
        """
        self._emitline('Contents of the %s section:' % section.name)

        for entry in cfi_entries:
            if isinstance(entry, CIE):
                self._emitline('\n%08x %s %s CIE "%s" cf=%d df=%d ra=%d' % (
                    entry.offset,
                    self._format_hex(entry['length'], fullhex=True, lead0x=False),
                    self._format_hex(entry['CIE_id'], fieldsize=8, lead0x=False),
                    bytes2str(entry['augmentation']),
                    entry['code_alignment_factor'],
                    entry['data_alignment_factor'],
                    entry['return_address_register']))
                ra_regnum = entry['return_address_register']

            elif isinstance(entry, FDE):
                self._emitline('\n%08x %s %s FDE cie=%08x pc=%s..%s' % (
                    entry.offset,
                    self._format_hex(entry['length'], fullhex=True, lead0x=False),
                    self._format_hex(entry['CIE_pointer'], fieldsize=8, lead0x=False),
                    entry.cie.offset,
                    self._format_hex(entry['initial_location'], fullhex=True, lead0x=False),
                    self._format_hex(entry['initial_location'] + entry['address_range'],
                        fullhex=True, lead0x=False)))
                ra_regnum = entry.cie['return_address_register']

                # If the FDE brings adds no unwinding information compared to
                # its CIE, omit its table.
                if (len(entry.get_decoded().table) ==
                        len(entry.cie.get_decoded().table)):
                    continue

            else: # ZERO terminator
                assert isinstance(entry, ZERO)
                self._emitline('\n%08x ZERO terminator' % entry.offset)
                continue

            # Decode the table.
            decoded_table = entry.get_decoded()
            if len(decoded_table.table) == 0:
                continue

            # Print the heading row for the decoded table
            self._emit('   LOC')
            self._emit('  ' if entry.structs.address_size == 4 else '          ')
            self._emit(' CFA      ')

            # Look at the registers the decoded table describes.
            # We build reg_order here to match readelf's order. In particular,
            # registers are sorted by their number, and the register matching
            # ra_regnum is always listed last with a special heading.
            decoded_table = entry.get_decoded()
            reg_order = sorted(ifilter(
                lambda r: r != ra_regnum,
                decoded_table.reg_order))
            if len(decoded_table.reg_order):

                # Headings for the registers
                for regnum in reg_order:
                    self._emit('%-6s' % describe_reg_name(regnum))
                self._emitline('ra      ')

                # Now include ra_regnum in reg_order to print its values
                # similarly to the other registers.
                reg_order.append(ra_regnum)
            else:
                self._emitline()

            for line in decoded_table.table:
                self._emit(self._format_hex(
                    line['pc'], fullhex=True, lead0x=False))

                if line['cfa'] is not None:
                    s = describe_CFI_CFA_rule(line['cfa'])
                else:
                    s = 'u'
                self._emit(' %-9s' % s)

                for regnum in reg_order:
                    if regnum in line:
                        s = describe_CFI_register_rule(line[regnum])
                    else:
                        s = 'u'
                    self._emit('%-6s' % s)
                self._emitline()
        self._emitline()

    def _dump_debug_frames_interp(self):
        """ Dump the interpreted (decoded) frame information from .debug_frame
        and .eh_framae sections.
        """
        if self._dwarfinfo.has_EH_CFI():
            self._dump_frames_interp_info(
                    self._dwarfinfo.eh_frame_sec,
                    self._dwarfinfo.EH_CFI_entries())
        self._emitline()

        if self._dwarfinfo.has_CFI():
            self._dump_frames_interp_info(
                    self._dwarfinfo.debug_frame_sec,
                    self._dwarfinfo.CFI_entries())

    def _dump_debug_locations(self):
        """ Dump the location lists from .debug_location section
        """
        def _get_cu_base(cu):
            top_die = cu.get_top_DIE()
            attr = top_die.attributes
            if 'DW_AT_low_pc' in attr:
                return attr['DW_AT_low_pc'].value
            elif 'DW_AT_entry_pc' in attr:
                return attr['DW_AT_entry_pc'].value
            else:
                raise ValueError("Can't find the base IP (low_pc) for a CU")

        di = self._dwarfinfo
        loc_lists = di.location_lists()
        if not loc_lists: # No locations section - readelf outputs nothing
            return

        loc_lists = list(loc_lists.iter_location_lists())
        if len(loc_lists) == 0:
            # Present but empty locations section - readelf outputs a message
            self._emitline("\nSection '%s' has no debugging data." % di.debug_loc_sec.name)
            return

        # To dump a location list, one needs to know the CU.
        # Scroll through DIEs once, list the known location list offsets
        cu_map = dict() # Loc list offset => CU
        for cu in di.iter_CUs():
            for die in cu.iter_DIEs():
                for key in die.attributes:
                    attr = die.attributes[key]
                    if (LocationParser.attribute_has_location(attr, cu['version']) and
                        not LocationParser._attribute_has_loc_expr(attr, cu['version'])):
                        cu_map[attr.value] = cu

        addr_size = di.config.default_address_size # In bytes, 4 or 8
        addr_width = addr_size * 2 # In hex digits, 8 or 16
        line_template = "    %%08x %%0%dx %%0%dx %%s%%s" % (addr_width, addr_width)

        self._emitline('Contents of the %s section:\n' % di.debug_loc_sec.name)
        self._emitline('    Offset   Begin            End              Expression')
        for loc_list in loc_lists:
            cu = cu_map.get(loc_list[0].entry_offset, False)
            if not cu:
                raise ValueError("Location list can't be tracked to a CU")
            base_ip = _get_cu_base(cu)
            for entry in loc_list:
                # TODO: support BaseAddressEntry lines
                expr = describe_DWARF_expr(entry.loc_expr, cu.structs, cu.cu_offset)
                postfix = ' (start == end)' if entry.begin_offset == entry.end_offset else ''
                self._emitline(line_template % (
                    entry.entry_offset,
                    base_ip + entry.begin_offset,
                    base_ip + entry.end_offset,
                    expr,
                    postfix))
            # Pyelftools doesn't store the terminating entry,
            # but readelf emits its offset, so this should too.
            last = loc_list[-1]
            last_len = 2*addr_size
            if isinstance(last, LocationEntry):
                last_len += 2 + len(last.loc_expr)
            self._emitline("    %08x <End of list>" % (last.entry_offset + last_len))

    def _emit(self, s=''):
        """ Emit an object to output
        """
        print(s, end="")

    def _emitline(self, s=''):
        """ Emit an object to output, followed by a newline
        """
        print(s)
    #endregion