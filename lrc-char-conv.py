# -*- coding: utf-8 -*-
import logging
import os
import sys
import locale
import cchardet

def listdir(path, list_name):
	for file in os.listdir(path):
		file_path = os.path.join(path, file)
		if os.path.isdir(file_path):
			listdir(file_path, list_name)
		else:
			list_name.append(file_path)

def convert_to_utf8():
	locale_lang, locale_encoding = locale.getdefaultlocale()
	print('system:', locale_lang, locale_encoding)
	list = []
	listdir(os.path.abspath('.'), list)
	for filename in list:
		if filename.split('.')[-1].lower() == 'lrc':
			with open(filename, 'rb') as f:
				bytedata = f.read()
				
			if len(bytedata) == 0:
				continue
			
			chr_res = cchardet.detect(bytedata)
			src_enc = chr_res['encoding'].lower()
			if src_enc == None:
				continue
			
			if (src_enc == 'utf-8') or (src_enc == 'utf-8-sig') or (src_enc == 'ascii'):
				continue
			
			if (src_enc == locale_encoding) or (src_enc == 'euc-jp'):
				src_enc = 'gb18030'
			
			print(src_enc, filename)
			
			try:
				strdata = bytedata.decode(src_enc)
			except UnicodeDecodeError as e:
				print(e)
				continue
			
			with open(filename, 'w+', encoding='utf-8') as f:
				f.write(strdata)
			

if __name__ == "__main__":
	convert_to_utf8()