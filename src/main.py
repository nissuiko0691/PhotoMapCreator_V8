from pathlib import Path
import sys
import traceback

from project_manager import ProjectManager
from photo_reader import PhotoReader
from exif_reader import ExifReader
from gps_util import GPSUtil
from kml_writer import KMLWriter
from photo_data import PhotoData
from csv_writer import CSVWriter
from html_writer import HtmlWriter
from photo_sheet_writer import PhotoSheetWriter

from github_auth import GitHubAuth
from github_repository import GitHubRepository
from github_pages import GitHubPages
from github_uploader import GitHubUploader

from config import get_base_url, REPOSITORY_NAME


# ==================================================
# 終了待ち
# ==================================================

def wait_for_exit():

    print()

    try:
        input("Enterキーを押すと終了します...")
    except Exception:
        pass


# ==================================================
# PhotoMapCreator 本体
# ==================================================

def main():

    # ==================================================
    # PhotoMapCreator ルート取得
    # ==================================================

    if getattr(sys, "frozen", False):

        root = (
            Path(sys.executable)
            .resolve()
            .parent
        )

    else:

        root = (
            Path(__file__)
            .resolve()
            .parent
            .parent
        )

    print()
    print("======================================")
    print(" PhotoMapCreator")
    print("======================================")
    print()

    # ==================================================
    # GitHub認証
    # ==================================================

    auth = GitHubAuth()

    token = auth.get_access_token()

    if token is None:

        print()
        print("GitHub認証に失敗しました。")
        return

    user = auth.get_user(token)

    if user is None:

        print()
        print(
            "GitHubユーザー情報を"
            "取得できませんでした。"
        )
        return

    github_username = user.get("login")

    if not github_username:

        print()
        print(
            "GitHubユーザー名を"
            "取得できませんでした。"
        )
        return

    # ==================================================
    # GitHub Pages URL
    # ==================================================

    base_url = get_base_url(
        github_username
    )

    print()
    print("======================================")
    print(" GitHub 接続")
    print("======================================")
    print()

    print(
        f"GitHubユーザー : "
        f"{github_username}"
    )

    print(
        f"公開URL        : "
        f"{base_url}"
    )

    # ==================================================
    # GitHub Repository準備
    # ==================================================

    repo_manager = GitHubRepository(
        token
    )

    repo_result = (
        repo_manager.prepare_repository()
    )

    if repo_result is None:

        print()
        print(
            "GitHub Repositoryの"
            "準備に失敗しました。"
        )
        return

    # ==================================================
    # GitHub Pages準備
    # ==================================================

    pages_manager = GitHubPages(
        token
    )

    pages = (
        pages_manager.prepare_pages(
            github_username,
            REPOSITORY_NAME
        )
    )

    if pages is None:

        print()
        print(
            "GitHub Pagesの"
            "準備に失敗しました。"
        )
        return

    # ==================================================
    # Uploader準備
    # ==================================================

    uploader = GitHubUploader(
        token,
        root
    )

    # ==================================================
    # START / GOAL アイコン確認
    # ==================================================

    icon_ok = (
        uploader.upload_icons(
            github_username,
            REPOSITORY_NAME
        )
    )

    if not icon_ok:

        print()
        print(
            "START / GOALアイコンの"
            "準備に失敗しました。"
        )
        return

    # ==================================================
    # プロジェクト管理
    # ==================================================

    pm = ProjectManager(root)

    projects = pm.get_projects()

    print()
    print("======================================")
    print(" プロジェクト")
    print("======================================")
    print()

    if len(projects) == 0:

        print(
            "プロジェクトはありません。"
        )

    else:

        print(
            "現在のプロジェクト"
        )
        print()

        for i, p in enumerate(
            projects,
            start=1
        ):

            print(
                f"{i}. {p}"
            )

    print()
    print(
        "プロジェクトフォルダ"
    )
    print(root)
    print()

    choice = input(
        "番号または新しい"
        "プロジェクト名："
    ).strip()

    project = None

    # ==================================================
    # 既存プロジェクトを開く
    # ==================================================

    if choice.isdigit():

        number = int(choice)

        if (
            1
            <= number
            <= len(projects)
        ):

            project = pm.open_project(
                projects[
                    number - 1
                ]
            )

            print()
            print(
                "既存プロジェクトを"
                "開きました。"
            )

            print(project)

        else:

            print()
            print(
                "正しい番号を"
                "入力してください。"
            )

            return

    # ==================================================
    # 新規プロジェクト作成
    # ==================================================

    elif choice:

        project = pm.create_project(
            choice
        )

        print()
        print(
            "新しいプロジェクトを"
            "作成しました。"
        )

        print(project)

    # ==================================================
    # プロジェクト未選択
    # ==================================================

    if project is None:

        print()
        print(
            "プロジェクトが"
            "選択されませんでした。"
        )

        return

    # ==================================================
    # 写真読込
    # ==================================================

    reader = PhotoReader(
        project
    )

    photos = (
        reader.get_photos()
    )

    print()
    print(
        f"写真を "
        f"{len(photos)} 枚"
        f"見つけました。"
    )

    # ==================================================
    # 写真がない場合
    # ==================================================

    if len(photos) == 0:

        print()
        print(
            "photosフォルダに"
            "写真がありません。"
        )

        print()
        print(
            "写真をphotosフォルダに入れて、"
            "もう一度PhotoMapCreatorを"
            "実行してください。"
        )

        print()
        print(
            f"写真保存先 : "
            f"{project / 'photos'}"
        )

        return

    # ==================================================
    # PhotoData作成
    # ==================================================

    exif = ExifReader()

    photo_list = []

    project_name = (
        project.name
    )

    gps_ok = 0
    gps_ng = 0

    gps_ng_list = []

    for index, photo in enumerate(
        photos,
        start=1
    ):

        info = exif.read(
            photo
        )

        lat = None
        lon = None
        direction = None

        if info["gps"] is not None:

            lat, lon = (
                GPSUtil.get_lat_lon(
                    info["gps"]
                )
            )

            # ----------------------------------------------
            # 撮影方向取得
            # GPSImgDirection: 0°=北、90°=東、180°=南、270°=西
            # ----------------------------------------------

            raw_direction = info["gps"].get(
                "GPSImgDirection"
            )

            if raw_direction is not None:

                try:
                    direction = float(
                        raw_direction
                    ) % 360.0

                except (
                    TypeError,
                    ValueError,
                    ZeroDivisionError
                ):

                    # Pillow / EXIF の有理数形式にも対応
                    try:
                        if (
                            isinstance(
                                raw_direction,
                                (tuple, list)
                            )
                            and len(raw_direction) == 2
                        ):

                            numerator = float(
                                raw_direction[0]
                            )
                            denominator = float(
                                raw_direction[1]
                            )

                            if denominator != 0:
                                direction = (
                                    numerator
                                    / denominator
                                ) % 360.0

                    except Exception:
                        direction = None

        if (
            lat is not None
            and lon is not None
        ):

            gps_ok += 1

        else:

            gps_ng += 1

            gps_ng_list.append(
                photo.name
            )

        photo_url = (
            f"{base_url}/"
            f"projects/"
            f"{project_name}/"
            f"photos/"
            f"{photo.name}"
        )

        data = PhotoData(
            name=photo.name,
            path=photo,
            datetime=info[
                "datetime"
            ],
            lat=lat,
            lon=lon,
            direction=direction,
            photo_url=photo_url,
            order=index
        )

        photo_list.append(
            data
        )

    print()
    print(
        f"PhotoDataを "
        f"{len(photo_list)} 件"
        f"作成しました。"
    )

    print()
    print(
        f"GPSあり : "
        f"{gps_ok}"
    )

    print(
        f"GPSなし : "
        f"{gps_ng}"
    )

    # ==================================================
    # GPSなし写真表示
    # ==================================================

    if gps_ng_list:

        print()
        print(
            "GPSなし写真"
        )

        for name in gps_ng_list:

            print(
                f"  {name}"
            )

    # ==================================================
    # 写真URL確認
    # ==================================================

    print()
    print(
        "---------- "
        "写真URL確認 "
        "----------"
    )

    for item in (
        photo_list[:3]
    ):

        print(
            f"No."
            f"{item.order:03d}"
        )

        print(
            item.photo_url
        )

    print(
        "----------------"
        "----------------"
    )

    # ==================================================
    # KML作成
    # ==================================================

    kml_writer = KMLWriter(
        project
    )

    kml_file = (
        kml_writer.write(
            photo_list
        )
    )

    print()
    print(
        "KMLを作成しました。"
    )

    print(
        kml_file
    )

    # ==================================================
    # CSV作成
    # ==================================================

    csv_writer = CSVWriter(
        project
    )

    csv_file = (
        csv_writer.write(
            photo_list
        )
    )

    print()
    print(
        "CSVを作成しました。"
    )

    print(
        csv_file
    )

    # ==================================================
    # HTML写真帳
    # ==================================================

    html_writer = HtmlWriter(
        project
    )

    html_writer.write(
        photo_list
    )

    print()
    print(
        "写真帳HTMLを"
        "作成しました。"
    )

    # ==================================================
    # 写真一覧HTML
    # ==================================================

    sheet_writer = (
        PhotoSheetWriter(
            project
        )
    )

    sheet_writer.write(
        photo_list
    )

    print()
    print(
        "写真シートHTMLを"
        "作成しました。"
    )

    # ==================================================
    # GitHubへ写真アップロード
    # ==================================================

    print()
    print(
        "GitHubへ写真を"
        "アップロードします。"
    )

    upload_ok = (
        uploader.upload_project_photos(
            github_username,
            project,
            REPOSITORY_NAME
        )
    )

    if not upload_ok:

        print()
        print(
            "写真のアップロードに"
            "失敗しました。"
        )

        print()
        print(
            "CSV / KML / HTMLは"
            "作成されています。"
        )

        return

    # ==================================================
    # 公開URL確認
    # ==================================================

    uploader.show_photo_url(
        github_username,
        project
    )

    # ==================================================
    # 完了
    # ==================================================

    print()
    print("======================================")
    print(" PhotoMapCreator 完了")
    print("======================================")
    print()

    print(
        f"プロジェクト : "
        f"{project_name}"
    )

    print(
        f"写真枚数     : "
        f"{len(photo_list)}"
    )

    print(
        f"GPSあり      : "
        f"{gps_ok}"
    )

    print(
        f"GPSなし      : "
        f"{gps_ng}"
    )

    print(
        f"GitHub       : "
        f"{github_username}"
    )

    print(
        f"Repository   : "
        f"{REPOSITORY_NAME}"
    )

    print(
        f"公開URL      : "
        f"{base_url}"
    )

    print()
    print(
        "My Maps用ファイル"
    )

    print(
        f"KML : "
        f"{kml_file}"
    )

    print(
        f"CSV : "
        f"{csv_file}"
    )

    print()
    print(
        "Google My Mapsへ"
        "MyMaps.kml または "
        "MyMaps.csv を読み込んでください。"
    )

    print()


# ==================================================
# 起動
# ==================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print()
        print(
            "処理を中止しました。"
        )

    except Exception:

        print()
        print(
            "======================================"
        )

        print(
            " PhotoMapCreator エラー"
        )

        print(
            "======================================"
        )

        print()
        print(
            "予期しないエラーが"
            "発生しました。"
        )

        print()
        print(
            "以下の内容を確認してください。"
        )

        print()

        traceback.print_exc()

    finally:

        wait_for_exit()