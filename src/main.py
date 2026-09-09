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
from config import BASE_URL


# ==================================================
# EXIFの値を安全にfloatへ変換
# ==================================================

def exif_to_float(value):
    """
    EXIFの数値をfloatへ変換する。

    PillowのIFDRational
    tuple/list
    int/float
    などに対応。
    """

    if value is None:
        return None

    # ----------------------------------------------
    # そのままfloatへ変換できる場合
    # ----------------------------------------------

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
        ZeroDivisionError
    ):
        pass

    # ----------------------------------------------
    # (分子, 分母) 形式の場合
    # ----------------------------------------------

    try:

        if (
            isinstance(value, (tuple, list))
            and len(value) == 2
        ):

            numerator = float(
                value[0]
            )

            denominator = float(
                value[1]
            )

            if denominator == 0:
                return None

            return (
                numerator
                /
                denominator
            )

    except Exception:
        pass

    # ----------------------------------------------
    # numerator / denominator属性を持つ場合
    # ----------------------------------------------

    try:

        numerator = float(
            value.numerator
        )

        denominator = float(
            value.denominator
        )

        if denominator == 0:
            return None

        return (
            numerator
            /
            denominator
        )

    except Exception:
        pass

    return None


# ==================================================
# 撮影方向取得
# ==================================================

def get_photo_direction(gps_info):
    """
    GPSInfoからGPSImgDirectionを取得。

    戻り値:
        0.0 ～ 359.999...
        取得できない場合は None

    方位:
        0°   = 北
        90°  = 東
        180° = 南
        270° = 西
    """

    if not gps_info:
        return None

    raw_direction = gps_info.get(
        "GPSImgDirection"
    )

    if raw_direction is None:
        return None

    direction = exif_to_float(
        raw_direction
    )

    if direction is None:
        return None

    return (
        direction
        % 360.0
    )


# ==================================================
# 方位角 → 方位名
# ==================================================

def get_direction_name(direction):

    if direction is None:
        return "なし"

    directions = [
        "北",
        "北東",
        "東",
        "南東",
        "南",
        "南西",
        "西",
        "北西"
    ]

    index = int(
        (
            direction
            + 22.5
        )
        // 45
    ) % 8

    return directions[index]


# ==================================================
# 方位角 → 矢印
# ==================================================

def get_direction_arrow(direction):

    if direction is None:
        return ""

    arrows = [
        "↑",
        "↗",
        "→",
        "↘",
        "↓",
        "↙",
        "←",
        "↖"
    ]

    index = int(
        (
            direction
            + 22.5
        )
        // 45
    ) % 8

    return arrows[index]


# ==================================================
# PhotoMapCreator 本体
# ==================================================

def main():

    # ==================================================
    # PhotoMapCreatorルート取得
    # ==================================================

    if getattr(
        sys,
        "frozen",
        False
    ):

        root = (
            Path(
                sys.executable
            )
            .resolve()
            .parent
        )

    else:

        root = (
            Path(
                __file__
            )
            .resolve()
            .parent
            .parent
        )

    # ==================================================
    # 起動画面
    # ==================================================

    print()

    print(
        "======================================"
    )

    print(
        " PhotoMapCreator V8"
    )

    print(
        "======================================"
    )

    print()

    print(
        f"PhotoMapCreator : {root}"
    )

    print(
        f"公開URL        : {BASE_URL}"
    )

    print()

    # ==================================================
    # プロジェクト管理
    # ==================================================

    pm = ProjectManager(
        root
    )

    projects = pm.get_projects()

    print(
        "======================================"
    )

    print(
        " プロジェクト"
    )

    print(
        "======================================"
    )

    print()

    # ==================================================
    # 既存プロジェクト一覧
    # ==================================================

    if len(projects) == 0:

        print(
            "現在プロジェクトはありません。"
        )

    else:

        print(
            "現在のプロジェクト"
        )

        print()

        for i, project_name in enumerate(
            projects,
            start=1
        ):

            print(
                f"{i}. {project_name}"
            )

    print()

    print(
        "既存案件は番号を入力してください。"
    )

    print(
        "新規案件は新しいプロジェクト名を入力してください。"
    )

    print()

    choice = input(
        "番号または新しいプロジェクト名："
    ).strip()

    project = None

    # ==================================================
    # 入力なし
    # ==================================================

    if not choice:

        print()

        print(
            "プロジェクトが選択されませんでした。"
        )

        return

    # ==================================================
    # 既存プロジェクト
    # ==================================================

    if choice.isdigit():

        number = int(
            choice
        )

        if (
            number < 1
            or
            number > len(projects)
        ):

            print()

            print(
                "正しい番号を入力してください。"
            )

            return

        project_name = (
            projects[
                number - 1
            ]
        )

        project = pm.open_project(
            project_name
        )

        print()

        print(
            "既存プロジェクトを開きました。"
        )

        print(
            project
        )

    # ==================================================
    # 新規プロジェクト
    # ==================================================

    else:

        project = pm.create_project(
            choice
        )

        print()

        print(
            "新しいプロジェクトを作成しました。"
        )

        print(
            project
        )

    # ==================================================
    # プロジェクト確認
    # ==================================================

    if project is None:

        print()

        print(
            "プロジェクトを取得できませんでした。"
        )

        return

    project = Path(
        project
    )

    project_name = (
        project.name
    )

    # ==================================================
    # 写真読込
    # ==================================================

    print()

    print(
        "======================================"
    )

    print(
        " 写真読込"
    )

    print(
        "======================================"
    )

    print()

    reader = PhotoReader(
        project
    )

    photos = (
        reader.get_photos()
    )

    print(
        f"写真を {len(photos)} 枚見つけました。"
    )

    # ==================================================
    # 写真がない
    # ==================================================

    if len(photos) == 0:

        print()

        print(
            "photosフォルダに写真がありません。"
        )

        print()

        print(
            "写真を以下のフォルダへ入れてください。"
        )

        print(
            project
            /
            "photos"
        )

        print()

        print(
            "その後、もう一度"
            " python src/main.py"
            " を実行してください。"
        )

        return

    # ==================================================
    # EXIF読込準備
    # ==================================================

    exif = ExifReader()

    photo_list = []

    gps_ok = 0
    gps_ng = 0

    direction_ok = 0
    direction_ng = 0

    gps_ng_list = []
    direction_ng_list = []

    # ==================================================
    # 写真1枚ずつ処理
    # ==================================================

    print()

    print(
        "写真のEXIF情報を読み取っています..."
    )

    print()

    for index, photo in enumerate(
        photos,
        start=1
    ):

        # ==============================================
        # EXIF読込
        # ==============================================

        info = exif.read(
            photo
        )

        # ==============================================
        # 初期値
        # ==============================================

        lat = None
        lon = None
        direction = None

        # ==============================================
        # GPS情報あり
        # ==============================================

        gps_info = info.get(
            "gps"
        )

        if gps_info is not None:

            # ------------------------------------------
            # 緯度・経度
            # ------------------------------------------

            try:

                lat, lon = (
                    GPSUtil.get_lat_lon(
                        gps_info
                    )
                )

            except Exception:

                lat = None
                lon = None

            # ------------------------------------------
            # 撮影方向
            # ------------------------------------------

            direction = (
                get_photo_direction(
                    gps_info
                )
            )

        # ==============================================
        # GPS判定
        # ==============================================

        if (
            lat is not None
            and
            lon is not None
        ):

            gps_ok += 1

        else:

            gps_ng += 1

            gps_ng_list.append(
                photo.name
            )

        # ==============================================
        # 撮影方向判定
        # ==============================================

        if direction is not None:

            direction_ok += 1

        else:

            direction_ng += 1

            direction_ng_list.append(
                photo.name
            )

        # ==============================================
        # GitHub Pages写真URL
        #
        # 例:
        # https://nissuiko0691.github.io/
        # PhotoMapCreator_V8/
        # projects/mabechi/photos/IMG_0001.JPG
        # ==============================================

        photo_url = (
            f"{BASE_URL}/"
            f"projects/"
            f"{project_name}/"
            f"photos/"
            f"{photo.name}"
        )

        # ==============================================
        # PhotoData作成
        # ==============================================

        data = PhotoData(
            name=photo.name,
            path=photo,
            datetime=info.get(
                "datetime"
            ),
            lat=lat,
            lon=lon,
            direction=direction,
            photo_url=photo_url,
            order=index
        )

        photo_list.append(
            data
        )

        # ==============================================
        # 画面表示
        # ==============================================

        if direction is not None:

            arrow = (
                get_direction_arrow(
                    direction
                )
            )

            direction_name = (
                get_direction_name(
                    direction
                )
            )

            direction_text = (
                f"{arrow} "
                f"{direction:.1f}° "
                f"({direction_name})"
            )

        else:

            direction_text = (
                "なし"
            )

        print(
            f"No.{index:03d} "
            f"{photo.name} "
            f"撮影方向={direction_text}"
        )

    # ==================================================
    # 読取結果
    # ==================================================

    print()

    print(
        "======================================"
    )

    print(
        " EXIF読取結果"
    )

    print(
        "======================================"
    )

    print()

    print(
        f"写真総数     : "
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
        f"撮影方向あり : "
        f"{direction_ok}"
    )

    print(
        f"撮影方向なし : "
        f"{direction_ng}"
    )

    # ==================================================
    # GPSなし写真
    # ==================================================

    if gps_ng_list:

        print()

        print(
            "---------- GPSなし写真 ----------"
        )

        for name in gps_ng_list:

            print(
                f"  {name}"
            )

    # ==================================================
    # 撮影方向なし写真
    # ==================================================

    if direction_ng_list:

        print()

        print(
            "---------- 撮影方向なし写真 ----------"
        )

        for name in (
            direction_ng_list
        ):

            print(
                f"  {name}"
            )

    # ==================================================
    # 先頭3枚確認
    # ==================================================

    print()

    print(
        "---------- 写真情報確認 ----------"
    )

    for item in (
        photo_list[:3]
    ):

        print()

        print(
            f"No.{item.order:03d}"
        )

        print(
            f"写真 : {item.name}"
        )

        print(
            f"URL  : {item.photo_url}"
        )

        if item.direction is not None:

            print(
                "方向 : "
                f"{get_direction_arrow(item.direction)} "
                f"{item.direction:.1f}° "
                f"({get_direction_name(item.direction)})"
            )

        else:

            print(
                "方向 : なし"
            )

    print()

    print(
        "------------------------------------"
    )

    # ==================================================
    # KML作成
    # ==================================================

    print()

    print(
        "======================================"
    )

    print(
        " KML作成"
    )

    print(
        "======================================"
    )

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
        "KMLファイルを作成しました。"
    )

    print(
        kml_file
    )

    # ==================================================
    # CSV作成
    # ==================================================

    print()

    print(
        "======================================"
    )

    print(
        " CSV作成"
    )

    print(
        "======================================"
    )

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
        "CSVファイルを作成しました。"
    )

    print(
        csv_file
    )

    # ==================================================
    # HTML写真帳
    # ==================================================

    print()

    print(
        "======================================"
    )

    print(
        " 写真帳作成"
    )

    print(
        "======================================"
    )

    html_writer = HtmlWriter(
        project
    )

    html_writer.write(
        photo_list
    )

    print()

    print(
        "写真帳HTMLを作成しました。"
    )

    # ==================================================
    # Photo Sheet作成
    # ==================================================

    sheet_writer = (
        PhotoSheetWriter(
            project
        )
    )

    sheet_writer.write(
        photo_list
    )

    print(
        "写真シートHTMLを作成しました。"
    )

    # ==================================================
    # 完了
    # ==================================================

    print()

    print(
        "======================================"
    )

    print(
        " PhotoMapCreator 完了"
    )

    print(
        "======================================"
    )

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
        f"撮影方向あり : "
        f"{direction_ok}"
    )

    print(
        f"撮影方向なし : "
        f"{direction_ng}"
    )

    print()

    print(
        "出力ファイル"
    )

    print(
        f"KML : {kml_file}"
    )

    print(
        f"CSV : {csv_file}"
    )

    print()

    print(
        "次の作業"
    )

    print(
        "1. GitHub Desktopを起動"
    )

    print(
        "2. Changesを確認"
    )

    print(
        "3. Commit to main"
    )

    print(
        "4. Push origin"
    )

    print(
        "5. Google My Mapsへ"
        " MyMaps.kml を読み込み"
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

        traceback.print_exc()