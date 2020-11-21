import csv


class CsvService:
    @staticmethod
    def export_from_db(Model, path: str):
        values = Model.objects.all()
        fieldnames = list(filter(lambda i: i[0] != '_', values[0].__dict__.keys()))

        with open(path, "w", newline='') as csv_file:
            writer = csv.DictWriter(csv_file, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            for line in values:
                result = {}
                for key, value in line.__dict__.items():
                    if key[0] != '_':
                        result[key] = value
                writer.writerow(result)
