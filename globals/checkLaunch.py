from globals import sqlConfig

def wasLaunched(n):
    global _l
    _l = n

def writeLaunched():
    with open("launched", "w") as outfile:
        outfile.write("%d" % _l)

def createDBase():
    try:
        with open("launched") as infile:
            _l = int(infile.read())
            if _l == 0:
                sqlConfig.runOnFirstStart()
    except FileNotFoundError:
        _l = '0'

def popDBase():
    try:
        with open("launched") as infile:
            _l = int(infile.read())
            if _l == 0:
                return True
            else:
                return False
    except FileNotFoundError:
        _l = '0'
