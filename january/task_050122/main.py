# Author - Kristiāns Francis Cagulis
# Date - 05.01.2022
# Title - main vs module

from module import consuption
import pandas as pd


def main():
	print(consuption(6.7, 2500))


def try_except():
	try:
		# print(error)  # "Name Error"
		data = pd.read_csv("auto_imports_mainits.csx")  # "Error 2"

	except NameError:
		print("Name Error")

	except Exception as error:
		print(error)

	except:
		print("Error 2")


if __name__ == '__main__':
	# main()
	try_except()
