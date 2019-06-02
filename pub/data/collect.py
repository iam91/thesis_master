from os import listdir
from os.path import isfile, join

if __name__ == '__main__':

    path = './data/'
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    values = []
    for file in files:
        with open(file, 'r') as f:

            skip = True
            for line in f.readlines():
                if(skip):
                    skip = False
                    continue
                
                val = int(line.split(",")[1])
                if(val > 0):
                    values.append(str(val))
            
            f.close()
    
    print(len(values))

    with open('data.csv', 'w+') as f:
        f.write('\n'.join(values))
        f.close()