"""
Brand and logo lookup for startup CLI messaging.
"""

from __future__ import annotations

import io
import json
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import quote
from urllib.request import Request, urlopen

from rich.text import Text

BRANDFETCH_BRAND_API = "https://api.brandfetch.io/v2/brands/{domain}"
BRANDFETCH_LOGO_API = "https://logo.brandfetch.io/{domain}"

try:
    from PIL import Image
    from PIL import ImageFilter
    from PIL import ImageOps
except ImportError:
    Image = None  # type: ignore[assignment]


@dataclass
class BrandInfo:
    name: str
    domain: str
    logo_url: str


@dataclass
class BrandIntro:
    source: BrandInfo
    target: BrandInfo

    @property
    def sentence(self) -> str:
        return "We're able to translate Salesforce speak into something you can understand."

    @property
    def pun_line(self) -> str:
        return "Mother-in-Law Decoder mode: from cloudy hints to Apple-clear answers."


def _default_brand_name(domain: str) -> str:
    root = domain.split(".")[0].strip()
    return root.capitalize() if root else domain


def _pick_logo_url(brand_data: dict[str, Any]) -> Optional[str]:
    logos = brand_data.get("logos") or []
    preferred_types = ("icon", "logo", "symbol")
    preferred_formats = ("png", "jpg", "jpeg", "webp", "svg")

    def pick_from_formats(formats: list[dict[str, Any]]) -> Optional[str]:
        for fmt in preferred_formats:
            for item in formats:
                if str(item.get("format", "")).lower() == fmt and item.get("src"):
                    return str(item["src"])
        for item in formats:
            if item.get("src"):
                return str(item["src"])
        return None

    for logo_type in preferred_types:
        for logo in logos:
            if str(logo.get("type", "")).lower() == logo_type:
                src = pick_from_formats(logo.get("formats") or [])
                if src:
                    return src

    for logo in logos:
        src = pick_from_formats(logo.get("formats") or [])
        if src:
            return src

    icon = brand_data.get("icon")
    if isinstance(icon, str) and icon:
        return icon

    return None


def fetch_brand_info(
    domain: str,
    api_key: Optional[str],
    timeout_sec: float = 2.0,
) -> BrandInfo:
    clean_domain = domain.strip().lower()
    fallback = BrandInfo(
        name=_default_brand_name(clean_domain),
        domain=clean_domain,
        logo_url=BRANDFETCH_LOGO_API.format(domain=quote(clean_domain)),
    )

    if not api_key:
        return fallback

    request = Request(
        BRANDFETCH_BRAND_API.format(domain=quote(clean_domain)),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": "mother-in-law-decoder/1.0",
        },
    )

    try:
        with urlopen(request, timeout=timeout_sec) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception:
        return fallback

    name = str(payload.get("name") or fallback.name)
    logo_url = _pick_logo_url(payload) or fallback.logo_url
    return BrandInfo(name=name, domain=clean_domain, logo_url=logo_url)


def build_brand_intro(
    source_domain: str = "salesforce.com",
    target_domain: str = "apple.com",
    api_key: Optional[str] = None,
) -> BrandIntro:
    source = fetch_brand_info(source_domain, api_key=api_key)
    target = fetch_brand_info(target_domain, api_key=api_key)
    return BrandIntro(source=source, target=target)


def fetch_logo_bytes(logo_url: str, timeout_sec: float = 2.0) -> Optional[bytes]:
    """Fetch logo bytes from URL."""
    request = Request(
        logo_url,
        headers={
            "Accept": "image/*",
            "User-Agent": "mother-in-law-decoder/1.0",
        },
    )
    try:
        with urlopen(request, timeout=timeout_sec) as response:
            return response.read()
    except Exception:
        return None


def can_render_images() -> bool:
    """Whether Pillow is available for inline image rendering."""
    return Image is not None


def render_logo_text(
    logo_bytes: bytes,
    max_width_chars: int = 28,
    max_height_chars: int = 10,
    style: str = "default",
) -> Optional[Text]:
    """Render an image into terminal-friendly colored block characters."""
    if Image is None:
        return None

    try:
        with Image.open(io.BytesIO(logo_bytes)) as img:
            rgba = img.convert("RGBA")
    except Exception:
        return None

    if style == "clear":
        # For crisp logos, crop transparent margins and render on light background.
        alpha = rgba.getchannel("A")
        bbox = alpha.point(lambda a: 255 if a > 12 else 0).getbbox()
        if bbox:
            rgba = rgba.crop(bbox)
        background = Image.new("RGBA", rgba.size, (245, 245, 245, 255))
        composed = Image.alpha_composite(background, rgba).convert("RGB")
        composed = ImageOps.autocontrast(composed)
        composed = composed.filter(ImageFilter.UnsharpMask(radius=1.6, percent=220, threshold=1))
    else:
        # Composite on dark background so transparent brand icons remain visible.
        background = Image.new("RGBA", rgba.size, (24, 24, 24, 255))
        composed = Image.alpha_composite(background, rgba).convert("RGB")

    src_w, src_h = composed.size
    if src_w <= 0 or src_h <= 0:
        return None

    max_h_pixels = max(2, max_height_chars * 2)
    scale = min(max_width_chars / src_w, max_h_pixels / src_h, 1.0)
    out_w = max(2, int(src_w * scale))
    out_h = max(2, int(src_h * scale))
    if out_h % 2 != 0:
        out_h += 1

    if style == "pixelated":
        # Deliberately degrade source logo for a "confusing" effect.
        tiny_w = max(6, out_w // 2)
        tiny_h = max(6, out_h // 2)
        tiny = composed.resize((tiny_w, tiny_h), Image.Resampling.BILINEAR)
        tiny = tiny.quantize(colors=20, method=Image.Quantize.MEDIANCUT).convert("RGB")
        resized = tiny.resize((out_w, out_h), Image.Resampling.NEAREST)
    else:
        resized = composed.resize((out_w, out_h), Image.Resampling.LANCZOS)

    if style == "clear":
        # Push near-monochrome logos (like Apple) to cleaner edges.
        gray = ImageOps.grayscale(resized)
        resized = gray.point(lambda p: 255 if p > 165 else 0).convert("RGB")
    px = resized.load()

    text = Text()
    for y in range(0, out_h, 2):
        for x in range(out_w):
            r1, g1, b1 = px[x, y]
            r2, g2, b2 = px[x, y + 1]
            style = f"rgb({r1},{g1},{b1}) on rgb({r2},{g2},{b2})"
            text.append("▀", style=style)
        if y + 2 < out_h:
            text.append("\n")

    return text
