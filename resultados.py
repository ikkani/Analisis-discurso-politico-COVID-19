from cargarCorpus import *
from matplotlib.pyplot import *
import math
import numpy as np
import matplotlib.pyplot as plt
import calendar
import joblib
from wordcloud import WordCloud

semanasMeses = ["5 de enero", "12 de enero", "19 de enero", "26 de enero", 
"2 de febrero", "9 de febrero", "16 de febrero", "23 de febrero",
"1 de marzo", "8 de marzo", "15 de marzo", "22 de marzo", "29 de marzo",
"5 de abril", "12 de abril", "19 de abril", "26 de abril",
"3 de mayo", "10 de mayo", "17 de mayo", "24 de mayo", "31 de mayo",
"7 de junio", "14 de junio", "21 de junio"]

meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
"agosto", "septiembre", "octubre", "noviembre", "diciembre"]

c = joblib.load('./corpusPandas.pkl')

def generarWordCloud(corpus, fechaMin = datetime.datetime(2020,1,1), fechaMax = datetime.datetime(2020,5,31), hashtags = []):
	l_string = ''
	diaMin = fechaMin.day
	diaMax = fechaMax.day
		

	if (fechaMin.month == fechaMax.month):
		arrays = [','.join(e) for e in list(corpus[meses[fechaMax.month-1]].query('dia >= @diaMin and dia <= @diaMax').tokens)]
		for array in arrays:
			l_string += array
	else:
		arrays = [','.join(e) for e in list(corpus[meses[fechaMin.month-1]].query('dia >= @diaMin').tokens)]
		for array in arrays:
			l_string += array

		for i in range (fechaMin.month, fechaMax.month-1):
			arrays = [','.join(e) for e in list(corpus[meses[i]].tokens)]
		for array in arrays:
			l_string += array
		arrays = [','.join(e) for e in list(corpus[meses[fechaMax.month-1]].query('dia <= @diaMax').tokens)]


	wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue', width = 1600, height = 800)
	wordcloud.generate(l_string)
	wordcloud.to_image().show()


def graficaHTsemanas(corpus, mes, titulo = ''):

	h = hashtagPorFecha(corpus, fechaMin = datetime.datetime(2020,mes,1), fechaMax = datetime.datetime(2020,mes,calendar.monthrange(2020,mes)[1]))[0:10]
	tags = [e[0] for e in h]
	hV = [[],[],[],[]]
	hV[0] = hashtagPorFecha(corpus, fechaMin = datetime.datetime(2020,mes,1), fechaMax = datetime.datetime(2020,mes,7))
	hV[0] = [e for e in hV[0] if e[0] in tags]
	hV[1] = hashtagPorFecha(corpus, fechaMin = datetime.datetime(2020,mes,8), fechaMax = datetime.datetime(2020,mes,14))
	hV[1] = [e for e in hV[1] if e[0] in tags]
	hV[2] = hashtagPorFecha(corpus, fechaMin = datetime.datetime(2020,mes,15), fechaMax = datetime.datetime(2020,mes,21))
	hV[2] = [e for e in hV[2] if e[0] in tags]
	hV[3] = hashtagPorFecha(corpus, fechaMin = datetime.datetime(2020,mes,22), fechaMax = datetime.datetime(2020,mes,calendar.monthrange(2020,mes)[1]))
	hV[3] = [e for e in hV[3] if e[0] in tags]

	tagsV = [[],[],[],[]]

	tagsV[0] = [e[0] for e in hV[0]]
	tagsV[1] = [e[0] for e in hV[1]]
	tagsV[2] = [e[0] for e in hV[2]]
	tagsV[3] = [e[0] for e in hV[3]]

	hOrdV = [[],[],[],[]]

	for e in h:
	 e = e[0]
	 i = 0
	 for hOrd in hOrdV:
	  if e not in tagsV[i]:
	   hOrd.append((e,0))
	  hOrd += [elem for elem in hV[i] if elem[0] == e]
	  i += 1

	x = np.arange(len(tags))
	width = 0.6
	valores = [e[1] for e in h]
	v1 = [e[1] for e in hOrdV[0]]
	v2 = [e[1] for e in hOrdV[1]]
	v3 = [e[1] for e in hOrdV[2]]
	v4 = [e[1] for e in hOrdV[3]]

	plt.bar(x-width/2, valores, width=width/2, edgecolor = 'black', 
			linewidth = 0.5, color = ['#DF2020' if any(palabra in e.lower() for palabra in ['covid', 'coronavir']) else '#2060DF' for e in tags], align = 'edge')

	plt.bar( (x+width/8) , v1, width = -width/8, edgecolor = 'black', linewidth = 0.5,  align = 'edge', color = 'violet', label='Primera semana')
	plt.bar( (x+width/4) , v2, width = -width/8, edgecolor = 'black', linewidth = 0.5,  align = 'edge', color = 'mediumorchid', label='Segunda semana')
	plt.bar( (x+(3*width/8)) , v3, width = -width/8, edgecolor = 'black', linewidth = 0.5,  align = 'edge', color = 'darkviolet', label='Tercera semana')
	plt.bar( (x+width/2) , v4, width = -width/8, edgecolor = 'black', linewidth = 0.5,  align = 'edge', color = 'indigo', label='Cuarta semana')


	fig = plt.gcf()
	fig.set_size_inches(18.5, 11.5)
	ax = lines[0].axes
	ax.yaxis.label.set_size(20)
	ax.xaxis.label.set_size(20)
	ax.tick_params(axis='x', which='major', labelsize=18)
	ax.tick_params(axis='y', which='major', labelsize=16)


	plt.xticks(np.arange(len(h)), tags, rotation = 45)
	plt.ylabel('Número de usos del hashtag')
	plt.subplots_adjust(left=0.08, bottom=0.18, right=0.92, top=0.97, wspace=0.2, hspace=0.2)
	plt.legend(loc = 'upper right')
	plt.title('Uso de hashtags en ' + meses[mes-1] + titulo, size=20)
	plt.savefig(fname = './Memoria/imagenes/graficas/hashtagsGeneral' + meses[mes-1] + 'DesgloseSemanas.pdf')


def graficaHTfebrero():

	h = hashtagPorFecha(corpus, fechaMin = datetime.datetime(2020,2,1), fechaMax = datetime.datetime(2020,2,28))[0:10]
	tags = [e[0] for e in h]
	hV = [[],[],[],[]]
	hV[0] = hashtagPorFecha(corpus, fechaMin = datetime.datetime(2020,2,1), fechaMax = datetime.datetime(2020,2,7))
	hV[0] = [e for e in hV[0] if e[0] in tags]
	hV[1] = hashtagPorFecha(corpus, fechaMin = datetime.datetime(2020,2,8), fechaMax = datetime.datetime(2020,2,14))
	hV[1] = [e for e in hV[1] if e[0] in tags]
	hV[2] = hashtagPorFecha(corpus, fechaMin = datetime.datetime(2020,2,15), fechaMax = datetime.datetime(2020,2,21))
	hV[2] = [e for e in hV[2] if e[0] in tags]
	hV[3] = hashtagPorFecha(corpus, fechaMin = datetime.datetime(2020,2,22), fechaMax = datetime.datetime(2020,2,28))
	hV[3] = [e for e in hV[3] if e[0] in tags]

	tagsV = [[],[],[],[]]

	tagsV[0] = [e[0] for e in hV[0]]
	tagsV[1] = [e[0] for e in hV[1]]
	tagsV[2] = [e[0] for e in hV[2]]
	tagsV[3] = [e[0] for e in hV[3]]

	hOrdV = [[],[],[],[]]

	for e in h:
	 e = e[0]
	 i = 0
	 for hOrd in hOrdV:
	  if e not in tagsV[i]:
	   hOrd.append((e,0))
	  hOrd += [elem for elem in hV[i] if elem[0] == e]
	  i += 1

	x = np.arange(len(tags))
	width = 0.6
	valores = [e[1] for e in h]
	v1 = [e[1] for e in hOrdV[0]]
	v2 = [e[1] for e in hOrdV[1]]
	v3 = [e[1] for e in hOrdV[2]]
	v4 = [e[1] for e in hOrdV[3]]

	plt.bar(x-width/2, valores, width=width/2, edgecolor = 'black', 
			linewidth = 0.5, color = ['#DF2020' if any(palabra in e.lower() for palabra in ['covid', 'coronavir']) else '#2060DF' for e in tags], align = 'edge')

	plt.bar( (x+width/8) , v1, width = -width/8, edgecolor = 'black', linewidth = 0.5,  align = 'edge', color = 'violet', label='Primera semana')
	plt.bar( (x+width/4) , v2, width = -width/8, edgecolor = 'black', linewidth = 0.5,  align = 'edge', color = 'mediumorchid', label='Segunda semana')
	plt.bar( (x+(3*width/8)) , v3, width = -width/8, edgecolor = 'black', linewidth = 0.5,  align = 'edge', color = 'darkviolet', label='Tercera semana')
	plt.bar( (x+width/2) , v4, width = -width/8, edgecolor = 'black', linewidth = 0.5,  align = 'edge', color = 'indigo', label='Cuarta semana')

	plt.xticks(np.arange(len(h)), tags, rotation = 45)
	plt.ylabel('Número de usos del hashtag')
	plt.subplots_adjust(left=0.08, bottom=0.18, right=0.92, top=0.97, wspace=0.2, hspace=0.2)
	plt.legend(loc = 'upper right')
	plt.title('Uso de hashtags en febrero')
	plt.show()


def printHT(h, n, titulo = ''):
	h = h[0:n]
	tags = [e[0] for e in h]
	valores = [e[1] for e in h]
	plt.bar(np.arange(len(h)), valores, width=0.6, edgecolor = 'black', 
		linewidth = 0.5, color = ['#DF2020' if any(palabra in e.lower() for palabra in ['covid', 'coronavir']) else '#2060DF' for e in tags])
	plt.xticks(np.arange(len(h)), tags, rotation = 45)
	plt.ylabel('Número de usos del hashtag')
	plt.title(titulo)
	plt.subplots_adjust(left=0.08, bottom=0.18, right=0.92, top=0.97, wspace=0.2, hspace=0.2)


def hashtagPorFecha(corpus, fechaMin = datetime.datetime(2020,1,1), fechaMax = datetime.datetime.now()):
	hashtags = {}

	if fechaMax > sorted(list(corpus))[-1]:
		fechaMax = sorted(list(corpus))[-1]

	assert fechaMin <= fechaMax , "La fecha minima es mayor a la maxima" 

	dia = fechaMin

	while dia <= fechaMax:
		tweets = corpus[dia]
		hashtagsDia = [t.hashtags for t in tweets if t.hashtags != []]
		hashtagsDia = [h.lower() for tweet in hashtagsDia for h in tweet]
		for h in hashtagsDia:
			hashtags[h] = hashtags.get(h,0) + 1
		dia += datetime.timedelta(days = 1)

	return sorted(hashtags.items(), key=lambda x: x[1], reverse=True)


def palabrasPorSemanas(corpus, palabras):
	dia = sorted(list(corpus))[0]
	ultimoDia = sorted(list(corpus))[-1]
	apariciones   = [0] * ultimoDia.isocalendar()[1]
	tweetsTotales = [0] * ultimoDia.isocalendar()[1]
	porcentaje    = [0] * ultimoDia.isocalendar()[1]
	while dia <= ultimoDia:
		tweets = corpus[dia]
		cont = 0
		for tweet in tweets:
			aparece = False
			for palabra in palabras:
				aparece = palabra in tweet.txtOriginal.lower()
				if aparece:
					cont = cont + 1
					break
		apariciones[dia.isocalendar()[1]-1] = apariciones[dia.isocalendar()[1]-1] + cont
		tweetsTotales[dia.isocalendar()[1]-1] = tweetsTotales[dia.isocalendar()[1]-1] + len(tweets)
		
		dia = dia + datetime.timedelta(days = 1)

	for i in range(0,len(apariciones)):
		porcentaje[i] = (apariciones[i] / tweetsTotales[i]) * 100

	return porcentaje


def palabrasPorSemanasPartidos(corpus, palabras, partidos):
	dia = sorted(list(corpus))[0]
	ultimoDia = sorted(list(corpus))[-1]
	apariciones   = [0] * ultimoDia.isocalendar()[1]
	tweetsTotales = [0] * ultimoDia.isocalendar()[1]
	porcentaje    = [0] * ultimoDia.isocalendar()[1]
	while dia <= ultimoDia:
		tweets = corpus[dia]
		tweets = [t for t in tweets if t.partido in partidos]
		cont = 0
		for tweet in tweets:
			aparece = False
			for palabra in palabras:
				aparece = palabra in tweet.txtOriginal.lower()
				if aparece:
					cont = cont + 1
					break
		apariciones[dia.isocalendar()[1]-1] = apariciones[dia.isocalendar()[1]-1] + cont
		tweetsTotales[dia.isocalendar()[1]-1] = tweetsTotales[dia.isocalendar()[1]-1] + len(tweets)
		
		dia = dia + datetime.timedelta(days = 1)

	for i in range(0,len(apariciones)):
		porcentaje[i] = (apariciones[i] / tweetsTotales[i]) * 100

	return porcentaje


def grafica(x, y, titulo = '' ):
	plt.title(titulo)
	rangoY = range(math.floor(min(y)) , (math.ceil(max(y))+1))
	plt.xticks(range(math.floor(min(x)) , (math.ceil(max(x))+1) ), semanasMeses[0:len(x)] , rotation=45)
	plt.yticks(rangoY , [str(p)+ ' %' for p in range(math.floor(min(y)),(math.ceil(max(y))+1))] )
	plt.ylabel('Tanto por ciento de tweets que mencionan directamente el tema')
	plt.xlabel('Semana')
	plt.subplots_adjust(left=0.05, bottom=0.13, right=0.95, top=0.95, wspace=0.2, hspace=0.2)
	plt.plot(x, y, 'o-', markersize=4, label='Todos los partidos', color = 'navy')
	plt.legend(loc = 'upper right')
	fig = plt.gcf()
	fig.set_size_inches(18.5, 10.5)
	plt.show()


def grafica2(x, y, estilos, info, titulo = '' ):
	plt.title(titulo)
	rangoY = range(math.floor(np.min(y)) , (math.ceil(np.max(y))+1))
	intervalo = math.ceil(len(rangoY) / 20)
	plt.xticks(range(math.floor(min(x)) , (math.ceil(max(x))+1) ), semanasMeses[0:len(x)] , rotation=45)
	plt.yticks(rangoY , [str(p)+ ' %' if p % intervalo == 0 else '' for p in rangoY] )
	plt.ylabel('Tanto por ciento de tweets que mencionan directamente el tema')
	plt.xlabel('Semana')
	plt.subplots_adjust(left=0.05, bottom=0.13, right=0.95, top=0.95, wspace=0.2, hspace=0.2)
	for i in range(0, len(y)):
		plt.plot(x, y[i], estilos[i], markersize=4, label=info[i][0], color=info[i][1])
	
	legend(loc = 'upper right')
	fig = plt.gcf()
	fig.set_size_inches(18.5, 10.5)
	plt.show()
