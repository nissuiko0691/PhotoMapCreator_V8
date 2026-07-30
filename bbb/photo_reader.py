from pathlib import Path


class PhotoReader:

    def __init__(self, project_dir):

        self.project_dir = Path(project_dir)
        self.photo_dir = self.project_dir / "photos"

    def get_photos(self):

        # photosフォルダが存在しない
        if not self.photo_dir.exists():
            return []

        photos = []

        for photo in self.photo_dir.iterdir():

            if not photo.is_file():
                continue

            if photo.suffix.lower() in [".jpg", ".jpeg"]:

                photos.append(photo)

        # ファイル名順
        photos.sort()

        return photos