import csv

with open('gtin.csv', 'r') as f:

    reader = csv.reader(f)
    s=0
    for line in reader:

        line=line[0].strip()
        link='https://www.reifen.de/reifen/offroad_suv_4x4/andere?freeTextSearch=true&text={}&sort=popularity'.format(line)

        s=s+1
        s_='No GTIN In Process!'

        print(link)
        print(str(s) + ' ' +s_)
