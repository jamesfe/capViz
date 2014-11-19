from os.path import join
from os import listdir
import Image, ImageStat
import capFunc

def main():
	capFunc.repickle('.', 'statsdat.pickle')

if(__name__=="__main__"):
	main()
