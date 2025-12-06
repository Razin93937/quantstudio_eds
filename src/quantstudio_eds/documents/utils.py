def clean_string(s: str) -> str:
    """Cleans a string by stripping leading/trailing whitespaces,
    converting to lowercase, and removing special characters.
    Preserves characters used in numeric literals (., +, -, e) so floats
    and scientific notation are not corrupted.
    """
    if s is None:
        return ""
    s = s.strip().lower()
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789.+-")
    return "".join(ch for ch in s if ch in allowed)


def parse_bracketed_list(text: str) -> list[str]:
    # Handles strings like "[A, B, C]" or "[1, 2, 3]"
    if text is None:
        return []
    s = text.strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    # Split by comma, strip whitespace
    if not s.strip():
        return []
    return [clean_string(part) for part in s.split(",")]


def parse_bracketed_floats(text: str) -> list[float]:
    return [float(x) for x in parse_bracketed_list(text)]


def parse_bracketed_ints(text: str) -> list[int]:
    return [int(x) for x in parse_bracketed_list(text)]


def get_jaxb_setting_value(jaxb_setting_value):
    if jaxb_setting_value.xpath(".//JaxbValueItem/@type")[0] == "String":
        return jaxb_setting_value.xpath(".//JaxbValueItem/StringValue")[0].text
    elif jaxb_setting_value.xpath(".//JaxbValueItem/@type")[0] == "Integer":
        return int(jaxb_setting_value.xpath(".//JaxbValueItem/IntValue")[0].text)
    elif jaxb_setting_value.xpath(".//JaxbValueItem/@type")[0] == "Boolean":
        return jaxb_setting_value.xpath(".//JaxbValueItem/BooleanValue")[0].text == "true"
    elif jaxb_setting_value.xpath(".//JaxbValueItem/@type")[0] == "Double":
        return float(jaxb_setting_value.xpath(".//JaxbValueItem/DoubleValue")[0].text)
    else:
        raise ValueError("Invalid JaxbValueItem")
