from WSUserInterface import chooseBin, getEmptyBinLocation

def test_chooseBin():
	assert chooseBin(1) == True
	assert chooseBin(0) == False
	assert chooseBin("Garbage") == False

def test_getEmptyBinLocation():
	assert getEmptyBinLocation( "BLT9N7F99578BAAM", 1222563, 0) == False
	assert getEmptyBinLocation( "BLT9N7F99578BAAM", 1222563, 4) == False
	assert getEmptyBinLocation( "BLT9N7F99578BAAM", 1222563, "Garbage") == False

if __name__ == '__main__':
	test_chooseBin()
	test_getEmptyBinLocation()
	print("Tests were successful")