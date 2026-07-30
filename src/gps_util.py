class GPSUtil:

    @staticmethod
    def dms_to_deg(dms, ref):

        deg = float(dms[0])
        minute = float(dms[1])
        sec = float(dms[2])

        value = deg + minute / 60 + sec / 3600

        if ref in ("S", "W"):
            value *= -1

        return value

    @staticmethod
    def get_lat_lon(gps):

        if gps is None:
            return None, None

        try:

            lat = GPSUtil.dms_to_deg(
                gps["GPSLatitude"],
                gps["GPSLatitudeRef"]
            )

            lon = GPSUtil.dms_to_deg(
                gps["GPSLongitude"],
                gps["GPSLongitudeRef"]
            )

            return lat, lon

        except Exception:
            return None, None