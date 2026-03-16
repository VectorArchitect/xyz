import socket
from crc_input import calcrc, append_crc

# ── Request: A1 03 00 0F 00 0F  (data only, CRC will be appended) ────────────
REQUEST_DATA = bytes.fromhex('A103000F000F')

HOST, PORT = '127.0.0.1', 12345

def parse_response(data: bytes):
    """
    Buffer indexing (1-based as per your spec):
    Buf[17] = data[16]  → Alarm 1–8
    Buf[18] = data[17]  → Alarm 1–8

    Word registers:
    HC_con  → Buf[7,8]   = data[6:8]
    AS_con  → Buf[9,10]  = data[8:10]
    CM_con  → Buf[11,12] = data[10:12]
    CP_con  → Buf[13,14] = data[12:14]
    CS_con  → Buf[15,16] = data[14:16]
    """
    print("\n─── Parsed Server Response ─────────────────────────────")
    print(f"  Full packet ({len(data)} bytes): {data.hex(' ').upper()}")

    if len(data) < 18:
        print("  ⚠️  Response too short to parse all fields.")
        return

    buf17 = data[16]
    buf18 = data[17]
    print(f"\n  Buffer[17] Alarm 1–8 : 0x{buf17:02X}  (bits: {buf17:08b})")
    print(f"  Buffer[18] Alarm 1–8 : 0x{buf18:02X}  (bits: {buf18:08b})")

    def word(hi, lo):
        return (hi << 8) | lo

    hc  = word(data[6],  data[7])
    as_ = word(data[8],  data[9])
    cm  = word(data[10], data[11])
    cp  = word(data[12], data[13])
    cs  = word(data[14], data[15])

    print(f"\n  HC_con [7,8]   : 0x{hc:04X}  ({hc})")
    print(f"  AS_con [9,10]  : 0x{as_:04X}  ({as_})")
    print(f"  CM_con [11,12] : 0x{cm:04X}  ({cm})")
    print(f"  CP_con [13,14] : 0x{cp:04X}  ({cp})")
    print(f"  CS_con [15,16] : 0x{cs:04X}  ({cs})")
    print("────────────────────────────────────────────────────────\n")


try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Connected to server {HOST}:{PORT}")

    while True:
        choice = input("\nSend request? (y/n) or '/exit': ").strip().lower()

        if choice == '/exit':
            print("Client disconnected.")
            break

        elif choice in ('y', 'yes'):
            # Append CRC to request before sending
            packet = append_crc(REQUEST_DATA)
            data_list = list(REQUEST_DATA)
            crch, crcl = calcrc(data_list, len(data_list) - 1)

            print(f"\nSending ({len(packet)} bytes): {packet.hex(' ').upper()}")
            print(f"  → CRC appended: CRCH={crch:02X}  CRCL={crcl:02X}")

            client_socket.send(packet)

            # Receive response
            response = client_socket.recv(1024)
            print(f"\nRaw response ({len(response)} bytes): {response.hex(' ').upper()}")

            # Parse & display
            parse_response(response)

        else:
            print("Please enter 'y', 'n', or '/exit'.")

except Exception as e:
    print(f"Error: {e}")
finally:
    client_socket.close()
