import pandas as pd
from pandas import DataFrame
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine
from models import Book, Series, Publisher, Author


def main():
    data: DataFrame = load_file()

    for line in data.values:
        print(line)
        with Session(engine) as session:

            stmt = select(Series).where(Series.name.is_(line[3]))
            series = session.scalars(stmt).one_or_none()

            if not series:
                series = Series(name=line[3] if line[3] != "" else "N/A")
                session.add(series)
                session.commit()

            stmt = select(Publisher).where(Publisher.name == line[5])
            publisher = session.scalars(stmt).one_or_none()
            if not publisher:
                publisher = Publisher(name=line[5] if line[5] != "" else "N/A", color="#32a852")
                session.add(publisher)
                session.commit()

            name = parse_author(line[2])
            stmt = select(Author).where(Author.name == name[0] and Author.surname == name[1])
            author = session.scalars(stmt).one_or_none()
            if not author or (name[0] == "" and name[1] == ""):
                author = Author(name=name[0], surname=name[1])
                session.add(author)
                session.commit()

            book = Book(title=line[1],
                        author_id=author.id ,
                        series_id=series.id ,
                        part=float(-1 if line[4] == "" else line[4]),
                        publisher_id=publisher.id ,
                        pages=int(-1 if line[6] == "" else line[6]),
                        cover=True if line[7].startswith("miękka") else False
                        )

            session.add(book)
            session.commit()


def load_file():
    df = pd.read_csv('data.csv',
                     encoding='utf-8',
                     keep_default_na=False,
                     dtype=str)

    # Remove quotes from book titles
    df['Tytuł'] = df['Tytuł'].str.strip('"')

    # Replace empty strings with 'N/A' in specific columns
    columns_to_check = ['Autor', 'Seria', 'Tom', 'Wydawnictwo']
    for col in columns_to_check:
        df[col] = df[col].replace('', '')

    return df


def parse_author(text: str) -> (str, str):
    if text == "": return "N/A", "N/A"
    split = text.split(" ")
    if len(split) == 2:
        return split[0], split[1]
    else:
        return split[0], " ".join(split[1:])


if __name__ == '__main__':
    main()
