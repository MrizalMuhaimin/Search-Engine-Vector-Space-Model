import requests
import bs4
import sqlite3
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


def urltoSQL(List):
	conn = sqlite3.connect('app/data_sql/fileBaseGoogle.sqlite')
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

	#scaping link dan data mendapatkan artikel
	for url in List:
		#url di sql
		#print ("Alamat:",url)
		ttl = url.split('/')
		for i in range(len(ttl)-1,1,-1):
			if '-' in ttl[i] :
				break
		if '-' in ttl[i]:
			ttl = ttl[i]
		else:continue

		name_file = re.sub(r'[-]','_',ttl)
		ttl = re.sub(r'[-]',' ',ttl)

		ttl = ttl.title() #judul di sql
		#print(ttl) 
		try:
			URLres = requests.get(url)
			URLres.raise_for_status()
			URLsoup = bs4.BeautifulSoup(URLres.text, "html.parser")
			URLText = URLsoup('p')
			URLspan = URLsoup('span')
			URLres.close()
			

			#print(URLText)

			text=[]
			for word in URLText:
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
			n_out = len(output.split(' '))

			################################### Pengulanganketikan <P> tidak bisa dibaca diganri dengan <span>
			if(n_out < 10):
				text=[]
				for word in URLspan:
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




			'''textTosave= output.split(' ')'''


			cur.execute('''INSERT OR IGNORE INTO UrlData (link,judul,kal,sastra,nkar,nkata)
				VALUES (?,?,?,?,?,?)''', (url,ttl,kal, output,n_karakter,n_Kata, ) )
			

		except:
			continue

	conn.commit()


