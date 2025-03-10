def reverse_byte(byte):
    byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)  # Swap nibbles
    byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)  # Swap 2-bit pairs
    byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)  # Swap individual bits
    return byte

def split_uint16(value):
    """
    Splits a 16-bit unsigned integer into two 8-bit unsigned integers.

    :param value: uint16 (0 to 65535)
    :return: (low_byte, high_byte) as two uint8 values
    """
    low_byte = value & 0xFF        # Extract lower 8 bits (Least Significant Byte)
    high_byte = (value >> 8) & 0xFF  # Extract upper 8 bits (Most Significant Byte)
    return low_byte, high_byte
