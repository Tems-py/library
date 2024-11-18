import csv

def main():
    with open('data.csv', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='"')
        for row in reader:
            print('  '.join(row))


if __name__ == '__main__':
    main()