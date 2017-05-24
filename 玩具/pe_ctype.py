# coding:utf-8

from ctypes import *
import time

class IMAGE_DOS_HEADER(LittleEndianStructure):
    _fields_ = [("e_magic", c_ushort),
                ("e_cblp", c_ushort),
                ("e_cp", c_ushort),
                ("e_crlc", c_ushort),
                ("e_cparhdr", c_ushort),
                ("e_minalloc", c_ushort),
                ("e_maxalloc", c_ushort),
                ("e_ss", c_ushort),
                ("e_sp", c_ushort),
                ("e_csum", c_ushort),
                ("e_ip", c_ushort),
                ("e_cs", c_ushort),
                ("e_lfarlc", c_ushort),
                ("e_ovno", c_ushort),
                ("e_res_01", c_ushort),
                ("e_res_02", c_ushort),
                ("e_res_03", c_ushort),
                ("e_res_04", c_ushort),
                ("e_oemid", c_ushort),
                ("e_oeminfo", c_ushort),
                ("e_res2_01", c_ushort),
                ("e_res2_02", c_ushort),
                ("e_res2_03", c_ushort),
                ("e_res2_04", c_ushort),
                ("e_res2_05", c_ushort),
                ("e_res2_06", c_ushort),
                ("e_res2_07", c_ushort),
                ("e_res2_08", c_ushort),
                ("e_res2_09", c_ushort),
                ("e_res2_10", c_ushort),
                ("e_lfanew", c_uint)]

class DataDirectory(LittleEndianStructure):
    _fields_ = [("VirtualAddress", c_uint),
                ("Size", c_uint)
                ]
class IMAGE_FILE_HEADER(LittleEndianStructure):
    _fields_ = [("Machine", c_ushort),
                ("NumberOfSections", c_ushort),
                ("TimeDateStamp", c_uint),
                ("PointerToSymbolTable", c_uint),
                ("NumberOfSymbols",c_uint),
                ("SizeOfOptionalHeader", c_ushort),
                ("Characteristics", c_ushort)
                ]

class IMAGE_OPTIONAL_HEADER(LittleEndianStructure):
    _fields_ = [("Magic", c_ushort),  # 标准头部
                ("MajorLinkerVersion", c_ubyte ),
                ("MinorLinkerVersion", c_ubyte ),
                ("SizeOfCode", c_uint ),
                ("SizeOfInitializedData", c_uint ),
                ("SizeOfUninitializedData", c_uint ),
                ("AddressOfEntryPoint", c_uint ),
                ("BaseOfCode", c_uint ),
                ("BaseOfData", c_uint ),
                # NT 附加头部
                ("ImageBase", c_uint ),
                ("SectionAlignment", c_uint ),
                ("FileAlignment", c_uint ),
                ("MajorOperatingSystemVersion",  c_ushort ),
                ("MinorOperatingSystemVersion", c_ushort ),
                ("MajorImageVersion", c_ushort ),
                ("MinorImageVersion", c_ushort ),
                ("MajorSubsystemVersion", c_ushort ),
                ("MinorSubsystemVersion", c_ushort ),
                ("Win32VersionValue", c_uint ),     # 保留位置，必须为0
                ("SizeOfImage", c_uint ),
                ("SizeOfHeaders", c_uint ),
                ("CheckSum", c_uint ),
                ("Subsystem", c_ushort ),
                ("DllCharacteristics", c_ushort ),
                ("SizeOfStackReserve", c_uint ),
                ("SizeOfStackCommit", c_uint ),
                ("SizeOfHeapReserve", c_uint ),
                ("SizeOfHeapCommit", c_uint ),
                ("LoaderFlags", c_uint ),
                ("NumberOfRvaAndSizes", c_uint ),
                ("dataDir", DataDirectory*16 )
                ]

class IMAGE_NT_HEADERS(LittleEndianStructure):
    _fields_ = [("Signature", c_uint),
                ("FileHeader", IMAGE_FILE_HEADER),
                ("OptionalHeader", IMAGE_OPTIONAL_HEADER)
                ]

class IMAGE_SECTION_HEADER(LittleEndianStructure):
    _fields_ = [("Name", c_char*8),
                ("VirtualSize", c_uint),
                ("VirtualAddress", c_uint),
                ("SizeOfRawData", c_uint),
                ("PointerToRawData", c_uint),
                ("PointerToRelocations", c_uint),
                ("PointerToLinenumbers", c_uint),
                ("NumberOfRelocations", c_ushort),
                ("NumberOfLinenumbers", c_ushort),
                ("Characteristics", c_uint)]


class IAMGE_IMPORT_DESCRIPTOR(LittleEndianStructure):
    _fields_ = [("OriginalFirstThunk", c_uint),
                ("TimeDateStamp", c_uint),
                ("ForwarderChain", c_uint),
                ("Name", c_uint),
                ("FirstThunk", c_uint),
                ]


class IMAGE_THUNK_DATA32(LittleEndianStructure):
    _fields_ = [("AddressOfData", c_uint)]


class IMAGE_IMPORT_BY_NAME(LittleEndianStructure):
    _fields_ = [("Hint", c_ushort),
                ("Name", c_char*20)]


class pe:
    def __init__(self,path):
        with open(path,'rb') as f:
            self.dos_header,pe_sk=self.get_dos_header(f)
            self.pe_header,sec_header_sk = self.get_pe_header(f,pe_sk)
            self.sec_header = self.get_section_header(f,sec_header_sk)
            self.get_import_table(f)

    def get_dos_header(self,file):
        dos_header= dict()
        l=file.read(sizeof(IMAGE_DOS_HEADER))
        s = IMAGE_DOS_HEADER.from_buffer_copy(l)
        print("-------dos头start--------")
        print("DOS头sig：{0}".format(hex(s.e_magic)))
        print("pe头偏移：{0}:{1}".format(hex(s.e_lfanew),s.e_lfanew))
        print("-------dos头end--------")
        print("\n")
        dos_header['e_magic']=s.e_magic
        dos_header['e_cblp']=s.e_cblp
        dos_header['e_cp']=s.e_cp
        dos_header['e_crlc']=s.e_crlc
        dos_header['e_cparhdr']=s.e_cparhdr
        dos_header['e_minalloc']=s.e_minalloc
        dos_header['e_maxalloc']=s.e_maxalloc
        dos_header['e_ss']=s.e_ss
        dos_header['e_sp']=s.e_sp
        dos_header['e_csum']=s.e_csum
        dos_header['e_ip']=s.e_ip
        dos_header['e_cs']=s.e_cs
        dos_header['e_lfarlc']=s.e_lfarlc
        dos_header['e_ovno']=s.e_ovno
        dos_header['e_res_01']=s.e_res_01
        dos_header['e_res_02']=s.e_res_02
        dos_header['e_res_03']=s.e_res_03
        dos_header['e_res_04']=s.e_res_04
        dos_header['e_oemid']=s.e_oemid
        dos_header['e_oeminfo']=s.e_oeminfo
        dos_header['e_res2_01']=s.e_res2_01
        dos_header['e_res2_02']=s.e_res2_02
        dos_header['e_res2_03']=s.e_res2_03
        dos_header['e_res2_04']=s.e_res2_04
        dos_header['e_res2_05']=s.e_res2_05
        dos_header['e_res2_06']=s.e_res2_06
        dos_header['e_res2_07']=s.e_res2_07
        dos_header['e_res2_08']=s.e_res2_08
        dos_header['e_res2_09']=s.e_res2_09
        dos_header['e_res2_10']=s.e_res2_10
        dos_header['e_lfanew']=s.e_lfanew
        return dos_header,s.e_lfanew

    def get_pe_header(self,file,sk):
        file.seek(sk,0)
        l=file.read(sizeof(IMAGE_NT_HEADERS))
        s = IMAGE_NT_HEADERS.from_buffer_copy(l)
        pe_header=dict()
        file_header=dict()
        op_header=dict()
        pe_header["Signature"]=s.Signature
        pe_header['file_header']=file_header
        pe_header['op_header']=op_header
        print("-------PE标准头start--------")
        print("pe头sig：{0}".format(hex(s.Signature)))
        print("Machine：{0}".format(hex(s.FileHeader.Machine)))
        print("节表数目：{0}".format(hex(s.FileHeader.NumberOfSections)))
        print("文件编译时间：{0}：{1}".format(hex(s.FileHeader.TimeDateStamp),
                                      time.strftime('%Y-%m-%d %H-%M-%S',
                                                    time.localtime(s.FileHeader.TimeDateStamp))))
        print("可选头部的大小：{0}：{1}".format(hex(s.FileHeader.SizeOfOptionalHeader),s.FileHeader.SizeOfOptionalHeader))
        print("Characteristics：{0}".format(hex(s.FileHeader.Characteristics)))
        print("-------PE标准头end--------")
        print('')
        print("-------附加头开始--------")
        print("输入表[地址,大小]：[{0}:{1}]".format(hex(s.OptionalHeader.dataDir[1].VirtualAddress),hex(s.OptionalHeader.dataDir[1].Size)))
        file_header['Machine']=s.FileHeader.Machine
        file_header['NumberOfSections']=s.FileHeader.NumberOfSections
        file_header['TimeDateStamp']=s.FileHeader.TimeDateStamp
        file_header['PointerToSymbolTable']=s.FileHeader.PointerToSymbolTable
        file_header['NumberOfSymbols']=s.FileHeader.NumberOfSymbols
        file_header['SizeOfOptionalHeader']=s.FileHeader.SizeOfOptionalHeader
        file_header['Characteristics']=s.FileHeader.Characteristics
        # ----------------------------------------------------------
        op_header['Magic']=s.OptionalHeader.Magic
        op_header['MajorLinkerVersion']=s.OptionalHeader.MajorLinkerVersion
        op_header['MinorLinkerVersion']=s.OptionalHeader.MinorLinkerVersion
        op_header['SizeOfCode']=s.OptionalHeader.SizeOfCode
        op_header['SizeOfInitializedData']=s.OptionalHeader.SizeOfInitializedData
        op_header['SizeOfUninitializedData']=s.OptionalHeader.SizeOfUninitializedData
        op_header['AddressOfEntryPoint']=s.OptionalHeader.AddressOfEntryPoint
        op_header['BaseOfCode']=s.OptionalHeader.BaseOfCode
        op_header['BaseOfData']=s.OptionalHeader.BaseOfData
        op_header['ImageBase']=s.OptionalHeader.ImageBase
        op_header['SectionAlignment']=s.OptionalHeader.SectionAlignment
        op_header['FileAlignment']=s.OptionalHeader.FileAlignment
        op_header['MajorOperatingSystemVersion']=s.OptionalHeader.MajorOperatingSystemVersion
        op_header['MinorOperatingSystemVersion']=s.OptionalHeader.MinorOperatingSystemVersion
        op_header['MajorImageVersion']=s.OptionalHeader.MajorImageVersion
        op_header['MinorImageVersion']=s.OptionalHeader.MinorImageVersion
        op_header['MajorSubsystemVersion']=s.OptionalHeader.MajorSubsystemVersion
        op_header['MinorSubsystemVersion']=s.OptionalHeader.MinorSubsystemVersion
        op_header['Win32VersionValue']=s.OptionalHeader.Win32VersionValue
        op_header['SizeOfImage']=s.OptionalHeader.SizeOfImage
        op_header['SizeOfHeaders']=s.OptionalHeader.SizeOfHeaders
        op_header['CheckSum']=s.OptionalHeader.CheckSum
        op_header['Subsystem']=s.OptionalHeader.Subsystem
        op_header['DllCharacteristics']=s.OptionalHeader.DllCharacteristics
        op_header['SizeOfStackReserve']=s.OptionalHeader.SizeOfStackReserve
        op_header['SizeOfStackCommit']=s.OptionalHeader.SizeOfStackCommit
        op_header['SizeOfHeapReserve']=s.OptionalHeader.SizeOfHeapReserve
        op_header['SizeOfHeapCommit']=s.OptionalHeader.SizeOfHeapCommit
        op_header['LoaderFlags']=s.OptionalHeader.LoaderFlags
        op_header['NumberOfRvaAndSizes']=s.OptionalHeader.NumberOfRvaAndSizes
        op_header['EXPORT_RVA']=s.OptionalHeader.dataDir[0].VirtualAddress
        op_header['EXPORT_SZ']=s.OptionalHeader.dataDir[0].Size
        op_header['IMPORT_RVA']=s.OptionalHeader.dataDir[1].VirtualAddress
        op_header['IMPORT_SZ']=s.OptionalHeader.dataDir[1].Size
        op_header['RESOURCE_RVA']=s.OptionalHeader.dataDir[2].VirtualAddress
        op_header['RESOURCE_SZ']=s.OptionalHeader.dataDir[2].Size
        op_header['EXCEPTION_RVA']=s.OptionalHeader.dataDir[3].VirtualAddress
        op_header['EXCEPTION_SZ']=s.OptionalHeader.dataDir[3].Size
        op_header['SECURITY_RVA']=s.OptionalHeader.dataDir[4].VirtualAddress
        op_header['SECURITY_SZ']=s.OptionalHeader.dataDir[4].Size
        op_header['BASERELOC_RVA']=s.OptionalHeader.dataDir[5].VirtualAddress
        op_header['BASERELOC_SZ']=s.OptionalHeader.dataDir[5].Size
        op_header['DEBUG_RVA']=s.OptionalHeader.dataDir[6].VirtualAddress
        op_header['DEBUG_SZ']=s.OptionalHeader.dataDir[6].Size
        op_header['COPYRIGHT_RVA']=s.OptionalHeader.dataDir[7].VirtualAddress
        op_header['COPYRIGHT_SZ']=s.OptionalHeader.dataDir[7].Size
        op_header['GLOBALPTR_RVA']=s.OptionalHeader.dataDir[8].VirtualAddress
        op_header['GLOBALPTR_SZ']=s.OptionalHeader.dataDir[8].Size
        op_header['TLS_RVA']=s.OptionalHeader.dataDir[9].VirtualAddress
        op_header['TLS_SZ']=s.OptionalHeader.dataDir[9].Size
        op_header['LOAD_CONFIG_RVA']=s.OptionalHeader.dataDir[10].VirtualAddress
        op_header['LOAD_CONFIG_SZ']=s.OptionalHeader.dataDir[10].Size
        op_header['BOUND_IMPORT_RVA']=s.OptionalHeader.dataDir[11].VirtualAddress
        op_header['BOUND_IMPORT_SZ']=s.OptionalHeader.dataDir[11].Size
        op_header['IAT_RVA']=s.OptionalHeader.dataDir[12].VirtualAddress
        op_header['IAT_SZ']=s.OptionalHeader.dataDir[12].Size
        op_header['DELAY_IMPORT_RVA']=s.OptionalHeader.dataDir[13].VirtualAddress
        op_header['DELAY_IMPORT_SZ']=s.OptionalHeader.dataDir[13].Size
        op_header['COM_DESCRIPTOR_RVA']=s.OptionalHeader.dataDir[14].VirtualAddress
        op_header['COM_DESCRIPTOR_SZ']=s.OptionalHeader.dataDir[14].Size
        op_header['END_RVA']=s.OptionalHeader.dataDir[15].VirtualAddress
        op_header['END_SZ']=s.OptionalHeader.dataDir[15].Size
        sec_header_sk =sk+sizeof(IMAGE_NT_HEADERS)
        return pe_header,sec_header_sk

    def get_section_header(self,file,sk,p=1):
        file.seek(sk,0)
        r=list()
        while True:
            l=file.read(sizeof(IMAGE_SECTION_HEADER))
            s = IMAGE_SECTION_HEADER.from_buffer_copy(l)
            d=dict()
            d["Name"]=s.Name
            d["VirtualSize"]=s.VirtualSize
            d["VirtualAddress"]=s.VirtualAddress
            d["SizeOfRawData"]=s.SizeOfRawData
            d["PointerToRawData"]=s.PointerToRawData
            d["PointerToRelocations"]=s.PointerToRelocations
            d["PointerToLinenumbers"]=s.PointerToLinenumbers
            d["NumberOfRelocations"]=s.NumberOfRelocations
            d["NumberOfLinenumbers"]=s.NumberOfLinenumbers
            d["Characteristics"]=s.Characteristics
            if d["SizeOfRawData"]== 0 and d["PointerToRelocations"]==0:break
            r.append(d)
            if p==1:
                for k in d.keys():
                    if k == "Name":
                        print("小节{0}:{1}，属性如下：".format(k,d[k]))
                    else:
                        print("{0}:{1}".format(k,hex(d[k])))

        return r

    def get_import_table(self,file):
        rva = self.pe_header['op_header']['IMPORT_RVA']
        print(hex(rva))
        off = self.rva_to_offset(rva,self.sec_header)
        r = list()
        num = 0
        sz= sizeof(IAMGE_IMPORT_DESCRIPTOR)
        while True:
            file.seek(off+sz*num,0)
            d= dict()
            l = file.read(sizeof(IAMGE_IMPORT_DESCRIPTOR))
            s = IAMGE_IMPORT_DESCRIPTOR.from_buffer_copy(l)
            if s.Name == 0:break
            file.seek(self.rva_to_offset(s.Name,self.sec_header),0)
            print("-"*10+str(string_at(file.read(20)))+"-"*10)
            r.append(d)
            self.get_impor_function_name(file,s.OriginalFirstThunk)
            num+=1
        return r


    def get_impor_function_name(self,file,orign_rva):
        off = self.rva_to_offset(orign_rva,self.sec_header)
        x =0
        while True:
            file.seek(off+x*sizeof(IMAGE_THUNK_DATA32),0)
            INT_x= file.read(sizeof(IMAGE_THUNK_DATA32))
            m= IMAGE_THUNK_DATA32.from_buffer_copy(INT_x)
            if m.AddressOfData == 0:break
            if int(hex(m.AddressOfData)[2:3]) >= 8 :
                print(bin(m.AddressOfData))
                x+=1
                continue
            file.seek(self.rva_to_offset(m.AddressOfData,self.sec_header),0)
            nam=file.read(sizeof(IMAGE_IMPORT_BY_NAME))
            r4= IMAGE_IMPORT_BY_NAME.from_buffer_copy(nam)
            if r4.Name == 0 :
                print(r4.Hint)
            else:
                print(string_at(r4.Name))
            x+=1



    def h_to_i(self,hx):
        return int(hx,16)



    def rva_to_offset(self,rva,secs):
        for i in secs:
            tmp = rva-i['VirtualAddress']
            if i['SizeOfRawData']>tmp>0:
                r = i['PointerToRawData'] + tmp
                return r


    def get_sz(self):
        print("dos头部的大小为：{0}".format(sizeof(IMAGE_DOS_HEADER)))
        print("file头部的大小为：{0}".format(sizeof(IMAGE_FILE_HEADER)))
        print("optioal部的大小为：{0}".format(sizeof(IMAGE_OPTIONAL_HEADER)))
        print("pe部的大小为：{0}".format(sizeof(IMAGE_NT_HEADERS)))

if __name__ == "__main__":
    m = pe("d:\\1.exe")







