import datetime

def calculate_checksum(data):
    """Calculate the checksum by summing the data bytes."""
    return sum(data) & 0xFFFF  # Get the lower 2 bytes of the sum

def create_packet(packet_type, data):
    """Create a packet with the given type and data."""
    header = [0x24]  # Header $
    
    # now = datetime.datetime.now()
    # date_time = [
    #     now.day,       # Day
    #     now.month,     # Month
    #     now.year % 100,  # Year (last two digits)
    #     now.hour,      # Hour
    #     now.minute,    # Minute
    #     now.second     # Second
    # ]
    now = datetime.datetime.now()
    date_time = [int(now.strftime('%d')), int(now.strftime('%m')), int(now.strftime('%y'))]
    header.extend(date_time)
    header.extend(date_time)
    
    # Header Packet Type
    header.append(packet_type)
    
    # Header Data Length
    data_length = len(data)
    header.append(data_length)
    
    # Footer Checksum
    checksum = calculate_checksum(data)
    footer = [(checksum >> 8) & 0xFF, checksum & 0xFF]  # Checksum in 2 bytes
    
    # Footer #
    footer.append(0x23)  # Footer #
    
    # Complete packet
    packet = header + data + footer
    
    print("Header:", header)
    print("Data:", bytearray(data))
    print("Footer:", footer)
    print("Complete packet:", bytearray(packet))
    
    return bytearray(packet)

def validate_packet(packet):
    """Validate the packet structure and checksum."""
    header_length = 9  # 1 (Header $) + 6 (Date-Time) + 1 (Packet Type) + 1 (Data Length)
    footer_length = 3  # 2 (Checksum) + 1 (Footer #)
    
    if len(packet) < header_length + footer_length:
        return False, "Packet too short"
    
    # Validate Header
    if packet[0] != 0x24:
        return False, "Invalid Header $"
    
    # Validate Data Length
    data_length = packet[8]
    if len(packet) != header_length + data_length + footer_length:
        return False, "Invalid Data Length"
    
    # Validate Footer #
    if packet[-1] != 0x23:
        return False, "Invalid Footer #"
    
    # Validate Checksum
    data = packet[9:-3]
    expected_checksum = calculate_checksum(data)
    provided_checksum = (packet[-3] << 8) | packet[-2]
    
    if expected_checksum != provided_checksum:
        return False, "Invalid Checksum"
    
    return True, "Valid Packet"

def extract_data(packet):
    """Extract and return data from the packet."""
    # Ensure packet is valid before extraction
    is_valid, message = validate_packet(packet)
    if not is_valid:
        return None, message
    
    # Extract Date and Time
    day = packet[1]
    month = packet[2]
    year = packet[3]
    hour = packet[4]
    minute = packet[5]
    second = packet[6]
    
    date_time = datetime.datetime(year + 2000, month, day, hour, minute, second)
    
    # Extract Packet Type
    packet_type = packet[7]
    # Extract Data Length
    data_length = packet[8]
    
    # Extract Data
    data = packet[9:9+data_length]
    
    # Extract Checksum
    checksum = (packet[-3] << 8) | packet[-2]
    
    extracted_info = {
        "date_time": date_time,
        "packet_type": packet_type,
        "data_length": data_length,
        "data": data,
        "checksum": checksum
    }
    
    return extracted_info, "Data extracted successfully"

def send_data(data):
    """Placeholder function for sending data."""
    print(f"Sending data: {data}")

# Example Initialization Data
initialization_data = [
    0x01,  # LEV Protocol Version
    0x00,  # Reserved
    0x01,  # Charger State (Initialization)
    0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x30, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46  # LEV Charge Point Id
]

packet_type = 0x01  # Initialization
packet = create_packet(packet_type, initialization_data)

# Validate the packet
is_valid, message = validate_packet(packet)

if is_valid:
    print("Packet is valid, sending data...")
    send_data(packet)
    
    # Extract data from packet
    extracted_info, message = extract_data(packet)
    if extracted_info:
        print("Extracted Information:")
        print("Date and Time:", extracted_info["date_time"])
        print("Packet Type:", extracted_info["packet_type"])
        print("Data Length:", extracted_info["data_length"])
        print("Data:", list(extracted_info["data"]))
        print("Checksum:", extracted_info["checksum"])
    else:
        print(f"Data extraction failed: {message}")
else:
    print(f"Packet validation failed: {message}")
