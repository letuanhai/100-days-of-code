# no gap between marks within a character
# short gap between letters of 1 spaces
# medium gap between words of 3 spaces

LETTER_GAP = " " * 1
WORD_GAP = " " * 2

CODE_MAP = {
    "a": ".-",
    "i": "..",
    "r": ".-.",
    "b": "-...",
    "j": ".---",
    "s": "...",
    "c": "-.-.",
    "k": "-.-",
    "t": "-",
    "d": "-..",
    "l": ".-..",
    "u": "..-",
    "e": ".",
    "m": "--",
    "v": "...-",
    "n": "-.",
    "w": ".--",
    "f": "..-.",
    "o": "---",
    "x": "-..-",
    "g": "--.",
    "p": ".--.",
    "y": "-.--",
    "h": "....",
    "q": "--.-",
    "z": "--..",
    "1": ".----",
    "6": "-....",
    "2": "..---",
    "7": "--...",
    "3": "...--",
    "8": "---..",
    "4": "....-",
    "9": "----.",
    "5": ".....",
    "0": "-----",
    ".": ".-.-.-",
    ",": "--..--",
    ":": "---...",
    "?": "..--..",
    "'": ".----.",
    "-": "-....-",
    "/": "-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    '"': ".-..-.",
    "=": "-...-",
    "+": ".-.-.",
    "@": ".--.-.",
    "!": "-.-.--",
}


def encode(message: str) -> str:
    """Encode a message in Morse code."""
    # standardize the message
    message = message.lower().strip()
    encoded_message = ""
    for character in message:
        if character == " ":
            encoded_message += WORD_GAP
            continue
        try:
            encoded_message += CODE_MAP[character] + LETTER_GAP
        except KeyError:
            raise ValueError(f"Invalid character: {character}")
    return encoded_message.strip()
