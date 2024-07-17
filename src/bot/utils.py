def check_text(text: str) -> bool:
    if not text:
        return False
    if text[0] not in ["+", "-"]:
        return False
    if text[1:].isdigit():
        return True
    else:
        return False

def save_amount(data: str):
    with open("src/bot/amount.txt", "w") as file:
        file.write(data)

def get_amount() -> int:
    try:
        with open("src/bot/amount.txt", "r") as file:
            data = file.read()
        if data == "": return 0
        return int(data)
    except:
        return 0

def format_number(number: int) -> str:
    return f"{number:,}".replace(",", " ")