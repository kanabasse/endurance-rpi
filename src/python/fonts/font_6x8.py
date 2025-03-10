# coding=utf-8

char_bitmap = {
    ' ':  [0x00, 0x00, 0x00],
    '!':  [0x60, 0xFA, 0x60],
    '"':  [0xE0, 0xC0, 0x00, 0xE0, 0xC0],
    '#':  [0x24, 0x7E, 0x24, 0x7E, 0x24],
    '$':  [0x24, 0xD4, 0x56, 0x48],
    '%':  [0xC6, 0xC8, 0x10, 0x26, 0xC6],
    '&':  [0x6C, 0x92, 0x6A, 0x04, 0x0A],
    '\'': [0xC0, 0xE0],
    '(':  [0x7C, 0x82],
    ')':  [0x82, 0x7C],
    '*':  [0x10, 0x7C, 0x38, 0x7C, 0x10],
    '+':  [0x10, 0x10, 0x7C, 0x10, 0x10],
    ',':  [0x06, 0x07],
    '-':  [0x10, 0x10, 0x10, 0x10, 0x10],
    '.':  [0x06, 0x06],
    '/':  [0x04, 0x08, 0x10, 0x20, 0x40],
    ':':  [0x36, 0x36],
    ';':  [0x36, 0x37],
    '<':  [0x10, 0x28, 0x44, 0x82],
    '=':  [0x24, 0x24, 0x24, 0x24, 0x24],
    '>':  [0x82, 0x44, 0x28, 0x10],
    '?':  [0x40, 0x80, 0x9A, 0x90, 0x60],
    '@':  [0x7C, 0x82, 0xBA, 0xAA, 0x78],
    '{':  [0x10, 0x7C, 0x82, 0x82],
    '}':  [0x82, 0x82, 0x7C, 0x10],
    '£':  [0x12, 0x7C, 0x92, 0x92, 0x46],
    '[':  [0xFE, 0x82, 0x82],
    '\\': [0x40, 0x20, 0x10, 0x08, 0x04],
    ']':  [0x82, 0x82, 0xFE],
    '^':  [0x20, 0x40, 0x80, 0x40, 0x20],
    '_':  [0x01, 0x01, 0x01, 0x01, 0x01],
    '0':  [0x7C, 0x8A, 0x92, 0xA2, 0x7C],
    '1':  [0x42, 0xFE, 0x02],
    '2':  [0x46, 0x8A, 0x92, 0x92, 0x62],
    '3':  [0x44, 0x92, 0x92, 0x92, 0x6C],
    '4':  [0x18, 0x28, 0x48, 0xFE, 0x08],
    '5':  [0xF4, 0x92, 0x92, 0x92, 0x8C],
    '6':  [0x3C, 0x52, 0x92, 0x92, 0x0C],
    '7':  [0x80, 0x8E, 0x90, 0xA0, 0xC0],
    '8':  [0x6C, 0x92, 0x92, 0x92, 0x6C],
    '9':  [0x60, 0x92, 0x92, 0x94, 0x78],
    'A':  [0x7E, 0x88, 0x88, 0x88, 0x7E],
    'B':  [0xFE, 0x92, 0x92, 0x92, 0x6C],
    'C':  [0x7C, 0x82, 0x82, 0x82, 0x44],
    'D':  [0xFE, 0x82, 0x82, 0x82, 0x7C],
    'E':  [0xFE, 0x92, 0x92, 0x92, 0x82],
    'F':  [0xFE, 0x90, 0x90, 0x90, 0x80],
    'G':  [0x7C, 0x82, 0x92, 0x92, 0x5E],
    'H':  [0xFE, 0x10, 0x10, 0x10, 0xFE],
    'I':  [0x82, 0xFE, 0x82],
    'J':  [0x0C, 0x02, 0x02, 0x02, 0xFC],
    'K':  [0xFE, 0x10, 0x28, 0x44, 0x82],
    'L':  [0xFE, 0x02, 0x02, 0x02, 0x02],
    'M':  [0xFE, 0x40, 0x20, 0x40, 0xFE],
    'N':  [0xFE, 0x40, 0x20, 0x10, 0xFE],
    'O':  [0x7C, 0x82, 0x82, 0x82, 0x7C],
    'P':  [0xFE, 0x90, 0x90, 0x90, 0x60],
    'Q':  [0x7C, 0x82, 0x8A, 0x84, 0x7A],
    'R':  [0xFE, 0x90, 0x90, 0x98, 0x66],
    'S':  [0x64, 0x92, 0x92, 0x92, 0x4C],
    'T':  [0x80, 0x80, 0xFE, 0x80, 0x80],
    'U':  [0xFC, 0x02, 0x02, 0x02, 0xFC],
    'V':  [0xF8, 0x04, 0x02, 0x04, 0xF8],
    'W':  [0xFC, 0x02, 0x3C, 0x02, 0xFC],
    'X':  [0xC6, 0x28, 0x10, 0x28, 0xC6],
    'Y':  [0xE0, 0x10, 0x0E, 0x10, 0xE0],
    'Z':  [0x8E, 0x92, 0xA2, 0xC2],
    'a':  [0x04, 0x2A, 0x2A, 0x2A, 0x1E],
    'b':  [0xFE, 0x22, 0x22, 0x22, 0x1C],
    'c':  [0x1C, 0x22, 0x22, 0x22, 0x14],
    'd':  [0x1C, 0x22, 0x22, 0x22, 0xFE],
    'e':  [0x1C, 0x2A, 0x2A, 0x2A, 0x10],
    'f':  [0x10, 0x7E, 0x90, 0x90],
    'g':  [0x18, 0x25, 0x25, 0x25, 0x3E],
    'h':  [0xFE, 0x20, 0x20, 0x1E],
    'i':  [0xBE, 0x02],
    'j':  [0x02, 0x01, 0x21, 0xBE],
    'k':  [0xFE, 0x08, 0x14, 0x22],
    'l':  [0xFE, 0x02],
    'm':  [0x3E, 0x20, 0x18, 0x20, 0x1E],
    'n':  [0x3E, 0x20, 0x20, 0x1E],
    'o':  [0x1C, 0x22, 0x22, 0x22, 0x1C],
    'p':  [0x3F, 0x22, 0x22, 0x22, 0x1C],
    'q':  [0x1C, 0x22, 0x22, 0x22, 0x3F],
    'r':  [0x22, 0x1E, 0x22, 0x20, 0x10],
    's':  [0x10, 0x2A, 0x2A, 0x2A, 0x04],
    't':  [0x20, 0x7C, 0x22, 0x24],
    'u':  [0x3C, 0x02, 0x04, 0x3E],
    'v':  [0x38, 0x04, 0x02, 0x04, 0x38],
    'w':  [0x3C, 0x06, 0x0C, 0x06, 0x3C],
    'x':  [0x36, 0x08, 0x08, 0x36],
    'y':  [0x39, 0x05, 0x06, 0x3C],
    'z':  [0x26, 0x2A, 0x2A, 0x32],
    'smiley': [0x02, 0x61, 0x61, 0x01, 0x01, 0x61, 0x61, 0x02],
    'clock': [0x3c, 0x42, 0x81, 0xb9, 0x89, 0x89, 0x42, 0x3c],
}


def get(c):
    return char_bitmap.get(c)

def getstr(s):
    returned = []
    for _, char in enumerate(s):
        returned += get(char) + [0x00]

    return returned