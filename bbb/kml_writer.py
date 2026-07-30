from pathlib import Path


class KMLWriter:

    def __init__(self, project_dir):

        self.project_dir = Path(project_dir)
        self.output_dir = self.project_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

    def write(self, photo_list):

        kml_file = self.output_dir / "MyMaps.kml"

        total = len(photo_list)

        with open(kml_file, "w", encoding="utf-8") as f:

            # XMLヘッダー
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            f.write("<Document>\n")
            f.write("<name>PhotoMap Creator Ver.8</name>\n")

            f.write("<Style id=\"startStyle\">\n")
            f.write("<IconStyle>\n")
            f.write("<scale>15.0</scale>\n")
            f.write("<Icon>\n")
            f.write("<href>https://nissuiko0691.github.io/mabechi/icons/start.png</href>\n")
            f.write("</Icon>\n")
            f.write("</IconStyle>\n")
            f.write("</Style>\n")

            f.write("<Style id=\"goalStyle\">\n")
            f.write("<IconStyle>\n")
            f.write("<scale>15.0</scale>\n")
            f.write("<Icon>\n")
            f.write("<href>https://nissuiko0691.github.io/mabechi/icons/goal.png</href>\n")
            f.write("</Icon>\n")
            f.write("</IconStyle>\n")
            f.write("</Style>\n")

            #===========================
            # 写真マーカー
            #===========================
            for photo in photo_list:

                if photo.lat is None or photo.lon is None:
                    continue

                # タイトル
                
                f.write("<Placemark>\n")

                if photo.order == 1:
                    f.write("<styleUrl>#startStyle</styleUrl>\n")

                elif photo.order == total:
                    f.write("<styleUrl>#goalStyle</styleUrl>\n")

                title = f"No.{photo.order:03d}"

                f.write(f"<name>{title}</name>\n")

                f.write("<description><![CDATA[")

                f.write(f"<h3>{photo.name}</h3>")

                # 写真
                if photo.photo_url:
                    f.write(
                        f'<img src="{photo.photo_url}" width="350"><br><br>'
                    )

                # 撮影日時
                if photo.datetime:
                    f.write(
                        f"<b>撮影日時</b><br>{photo.datetime}<br><br>"
                    )

                # 撮影順
                f.write(
                    f"<b>撮影順</b><br>{photo.order} / {total}"
                )

                f.write("]]></description>\n")

                f.write("<Point>\n")
                f.write(
                    f"<coordinates>{photo.lon},{photo.lat},0</coordinates>\n"
                )
                f.write("</Point>\n")

                f.write("</Placemark>\n")

            #===========================
            # 撮影ルート
            #===========================
            route = [
                p for p in photo_list
                if p.lat is not None and p.lon is not None
            ]

            if len(route) >= 2:

                f.write("<Placemark>\n")
                f.write("<name>撮影ルート</name>\n")

                f.write("<Style>\n")
                f.write("<LineStyle>\n")

                # 赤線
                f.write("<color>ff0000ff</color>\n")

                # 線幅
                f.write("<width>4</width>\n")

                f.write("</LineStyle>\n")
                f.write("</Style>\n")

                f.write("<LineString>\n")
                f.write("<tessellate>1</tessellate>\n")
                f.write("<coordinates>\n")

                for p in route:
                    f.write(f"{p.lon},{p.lat},0\n")

                f.write("</coordinates>\n")
                f.write("</LineString>\n")

                f.write("</Placemark>\n")

            f.write("</Document>\n")




            f.write("</kml>\n")

        return kml_file