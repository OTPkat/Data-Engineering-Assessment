import csv
from sqlalchemy.ext.asyncio import AsyncSession


class CsvLoader:
    def __init__(self, engine):
        self.engine = engine

    async def load_csv(self, file_path: str, model, schema):
        async with AsyncSession(self.engine) as session:
            async with session.begin():
                with open(file_path) as csv_file:
                    reader = csv.reader(csv_file)
                    headers = next(reader)
                    session.add_all(
                        [
                            model(**schema(**{header: value for (header, value) in zip(headers, row)}).dict())
                            for row in reader
                        ]
                        )

        await session.commit()