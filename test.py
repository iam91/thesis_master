val = -1

def fun():
    global val
    print val
    val = 1

if __name__ == '__main__':
    print val
    val = 0
    fun()
    print val