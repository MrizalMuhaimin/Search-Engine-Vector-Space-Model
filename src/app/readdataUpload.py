import os
import bs4
import re
import sqlite3
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def readDataUpload():

	dir_list = os.listdir('app/static/uploads/')
	#print(dir_list)
	conn = sqlite3.connect('app/data_sql/fileUploadBase.sqlite')
	cur = conn.cursor()

	# Do some setup
	cur.executescript('''
	DROP TABLE IF EXISTS UrlData;

	CREATE TABLE UrlData (
		id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		link   TEXT UNIQUE,
		judul  TEXT,
		kal	   TEXT,
		sastra TEXT,
		nkar   INTEGER,
		nkata  INTEGER
	)
	''')

	for file in dir_list:
		if '.py' in file: continue
		if '.sqlite' in file: continue
		title = file;
		title = title.split('.')
		title = title[0]
		open_file = open('app/static/uploads/'+str(file))	
		#print(open_file.readlines())
		if '.html' in file:
			Filesoup = bs4.BeautifulSoup(open_file, "html.parser")
			FileText = Filesoup('p')
			Filespan = Filesoup('span')
			#print(FileText)

			text=[]
			for word in FileText:
				for ctk in word.contents:
					text.append(ctk)

			#pembersihan text dengan  '< .....>''
			text_clean = '' 
			for word in text:
				try:
					dokumen = re.sub(r'^<\S+ \S+>','',word)
					if dokumen == ' ' or dokumen ==' .' : continue
					#print(dokumen) 
					text_clean += dokumen +' '

				except:
					continue

			n_karakter = len(text_clean) # banyakny akerakter di sql
			#if n_karakter == 0: continue #menhapus link yang kaliatny
			n_Kata = len(text_clean.split(' '))
			kal = text_clean


			factory = StemmerFactory()
			stemmer = factory.create_stemmer()
			output   = stemmer.stem(text_clean)
			#print(output)
			n_out = len(output.split(' '))

			################################### Pengulanganketikan <P> tidak bisa dibaca diganri dengan <span>
			if(n_out < 10):
				text=[]
				for word in Filespan:
					for ctk in word.contents:
						text.append(ctk)

				#pembersihan text dengan  '< .....>''
				text_clean = '' 
				for word in text:
					try:
						dokumen = re.sub(r'^<\S+ \S+>','',word)
						if dokumen == ' ' or dokumen ==' .' : continue
						#print(dokumen) 
						text_clean += dokumen +' '

					except:
						continue

				n_karakter = len(text_clean) # banyakny akerakter di sql
				if n_karakter == 0: continue #menhapus link yang kaliatny
				n_Kata = len(text_clean.split(' '))
				kal = text_clean

				factory = StemmerFactory()
				stemmer = factory.create_stemmer()
				output   = stemmer.stem(text_clean)


			#print(output)
			#print(kal)

		elif '.txt' in file:	
			open_file = open('app/static/uploads/'+str(file))
			kal = open_file.read()
			#print(text)
			n_karakter = len(kal)
			n_Kata = len(kal.split(' '))
			factory = StemmerFactory()
			stemmer = factory.create_stemmer()
			output   = stemmer.stem(kal)
			#print(output)

		

		cur.execute('''INSERT OR IGNORE INTO UrlData (link,judul,kal,sastra,nkar,nkata)
			VALUES (?,?,?,?,?,?)''', (file,title,kal, output,n_karakter,n_Kata, ) )

	conn.commit()


