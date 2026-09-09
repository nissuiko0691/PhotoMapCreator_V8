from pathlib import Path


class KMLWriter:

    def __init__(self, project_dir):

        self.project_dir = Path(
            project_dir
        )

        self.output_dir = (
            self.project_dir
            / "output"
        )

        self.output_dir.mkdir(
            exist_ok=True
        )

    # ==================================================
    # 方位角 → 方位名
    # ==================================================

    def get_direction_name(
        self,
        direction
    ):

        if direction is None:
            return None

        direction = (
            float(direction)
            % 360.0
        )

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
            (direction + 22.5)
            / 45
        ) % 8

        return directions[index]

    # ==================================================
    # 方位角 → 矢印
    # ==================================================

    def get_direction_arrow(
        self,
        direction
    ):

        if direction is None:
            return None

        direction = (
            float(direction)
            % 360.0
        )

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
            (direction + 22.5)
            / 45
        ) % 8

        return arrows[index]

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

        # ==============================================
        # GPS付き写真のみ
        # ==============================================

        route = [
            p
            for p in photo_list
            if (
                p.lat is not None
                and
                p.lon is not None
            )
        ]

        total = len(route)

        with open(
            kml_file,
            "w",
            encoding="utf-8"
        ) as f:

            # ==========================================
            # KMLヘッダー
            # ==========================================

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
                "PhotoMap Creator Ver.8.1"
                "</name>\n"
            )

            # ==========================================
            # STARTアイコン
            # ==========================================

            f.write(
                '<Style id="startStyle">'
                '<IconStyle>'
                '<scale>1.2</scale>'
                '<Icon>'
                '<href>'
                'https://nissuiko0691.github.io/'
                'mabechi/icons/start.png'
                '</href>'
                '</Icon>'
                '</IconStyle>'
                '</Style>\n'
            )

            # ==========================================
            # GOALアイコン
            # ==========================================

            f.write(
                '<Style id="goalStyle">'
                '<IconStyle>'
                '<scale>1.2</scale>'
                '<Icon>'
                '<href>'
                'https://nissuiko0691.github.io/'
                'mabechi/icons/goal.png'
                '</href>'
                '</Icon>'
                '</IconStyle>'
                '</Style>\n'
            )

            # ==========================================
            # 写真ポイント
            # ==========================================

            for photo in route:

                f.write(
                    "<Placemark>\n"
                )

                # --------------------------------------
                # START / GOAL
                # --------------------------------------

                if photo.order == 1:

                    f.write(
                        "<styleUrl>"
                        "#startStyle"
                        "</styleUrl>\n"
                    )

                elif photo.order == total:

                    f.write(
                        "<styleUrl>"
                        "#goalStyle"
                        "</styleUrl>\n"
                    )

                # --------------------------------------
                # タイトル
                # --------------------------------------

                title = (
                    f"No."
                    f"{photo.order:03d}"
                )

                f.write(
                    f"<name>"
                    f"{title}"
                    f"</name>\n"
                )

                # ======================================
                # ポップアップ
                # ======================================

                f.write(
                    "<description>"
                    "<![CDATA["
                )

                # --------------------------------------
                # No.
                # --------------------------------------

                f.write(
                    f"<h3>"
                    f"{title}"
                    f"</h3>"
                )

                # --------------------------------------
                # 写真
                # --------------------------------------

                if photo.photo_url:

                    f.write(
                        f'<img '
                        f'src="{photo.photo_url}" '
                        f'width="350">'
                        f'<br><br>'
                    )

                # --------------------------------------
                # 撮影方向
                # --------------------------------------

                if photo.direction is not None:

                    direction = (
                        float(
                            photo.direction
                        )
                        % 360.0
                    )

                    direction_name = (
                        self.get_direction_name(
                            direction
                        )
                    )

                    direction_arrow = (
                        self.get_direction_arrow(
                            direction
                        )
                    )

                    f.write(
                        "<b>"
                        "撮影方向"
                        "</b>"
                        "<br>"
                    )

                    f.write(
                        '<span '
                        'style="font-size:28px;">'
                        f"{direction_arrow}"
                        '</span>'
                    )

                    f.write(
                        "&nbsp;&nbsp;"
                    )

                    f.write(
                        f"{direction:.1f}°"
                        f"（{direction_name}）"
                        "<br><br>"
                    )

                # --------------------------------------
                # 撮影日時
                # --------------------------------------

                if photo.datetime:

                    f.write(
                        "<b>"
                        "撮影日時"
                        "</b>"
                        "<br>"
                        f"{photo.datetime}"
                        "<br><br>"
                    )

                # --------------------------------------
                # 撮影順
                # --------------------------------------

                f.write(
                    "<b>"
                    "撮影順"
                    "</b>"
                    "<br>"
                    f"{photo.order} / {total}"
                )

                f.write(
                    "]]>"
                    "</description>\n"
                )

                # ======================================
                # 座標
                # ======================================

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

            # ==========================================
            # 撮影ルート
            # ==========================================

            if len(route) >= 2:

                f.write(
                    "<Placemark>"
                )

                f.write(
                    "<name>"
                    "撮影ルート"
                    "</name>"
                )

                f.write(
                    "<Style>"
                    "<LineStyle>"
                    "<color>"
                    "ff0000ff"
                    "</color>"
                    "<width>"
                    "4"
                    "</width>"
                    "</LineStyle>"
                    "</Style>"
                )

                f.write(
                    "<LineString>"
                    "<tessellate>"
                    "1"
                    "</tessellate>"
                    "<coordinates>\n"
                )

                for photo in route:

                    f.write(
                        f"{photo.lon},"
                        f"{photo.lat},"
                        f"0\n"
                    )

                f.write(
                    "</coordinates>"
                    "</LineString>"
                    "</Placemark>\n"
                )

            # ==========================================
            # 終了
            # ==========================================

            f.write(
                "</Document>\n"
            )

            f.write(
                "</kml>\n"
            )

        return kml_file