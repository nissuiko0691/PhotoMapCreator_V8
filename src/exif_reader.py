from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class ExifReader:

    def __init__(self):
        pass

    def read(self, photo_path):

        result = {
            "datetime": None,
            "gps": None,
            "tags": {}
        }

        try:

            image = Image.open(photo_path)

            exif = image._getexif()

            if not exif:
                return result

            tags = {}

            for tag_id, value in exif.items():

                tag = TAGS.get(tag_id, tag_id)

                tags[tag] = value

            result["tags"] = tags

            if "DateTimeOriginal" in tags:
                result["datetime"] = str(tags["DateTimeOriginal"])

            if "GPSInfo" in tags:

                gps = {}

                for key, value in tags["GPSInfo"].items():

                    gps[GPSTAGS.get(key, key)] = value

                result["gps"] = gps


            return result

        except Exception:

            return result