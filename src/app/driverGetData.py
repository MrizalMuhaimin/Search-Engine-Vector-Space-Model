import getURLfromGoogle
import saveDatatoSql
import readdataUpload

src = str(input())

readdataUpload.readDataUpload()
print("data readdataUpload")

URL_From_Google = getURLfromGoogle.UrlFromGoogle(src)
URL_In_Google = getURLfromGoogle.UrlInGoogle(URL_From_Google)
saveDatatoSql.urltoSQL(URL_In_Google)
print("lihat lah data")