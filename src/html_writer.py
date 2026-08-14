from pathlib import Path
from datetime import datetime
from config import MY_MAPS_ID


class HtmlWriter:


    def __init__(self, project):

        self.project = Path(project)

        self.output_file = (
            self.project
            / "output"
            / "photo_book.html"
        )


    def write(self, photos):

        today = datetime.now().strftime("%Y/%m/%d")


        with open(
            self.output_file,
            "w",
            encoding="utf-8"
        ) as f:


            # ---------------------------------
            # HTML + CSS
            # ---------------------------------

            f.write("""
<!DOCTYPE html>

<html lang="ja">

<head>

<meta charset="UTF-8">

<title>写真帳</title>


<style>


@page {

    size:A4 portrait;

    margin:12mm 10mm;

}



body {

    font-family:Meiryo,sans-serif;

    margin:0;

}



/* 表紙 */

.cover {

    width:190mm;

    height:265mm;

    border:2px solid black;

    box-sizing:border-box;

    display:flex;

    flex-direction:column;

    justify-content:center;

    align-items:center;

    page-break-after:always;

}



.cover h1 {

    font-size:36px;

    padding:10mm 30mm;

    border-bottom:2px solid black;

}



.cover p {

    font-size:18px;

    margin:5mm;

}



/* 写真ページ */

.page {

    width:190mm;

    height:273mm;

    display:flex;

    flex-direction:column;

    gap:6mm;

    page-break-after:always;

}



/* 写真枠 */

.card {
    border: 1px solid #666;
    padding: 2mm;
    box-sizing: border-box;
    overflow: hidden;
    position: relative;
}



/* 番号 */

.number {
    position: absolute;
    top: 5px;
    left: 5px;

    background: rgba(255, 255, 255, 0.9);
    color: #000000;

    font-size: 16px;
    font-weight: bold;

    padding: 3px 5px;

    line-height: 1;

    z-index: 10;
}



/* 写真 */

.photo {

    width:95mm;

    height:80mm;

    object-fit:contain;

    float:left;

    margin-right:8mm;

}



/* 情報 */

.info {

    font-size:12px;

    line-height:1.8;

    padding-top:8mm;

}



.clear {

    clear:both;

}


</style>


</head>


<body>

""")



            # ---------------------------------
            # 表紙
            # ---------------------------------

            f.write(f"""

<div class="cover">


<h1>
写真帳
</h1>


<p>
プロジェクト：{self.project.name}
</p>


<p>
写真枚数：{len(photos)}枚
</p>


<p>
作成日：{today}
</p>


</div>

""")



            # ---------------------------------
            # 写真帳
            # ---------------------------------

            for index, photo in enumerate(photos):


                if index % 3 == 0:

                    f.write(
                        """
<div class="page">
"""
                    )


                f.write(
                    f"""

<div class="card">


<div class="number">
    No.{photo.order:03}
</div>


<img

class="photo"

src="{photo.photo_url}">


<div class="info">


ファイル名：
{photo.name}

<br>


撮影日時：
{photo.datetime}

<br>

"""
                )


                if photo.lat is not None and photo.lon is not None:


                    map_url = (
                        "https://maps.google.com/?q="
                        f"{photo.lat},{photo.lon}"
                    )


                    f.write(
                        f"""
緯度：
{photo.lat}

<br>

経度：
{photo.lon}

<br><br>


<a href="{map_url}" target="_blank">

Googleマップで見る

</a>

<br>

"""
                    )


                    mymap_url = (
                        "https://www.google.com/maps/d/viewer?"
                        f"mid={MY_MAPS_ID}"
                        f"&ll={photo.lat},{photo.lon}"
                    )


                    f.write(
                        f"""

<a href="{mymap_url}" target="_blank">

My Mapsで位置を見る

</a>

"""
                    )


                f.write(
                    """

</div>


<div class="clear"></div>


</div>

"""
                )



                if index % 3 == 2:

                    f.write(
                        "</div>\n"
                    )



            # 最後のページ処理

            if len(photos) % 3 != 0:

                f.write(
                    "</div>\n"
                )



            f.write("""

</body>

</html>

""")



        print()

        print("HTML写真帳を作成しました。")

        print(self.output_file)