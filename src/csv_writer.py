from pathlib import Path
import csv


class CSVWriter:

    def __init__(self, project_dir):

        self.project_dir = Path(project_dir)

        self.output_dir = self.project_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

    def write(self, photo_list):

        csv_file = self.output_dir / "MyMaps.csv"

        with open(csv_file,
                  "w",
                  newline="",
                  encoding="utf-8-sig") as f:

            writer = csv.writer(f)

            # Google My Maps 用ヘッダー
            writer.writerow([
                "名前",
                "緯度",
                "経度",
                "説明"
            ])

            for photo in photo_list:

                if photo.lat is None or photo.lon is None:
                    continue

                description = ""

                if photo.datetime:
                    description += f"撮影日時：{photo.datetime}\n"

                description += f"撮影順：{photo.order}"

                writer.writerow([
                    photo.name,
                    photo.lat,
                    photo.lon,
                    description
                ])

        return csv_file