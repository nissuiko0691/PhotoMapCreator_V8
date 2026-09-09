from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class PhotoData:
    """写真1枚分の情報"""

    name: str
    path: Path

    datetime: Optional[str]

    lat: Optional[float]
    lon: Optional[float]

    # 撮影方向
    # 0°   = 北
    # 90°  = 東
    # 180° = 南
    # 270° = 西
    direction: Optional[float] = None

    photo_url: str = ""

    order: int = 0