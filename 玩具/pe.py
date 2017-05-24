# coding:utf-8

import pefile
import struct


def dos_header():
    '''
    （注：最左边是文件头的偏移量。）
        IMAGE_DOS_HEADER STRUCT {
            +0h WORD    e_magic        //   Magic DOS signature MZ(4Dh 5Ah)     DOS可执行文件标记
            +2h     WORD    e_cblp     //   Bytes on last page of file
            +4h WORD    e_cp       //   Pages in file
            +6h WORD    e_crlc     //   Relocations
            +8h WORD    e_cparhdr   //  Size of header in paragraphs
            +0ah    WORD    e_minalloc   // Minimun extra paragraphs needs
            +0ch    WORD    e_maxalloc  //  Maximun extra paragraphs needs
            +0eh    WORD    e_ss            //  intial(relative)SS value        DOS代码的初始化堆栈SS
            +10h    WORD    e_sp        //  intial SP value                       DOS代码的初始化堆栈指针SP
            +12h    WORD    e_csum      //  Checksum
            +14h    WORD    e_ip        // intial IP value                    DOS代码的初始化指令入口[指针IP]
            +16h    WORD    e_cs        //  intial(relative)CS value         DOS代码的初始堆栈入口
            +18h    WORD    e_lfarlc        //  File Address of relocation table
            +1ah    WORD    e_ovno         // Overlay number
            +1ch    WORD    e_res[4]         // Reserved words
            +24h    WORD    e_oemid          // OEM identifier(for e_oeminfo)
            +26h    WORD    e_oeminfo   // OEM information;e_oemid specific
            +29h    WORD    e_res2[10]   // Reserved words
            +3ch    DWORD   e_lfanew     //  Offset to start of PE header      指向PE文件头
        } IMAGE_DOS_HEADER ENDS
    '''


    dos_h =['e_magic',
            'e_cblp','e_cp','e_crlc','e_cparhdr','e_minalloc','e_maxalloc',
            'e_ss','e_sp','e_csum','e_ip','e_cs','e_lfarlc','e_ovno',
            'e_res_01','e_res_02','e_res_03','e_res_04',
            'e_oemid','e_oeminfo',
            'e_res2_01','e_res2_02','e_res2_03','e_res2_04','e_res2_05',
            'e_res2_06','e_res2_07','e_res2_08','e_res2_09','e_res2_10',
            'e_lfanew']
    IMAGE_DOS_HEADER_FMT='<HHHHHHHHHHHHHH4HHH10HL'
    IMAGE_DOS_HEADER_SZ =struct.calcsize(IMAGE_DOS_HEADER_FMT)
    print("文件dos头部分结构，长度为{0}\n".format(IMAGE_DOS_HEADER_SZ))
    with open("d:\\1.exe",'rb') as f:
        buf=f.read(IMAGE_DOS_HEADER_SZ)
    dos_head= [hex(x) for x in struct.unpack(IMAGE_DOS_HEADER_FMT,buf)]
    r = zip(dos_h,dos_head)
    print("-------dos头--------")
    for i in r:
        print(i)

    return dos_head[0],dos_head[-1]

def pe_header():
    '''
    PE文件头是由IMAGE_NT_HEADERS结构定义的：

    IMAGE_NT_HEADERS STRUCT {

        +0h DWORD Signature                    PE文件标识

        +4h   IMAGE_FILE_HEADER  FileHeader

        +18h IMAGE_OPTIONAL_HEADER32 OptionalHeader

    } IMAGE_NT_HEADERS ENDS

    '''

if __name__ == "__main__":
    print(dos_header())




