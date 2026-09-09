from pathlib import Path


class KMLWriter:

    def __init__(self, project_dir):

        self.project_dir = Path(project_dir)

        self.output_dir = (
            self.project_dir
            / "output"
        )

        self.output_dir.mkdir(
            exist_ok=True
        )

    # ==================================================
    # GitHub Pages ベースURL取得
    # ==================================================

    def get_base_url(
        self,
        photo_list
    ):

        """
        photo_url から

        https://ユーザー名.github.io/PhotoMapCreator

        の部分だけを取り出す
        """

        for photo in photo_list:

            if not photo.photo_url:
                continue

            marker = "/projects/"

            if marker in photo.photo_url:

                return (
                    photo.photo_url
                    .split(
                        marker,
                        1
                    )[0]
                )

        return ""

    # ==================================================
    # 撮影方向を16方位へ変換
    # ==================================================

    def get_direction_name(
        self,
        direction
    ):

        """
        方位角を16方位の日本語表記へ変換する。

        0°   = 北
        90°  = 東
        180° = 南
        270° = 西
        """

        try:
            angle = float(direction) % 360.0
        except (TypeError, ValueError):
            return ""

        directions = [
            "北",
            "北北東",
            "北東",
            "東北東",
            "東",
            "東南東",
            "南東",
            "南南東",
            "南",
            "南南西",
            "南西",
            "西南西",
            "西",
            "西北西",
            "北西",
            "北北西"
        ]

        index = int(
            (angle + 11.25)
            // 22.5
        ) % 16

        return directions[index]

    # ==================================================
    # KML作成
    # ==================================================

    def write(
        self,
        photo_list
    ):

        kml_file = (
            self.output_dir
            / "MyMaps.kml"
        )

        total = len(
            photo_list
        )

        # ----------------------------------------------
        # GitHub Pages URL
        # ----------------------------------------------

        base_url = (
            self.get_base_url(
                photo_list
            )
        )

        with open(
            kml_file,
            "w",
            encoding="utf-8"
        ) as f:

            # ==================================================
            # XMLヘッダー
            # ==================================================

            f.write(
                '<?xml version="1.0" '
                'encoding="UTF-8"?>\n'
            )

            f.write(
                '<kml xmlns='
                '"http://www.opengis.net/kml/2.2">\n'
            )

            f.write(
                "<Document>\n"
            )

            f.write(
                "<name>"
                "PhotoMapCreator"
                "</name>\n"
            )

            # ==================================================
            # START アイコン
            # ==================================================

            f.write(
                '<Style id="startStyle">\n'
            )

            f.write(
                "<IconStyle>\n"
            )

            f.write(
                "<scale>15.0</scale>\n"
            )

            f.write(
                "<Icon>\n"
            )

            if base_url:

                f.write(
                    f"<href>"
                    f"{base_url}/"
                    f"icons/start.png"
                    f"</href>\n"
                )

            f.write(
                "</Icon>\n"
            )

            f.write(
                "</IconStyle>\n"
            )

            f.write(
                "</Style>\n"
            )

            # ==================================================
            # GOAL アイコン
            # ==================================================

            f.write(
                '<Style id="goalStyle">\n'
            )

            f.write(
                "<IconStyle>\n"
            )

            f.write(
                "<scale>15.0</scale>\n"
            )

            f.write(
                "<Icon>\n"
            )

            if base_url:

                f.write(
                    f"<href>"
                    f"{base_url}/"
                    f"icons/goal.png"
                    f"</href>\n"
                )

            f.write(
                "</Icon>\n"
            )

            f.write(
                "</IconStyle>\n"
            )

            f.write(
                "</Style>\n"
            )

            # ==================================================
            # 写真マーカー
            # ==================================================

            for photo in photo_list:

                # GPSなし写真はKMLに入れない
                if (
                    photo.lat is None
                    or photo.lon is None
                ):

                    continue

                f.write(
                    "<Placemark>\n"
                )

                # ----------------------------------------------
                # START
                # ----------------------------------------------

                if photo.order == 1:

                    f.write(
                        "<styleUrl>"
                        "#startStyle"
                        "</styleUrl>\n"
                    )

                # ----------------------------------------------
                # GOAL
                # ----------------------------------------------

                elif photo.order == total:

                    f.write(
                        "<styleUrl>"
                        "#goalStyle"
                        "</styleUrl>\n"
                    )

                # ----------------------------------------------
                # タイトル
                # ----------------------------------------------

                title = (
                    f"No."
                    f"{photo.order:03d}"
                )

                f.write(
                    f"<name>"
                    f"{title}"
                    f"</name>\n"
                )

                # ----------------------------------------------
                # 説明
                # ----------------------------------------------

                f.write(
                    "<description>"
                    "<![CDATA["
                )

                # 写真ファイル名
                f.write(
                    f"<h3>"
                    f"{photo.name}"
                    f"</h3>"
                )

                # ----------------------------------------------
                # 写真
                # ----------------------------------------------

                if photo.photo_url:

                    f.write(
                        f'<img '
                        f'src="{photo.photo_url}" '
                        f'width="350">'
                        f'<br><br>'
                    )

                # ----------------------------------------------
                # 撮影日時
                # ----------------------------------------------

                if photo.datetime:

                    f.write(
                        f"<b>撮影日時</b>"
                        f"<br>"
                        f"{photo.datetime}"
                        f"<br><br>"
                    )

                # ----------------------------------------------
                # 撮影方向
                # ----------------------------------------------

                if photo.direction is not None:

                    try:
                        direction = (
                            float(photo.direction)
                            % 360.0
                        )

                        direction_name = (
                            self.get_direction_name(
                                direction
                            )
                        )

                        f.write(
                            f"<b>撮影方向</b>"
                            f"<br>"
                            f"{direction:.1f}°"
                            f"（{direction_name}）"
                            f"<br><br>"
                        )

                    except (
                        TypeError,
                        ValueError
                    ):
                        pass

                # ----------------------------------------------
                # 撮影順
                # ----------------------------------------------

                f.write(
                    f"<b>撮影順</b>"
                    f"<br>"
                    f"{photo.order}"
                    f" / "
                    f"{total}"
                )

                f.write(
                    "]]>"
                    "</description>\n"
                )

                # ----------------------------------------------
                # 座標
                # ----------------------------------------------

                f.write(
                    "<Point>\n"
                )

                f.write(
                    f"<coordinates>"
                    f"{photo.lon},"
                    f"{photo.lat},"
                    f"0"
                    f"</coordinates>\n"
                )

                f.write(
                    "</Point>\n"
                )

                f.write(
                    "</Placemark>\n"
                )

            # ==================================================
            # 撮影ルート
            # ==================================================

            route = [

                p
                for p in photo_list

                if (
                    p.lat is not None
                    and p.lon is not None
                )
            ]

            if len(route) >= 2:

                f.write(
                    "<Placemark>\n"
                )

                f.write(
                    "<name>"
                    "撮影ルート"
                    "</name>\n"
                )

                f.write(
                    "<Style>\n"
                )

                f.write(
                    "<LineStyle>\n"
                )

                # KMLでは AABBGGRR
                # ff0000ff = 赤
                f.write(
                    "<color>"
                    "ff0000ff"
                    "</color>\n"
                )

                f.write(
                    "<width>"
                    "4"
                    "</width>\n"
                )

                f.write(
                    "</LineStyle>\n"
                )

                f.write(
                    "</Style>\n"
                )

                f.write(
                    "<LineString>\n"
                )

                f.write(
                    "<tessellate>"
                    "1"
                    "</tessellate>\n"
                )

                f.write(
                    "<coordinates>\n"
                )

                for p in route:

                    f.write(
                        f"{p.lon},"
                        f"{p.lat},"
                        f"0\n"
                    )

                f.write(
                    "</coordinates>\n"
                )

                f.write(
                    "</LineString>\n"
                )

                f.write(
                    "</Placemark>\n"
                )

            # ==================================================
            # 終了
            # ==================================================

            f.write(
                "</Document>\n"
            )

            f.write(
                "</kml>\n"
            )

        return kml_file