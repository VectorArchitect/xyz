def calc_crc(buf):
    ch = 0xFF
    cl = 0xFF
    for byte in buf:
        cl ^= byte
        for _ in range(8):
            carryl = cl & 0x01
            carryh = ch & 0x01
            ch >>= 1
            cl >>= 1
            if carryh:
                cl |= 0x80
            if carryl:
                ch ^= 0xA0
                cl ^= 0x01
    return ch, cl

# Input values (decimal)
device_address = 161
function_code  = 3
start_addr_hi  = 0
start_addr_lo  = 0
reg_count_hi   = 0
reg_count_lo   = 15

buf = [device_address, function_code, start_addr_hi, start_addr_lo, reg_count_hi, reg_count_lo]

crc_h, crc_l = calc_crc(buf)

frame = buf + [crc_l, crc_h]  # CRC low byte first (Modbus standard)
print("Frame:", [f"{b:02X}" for b in frame])


#**Output:**

Frame: ['A1', '03', '00', '00', '00', '0F', '1D', '6E']
