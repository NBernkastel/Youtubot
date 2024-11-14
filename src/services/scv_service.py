import csv
import os
import uuid
from typing import List


class CSVService:
    @staticmethod
    async def create_csv_file(data: List):
        filename = str(uuid.uuid4()) + '.csv'
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        return filename

    @staticmethod
    async def delete_csv_file(file_path):
        os.remove(file_path)
