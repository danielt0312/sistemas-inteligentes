from arff_lector import *
from window import *

lector = ArffLector("example.arff")
df = lector.getDataFrame()
print (df.head())
ventana = Window.main()