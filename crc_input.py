# CRC-16 | Polynomial = 0xA001

def calcrc(data, ldata):
    ch = 0xFF
    cl = 0xFF

    for i in range(ldata + 1):
        cl = cl ^ data[i]
        for ctrc in range(8):
            carryh = ch % 2
            carryl = cl % 2
            ch = ch // 2
            cl = (carryh * 128) + (cl // 2)
            if carryl != 0:
                ch = ch ^ 0xA0
                cl = cl ^ 0x01
    return ch, cl  # returns (CRCH, CRCL)


def verify_packet(packet_bytes):
    """
    Given a full packet (data + 2 CRC bytes at end),
    verifies CRC and returns (crch, crcl, is_valid).
    """
    data = list(packet_bytes[:-2])
    received_crch = packet_bytes[-2]
    received_crcl = packet_bytes[-1]
    ldata = len(data) - 1

    crch, crcl = calcrc(data, ldata)
    is_valid = (crch == received_crch) and (crcl == received_crcl)
    return crch, crcl, is_valid


def append_crc(data_bytes):
    """
    Given raw data bytes, computes and appends CRC bytes.
    Returns full packet bytes.
    """
    data = list(data_bytes)
    ldata = len(data) - 1
    crch, crcl = calcrc(data, ldata)
    return data_bytes + bytes([crch, crcl])


if __name__ == "__main__":
    packet = input("Enter hex values (space separated): ").split()
    packet_int = [int(x, 16) for x in packet]

    if len(packet_int) > 6:
        data = packet_int[:6]
        crc = packet_int[6:8]
        ldata = len(data) - 1
        crch, crcl = calcrc(data, ldata)
        print(f"Calculated → CRCH: {crch:02X}  CRCL: {crcl:02X}")
        if crc[0] == crch and crc[1] == crcl:
            print("✅ Data is Intact")
        else:
            print("❌ Data is Varied!")
    else:
        ldata = len(packet_int) - 1
        crch, crcl = calcrc(packet_int, ldata)
        print(f"Calculated → CRCH: {crch:02X}  CRCL: {crcl:02X}")
