import sqlite3
import re

path = 'app/data_sql/'

def SaveFinalSql():
	conn = sqlite3.connect(path +'finalDataBase.sqlite')
	conn1 = sqlite3.connect(path +'fileUploadBase.sqlite')
	conn2 = sqlite3.connect(path +'fileBaseGoogle.sqlite')
	cur = conn.cursor()
	cur1 = conn1.cursor()
	cur2 = conn2.cursor()

	# Do some setup
	#cur.executescript('''
	#DROP TABLE IF EXISTS UrlData;

	#CREATE TABLE UrlData (
		#id     INTEGER NOT NULL PRIMARY KEY UNIQUE,
		#link   TEXT UNIQUE,
		#judul  TEXT,
		#kal	   TEXT,
		#sastra TEXT,
		#nkar   INTEGER,
		#nkata  INTEGER,
		#persen INTEGER
	#)
	#''')
	cnt = 'SELECT id FROM UrlData'
	count = [row for row in cur.execute(cnt)]
	count = len(count)

	filebase = 'SELECT * FROM UrlData'
	for row in cur1.execute(filebase): ## file upload
	    file = row[1]
	    tit = row[2]
	    kal = row[3]
	    output = row[4]
	    n_karakter = row[5]
	    n_Kata = row[6]
	    title = re.sub(r'_',' ',tit)
	    FileTitle = 'SELECT * FROM UrlData WHERE judul LIKE ?'
	    adr = (title, )
	    list_f = cur.execute(FileTitle, adr)
	    bol = False
	    for row in cur.execute(FileTitle, adr):
	    	ttl = row[3]
	    	if kal == ttl :bol= True

	    if bol: continue

	    cur.execute('''INSERT OR IGNORE INTO UrlData (id,link,judul,kal,sastra,nkar,nkata)
			VALUES (?,?,?,?,?,?,?)''', (count+1,file,title,kal, output,n_karakter,n_Kata, ) )

	    count += 1
	    #print(count)

	for row in cur2.execute(filebase): ## file google
	    file = row[1]
	    title = row[2]
	    kal = row[3]
	    output = row[4]
	    n_karakter = row[5]
	    n_Kata = row[6]
	    FileTitle = 'SELECT * FROM UrlData WHERE judul LIKE ?'
	    adr = (title, )
	    list_f = cur.execute(FileTitle, adr)
	    bol = False
	    for row in cur.execute(FileTitle, adr):
	    	ttl = row[3]
	    	if kal == ttl :bol= True

	    if bol: continue
	    cur.execute('''INSERT OR IGNORE INTO UrlData (id,link,judul,kal,sastra,nkar,nkata)
			VALUES (?,?,?,?,?,?,?)''', (count+1,file,title,kal, output,n_karakter,n_Kata, ) )

	    count += 1
	    #print(count)

	conn.commit()

def ReturnListSastra():
	conn = sqlite3.connect(path +'finalDataBase.sqlite')
	cur = conn.cursor()
	File_sastra = 'SELECT sastra FROM UrlData'
	list_sartra = []
	for row in cur.execute(File_sastra):
		row = (str(row)).split("'")
		row = row[1]
		list_sartra.append(row)

	return list_sartra

def SavePersen(list):
	conn = sqlite3.connect(path +'finalDataBase.sqlite')
	cur = conn.cursor()
	for i in range(0,len(list)):
		cur.execute('UPDATE UrlData SET persen =? WHERE id = ?',(list[i],i+1,))
	conn.commit()



def ReturnRank():
	file_Rank = 'SELECT * FROM UrlData ORDER BY persen DESC'
	conn = sqlite3.connect(path +'finalDataBase.sqlite')
	cur = conn.cursor()
	list_rank= []
	for row in cur.execute(file_Rank):
		#row = (str(row)).split("'")
		#row = row[0]
		list_rank.append(row)

	return list_rank

#SaveFinalSql()
#SavePersen([0,1,2,3,5])
#LIST_R = ReturnRank()
#print(LIST_R)