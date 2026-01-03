from typing import Literal

HexMode = Literal["none", "\\x", "0x"]


def string_to_hex(
    value: str, *, mode: HexMode = "none", encoding: str = "utf-8", separator: str = ""
):
    raw = value.encode(encoding)
    hex_bytes = [f"{b:02x}" for b in raw]

    if mode == "none":
        return separator.join(hex_bytes)
    if mode == "\\x":
        return separator.join(f"\\x{hb}" for hb in hex_bytes)
    if mode == "0x":
        return separator.join(f"0x{hb}" for hb in hex_bytes)
