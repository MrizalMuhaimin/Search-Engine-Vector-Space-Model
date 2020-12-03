import requests
import bs4

def UrlFromGoogle(Input):

	res = requests.get('https://google.com/search?q='+''.join(Input))
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	linkElement = soup('a')
	res.close()
	linkToSrc=[]

	count = 0
	idx = 0
	while count < 4:
		if 'search?q=' in linkElement[idx].get('href'):
			link= 'https://google.com'+ linkElement[idx].get('href',None)
			#print(link)
			linkToSrc.append(link)
			count += 1

		idx +=1

	

	return linkToSrc


def UrlInGoogle(List):
	########## Pembersihan link yang mau di jadikan data ###########
	realURL = [] #alamat web yang siap digunakan

	for i in range(len(List)):
		url = List[i]
		#print ("Alamat:",url)

		URLres = requests.get(url)
		URLres.raise_for_status()
		URLsoup = bs4.BeautifulSoup(URLres.text, "html.parser")
		URLlink = URLsoup('a')
		URLres.close()


		GetURLlilk = []

		for link in URLlink:
			tag = link.get('href',None)
			if 'https' not in tag: continue # menghapus href yang bukan link
			if 'google' in tag: continue #menghapu link gooogle
			if 'youtube' in tag: continue #menghapus link youtube
			GetURLlilk.append(tag)


		for link in (GetURLlilk):
			if(link.startswith('/url?q=')):
				URL = link.split('=')
				URL =URL[1]
				URL = URL.split('&')
				URL = URL[0]
				if URL not in realURL:
					realURL.append(URL)
					#print(URL)



		
		
	return realURL