# coding:utf-8
import sys

class inf_10:
	tp={}
	tp["ffd8ffe000104a464946"] = "jpg"     # JPEG [jpg)     
	tp["89504e470d0a1a0a0000"] = "png"     # PNG [png)     
	tp["47494638396126026f01"] = "gif"     # GIF [gif)     
	tp["49492a00227105008037"] = "tif"     # TIFF [tif)     
	tp["424d228c010000000000"] = "bmp"     # 16色位图[bmp)     
	tp["424d8240090000000000"] = "bmp"     # 24位位图[bmp)     
	tp["424d8e1b030000000000"] = "bmp"     # 256色位图[bmp)     
	tp["41433130313500000000"] = "dwg"     # CAD [dwg)     
	tp["3c21444f435459504520"] = "html"     # HTML [html)
	tp["3c21646f637479706520"] = "htm"     # HTM [htm)
	tp["48544d4c207b0d0a0942"] = "css"     # css
	tp["696b2e71623d696b2e71"] = "js"     # js
	tp["7b5c727466315c616e73"] = "rtf"     # Rich Text Format [rtf)     
	tp["38425053000100000000"] = "psd"     # Photoshop [psd)     
	tp["46726f6d3a203d3f6762"] = "eml"     # Email [Outlook Express 6] [eml)       
	tp["d0cf11e0a1b11ae10000"] = "doc"     # MS Excel 注意：word、msi 和 excel的文件头一样     
	tp["d0cf11e0a1b11ae10000"] = "vsd"     # Visio 绘图     
	tp["5374616E64617264204A"] = "mdb"     # MS Access [mdb)      
	tp["252150532D41646F6265"] = "ps"     
	tp["255044462d312e350d0a"] = "pdf"     # Adobe Acrobat [pdf)   
	tp["2e524d46000000120001"] = "rmvb"     # rmvb/rm相同  
	tp["464c5601050000000900"] = "flv"     # flv与f4v相同  
	tp["00000020667479706d70"] = "mp4" 
	tp["49443303000000002176"] = "mp3" 
	tp["000001ba210001000180"] = "mpg"     #      
	tp["3026b2758e66cf11a6d9"] = "wmv"     # wmv与asf相同    
	tp["52494646e27807005741"] = "wav"     # Wave [wav)  
	tp["52494646d07d60074156"] = "avi"  
	tp["4d546864000000060001"] = "mid"     # MIDI [mid)   
	tp["504b0304140000000800"] = "zip"    
	tp["526172211a0700cf9073"] = "rar"   
	tp["235468697320636f6e66"] = "ini"   
	tp["504b03040a0000000000"] = "jar" 
	tp["4d5a9000030000000400"] = "exe"    # 可执行文件
	tp["3c25402070616765206c"] = "jsp"    # jsp文件
	tp["4d616e69666573742d56"] = "mf"    # MF文件
	tp["3c3f786d6c2076657273"] = "xml"    # xml文件
	tp["494e5345525420494e54"] = "sql"    # xml文件
	tp["7061636b616765207765"] = "java"    # java文件
	tp["406563686f206f66660d"] = "bat"    # bat文件
	tp["1f8b0800000000000000"] = "gz"    # gz文件
	tp["6c6f67346a2e726f6f74"] = "properties"    # bat文件
	tp["cafebabe0000002e0041"] = "class"    # bat文件
	tp["49545346030000006000"] = "chm"    # bat文件
	tp["04000000010000001300"] = "mxp"    # bat文件
	tp["504b0304140006000800"] = "docx"    # docx文件
	tp["d0cf11e0a1b11ae10000"] = "wps"    # WPS文字wps、表格et、演示dps都是一样的
	tp["6431303a637265617465"] = "torrent"	


class inf_5:
	tp={}
	tp["6D6F6F76"] = "mov" # Quicktime[mov]
	tp["FF575043"] = "wpd" # WordPerfect[wpd]
	tp["CFAD12FEC5FD746F"] = "dbx" # Outlook Express [dbx]
	tp["2142444E"] = "pst" # Outlook [pst]
	tp["AC9EBD8F"] = "qdf" # Quicken [qdf)
	tp["E3828596"] = "pwl" # Windows Password [pwl]
	tp["2E7261FD"] = "ram" # Real Audio [ram]
	

def handler(fn):
	with open(fn,'rb') as f:
		tm=''
		for i in range(9):
			tm+=str(f.read(1))
		print(tm)
		print(tmp_1)
		'''
		if tmp_1 in inf_10.tp:
			print(inf_10.tp[tmp1])'''
	
def main(argv):
	print(argv)
	handler(argv[1])
	
if __name__ == '__main__':
	main(sys.argv)