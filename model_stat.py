import pandas as pd 


if __name__ == '__main__':

    data = pd.read_csv('data_stat.csv')

    print data.info()
    print data.columns