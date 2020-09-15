import joblib
from descargarTuits import *
from procesarTuits import *
from cargarCorpus import *

descargar()
procesar()
c = cargarPandas()
joblib.dump(c, 'corpusPandas.pkl')