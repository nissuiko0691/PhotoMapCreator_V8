from pathlib import Path
from datetime import datetime


class PhotoSheetWriter:


    def __init__(self, project):

        self.project = Path(project)

        self.output_file = (
            self.project
            / "output"
            / "photo_sheet.html"
        )


    def write(self, photos):

        today = datetime.now().strftime("%Y/%m/%d")


        with open(
            self.output_file,
            "w",
            encoding="utf-8"
        ) as f:


            # ---------------------------------
            # HTML開始 + CSS
            # ---------------------------------

            f.write("""
<!DOCTYPE html>
<html lang="ja">

<head>

<meta charset="UTF-8">

<title>写真一覧</title>


<style>


@page {

    size:A4 portrait;

    margin:12mm 10mm;

}



body {

    font-family: Meiryo, sans-serif;

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

    border-bottom:2px solid black;

    padding:10mm 30mm;

    margin-bottom:30mm;

}



.cover p {

    font-size:18px;

    margin:5mm;

}



/* 写真ページ */

.page {

    width:190mm;

    height:273mm;

    box-sizing:border-box;

    display:grid;

    grid-template-columns:1fr 1fr;

    grid-template-rows:repeat(3, 84mm);

    gap:6mm;

    page-break-after:always;

}



/* 写真枠 */

.card {

    border:1px solid #666;

    padding:4mm;

    height:86mm;

    box-sizing:border-box;

    overflow:hidden;

    position:relative;

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

    width:100%;

    height:72mm;

    object-fit:contain;

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
写真一覧
</h1>


<p>
プロジェクト：{self.project.name}
</p>


<p>
写真枚数：{len(photos)} 枚
</p>


<p>
作成日：{today}
</p>


</div>

""")



            # ---------------------------------
            # 写真一覧
            # ---------------------------------

            for index, photo in enumerate(photos):


                # 6枚ごとにページ開始

                if index % 6 == 0:

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


</div>

"""
                )


                # 6枚でページ終了

                if index % 6 == 5:

                    f.write(
                        "</div>\n"
                    )



            # ---------------------------------
            # 最終ページ空欄補完
            # ---------------------------------

            remainder = len(photos) % 6


            if remainder != 0:


                empty = 6 - remainder


                for _ in range(empty):

                    f.write(
                        """
<div class="card">

</div>
"""
                    )


                f.write(
                    "</div>\n"
                )



            # ---------------------------------
            # HTML終了
            # ---------------------------------

            f.write("""

</body>

</html>

""")



        print()

        print("写真一覧を作成しました。")

        print(self.output_file)