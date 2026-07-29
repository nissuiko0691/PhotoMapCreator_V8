from pathlib import Path

from project_manager import ProjectManager
from photo_reader import PhotoReader
from exif_reader import ExifReader
from gps_util import GPSUtil
from kml_writer import KMLWriter
from photo_data import PhotoData
from csv_writer import CSVWriter

def main():

    print("=" * 35)
    print("PhotoMap Creator Ver.7.5")
    print("=" * 35)

    # ---------------------------------
    # プロジェクト管理
    # ---------------------------------

    root = Path(__file__).resolve().parent.parent

    pm = ProjectManager(root)

    projects = pm.get_projects()

    print()

    if len(projects) == 0:
        print("プロジェクトはありません。")
    else:
        print("現在のプロジェクト")

        for i, p in enumerate(projects, start=1):
            print(f"{i}. {p}")

    print()
    print("プロジェクトフォルダ")
    print(root)
    print()

    choice = input("番号または新しいプロジェクト名：").strip()

    project = None

    if choice.isdigit():

        number = int(choice)

        if 1 <= number <= len(projects):

            project = pm.open_project(projects[number - 1])

            print()
            print("既存プロジェクトを開きました。")
            print(project)

    elif choice:

        project = pm.create_project(choice)

        print()
        print("新しいプロジェクトを作成しました。")
        print(project)

    if project is None:
        print("プロジェクトが選択されませんでした。")
        return

    # ---------------------------------
    # 写真読込
    # ---------------------------------

    reader = PhotoReader(project)

    photos = reader.get_photos()

    print()
    print(f"写真を {len(photos)} 枚見つけました。")

    if len(photos) == 0:
        print("photosフォルダに写真がありません。")
        return

    # ---------------------------------
    # PhotoData作成
    # ---------------------------------

    exif = ExifReader()

    photo_list = []

    for index, photo in enumerate(photos, start=1):

        info = exif.read(photo)

        lat = None
        lon = None

        if info["gps"] is not None:
            lat, lon = GPSUtil.get_lat_lon(info["gps"])

        data = PhotoData(
            name=photo.name,
            path=photo,
            datetime=info["datetime"],
            lat=lat,
            lon=lon,
            photo_url="",
            order=index
        )

        data.photo_url = (
            f"https://nissuiko0691.github.io/mabechi/photos/{photo.name}"
        )

        print(data.photo_url)
        photo_list.append(data)

    print()
    print(f"PhotoDataを {len(photo_list)} 件作成しました。")

    print()
    print("---------- PhotoData確認（先頭3件） ----------")

    for item in photo_list[:3]:
        print(item)

    print("---------------------------------------------")

    # ---------------------------------
    # KML作成（現在はテスト版）
    # ---------------------------------

    writer = KMLWriter(project)

    kml = writer.write(photo_list)

    print()
    print("KMLを作成しました。")
    print(kml)

    csv_writer = CSVWriter(project)

    csv_file = csv_writer.write(photo_list)

    print()
    print("CSVを作成しました。")
    print(csv_file)

    print()
    print("Ver.7.5 完了")


if __name__ == "__main__":
    main()