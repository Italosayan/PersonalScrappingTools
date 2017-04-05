import urllib2
import bs4 #this is beautiful soup
import smtplib #sending email function
from email.mime.text import MIMEText #email module
import sys

#Extracting magic

#BCRP http://stackoverflow.com/questions/13303449/urllib2-httperror-http-error-403-forbidden
site ='http://www.bcrp.gob.pe/transparencia/notas-informativas.html'
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

req = urllib2.Request(site, headers=hdr)

try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

#Extracting magic:Inei
inei = 'https://www.inei.gob.pe/prensa/noticias/'
magia = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
pedido = urllib2.Request(inei, headers=magia)
try:
	pagina = urllib2.urlopen(pedido)
except urllib2.HTTPError, e:
	print e.fp.read()

#get INEI soup
contenido = pagina.read()
sopa = bs4.BeautifulSoup(contenido, "lxml")

#get BCRP soup
content = page.read()
soup = bs4.BeautifulSoup(content ,"lxml")

#inei sacar link y fecha de noticias
ultimanotainei = sopa.find("div", {"class":"cuerponoticias"}).find('b')

link =ultimanotainei.find('a')['href']
fecha =ultimanotainei.find('span').contents[0]

#list of articles of 2017
li2017 = soup.find("div",{"itemprop":"articleBody"}).find('ul').findAll('li')

#Get last article link
day   = str(li2017[0])[5:7]
month = str(li2017[0])[8:10]
date = str(li2017[0])[4:11]
link  = "http://www.bcrp.gob.pe/docs/Transparencia/Notas-Informativas/2017/nota-informativa-2017-{}-{}.pdf".format(month,day)

#Conseguir la cantidad de articulos
datelist = []
for i in range(0,len(li2017)):
	datelist.append(str(li2017[i])[4:11])

#Condition to find if there is more notes
f = open('textfile.txt', 'r')
a = f.readline()
print "reading {}".format(a)
f.close()
print "the list lenght {}".format(len(datelist))

if len(datelist)> int(a) :
	msgs="Nueva nota BCRP"
	f = open('textfile.txt', 'w')
	a=int(a) + 1
	f.write(str(a))
else:
	sys.exit("bye bye")
	msgs="Nada nuevo. La nota de BCRP{}:".format(date)

#send email
#http://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
users =["YOUREMAIL@gmail.com]

print "Sending"
for user in users:
	fromaddr = 'italosayan@gmail.com'
	toaddrs  = user
	msg = "\r\n".join([
		"From: italosayan@gmail.com",
		"To: italosayanus@gmail.com",
		"Subject: Notas informativas Peru",
		"Hola, Si tienen algun cuadro o formato que quieren que les llegue automaticamente mandenme un mail.",
		"Basicamente cualquier cosa que quieran automatizar",
		"{} {}".format(msgs, link),
		"En breves INEI",
		])
	username = 'italosayan@gmail.com'
	password = 'jose4123'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()


