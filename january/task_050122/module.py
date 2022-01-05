def consuption(consuption: float, distance: int, price: float = 1.34):
	result = distance / 100 * consuption * price
	return round(result, 3)


def main():
	print(consuption(7.2, 7200))


if __name__ == '__main__':
	main()