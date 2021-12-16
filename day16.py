# https://adventofcode.com/2021/day/16

import itertools
import math
from pathlib import Path

import pytest


class BitsReader:
    def __init__(self, hexstring):
        # Leading zeros trip us up, so pre-pad with ones, and read them off.
        self.bits = bin(int("F"+hexstring, 16))[6:]
        self.bit_iter = iter(self.bits)
        self.bits_read = 0

    def read_num(self, nbits):
        self.bits_read += nbits
        return int("".join(itertools.islice(self.bit_iter, nbits)), 2)

def test_read_num():
    reader = BitsReader("D2FE28")
    assert reader.read_num(3) == 6
    assert reader.read_num(3) == 4
    assert reader.read_num(5) == 0b10111
    assert reader.read_num(5) == 0b11110
    assert reader.read_num(5) == 0b00101

def parse_packet(hexstring):
    reader = BitsReader(hexstring)
    return read_packet(reader)

def read_packet(reader):
    version = reader.read_num(3)
    ptype = reader.read_num(3)
    match ptype:
        case 4:
            # Literal packet
            num = 0
            keep_reading = True
            while keep_reading:
                next5 = reader.read_num(5)
                keep_reading = next5 & 0b10000
                num <<= 4
                num += next5 & 0b01111
            return ("lit", version, num)
        case _:
            length_type = reader.read_num(1)
            packets = []
            match length_type:
                case 0:
                    bit_length = reader.read_num(15)
                    start_read = reader.bits_read
                    while (reader.bits_read - start_read) < bit_length:
                        packets.append(read_packet(reader))
                case 1:
                    packet_length = reader.read_num(11)
                    while len(packets) < packet_length:
                        packets.append(read_packet(reader))
            return ("op", version, ptype, packets)

@pytest.mark.parametrize("hexstring, packet", [
    ("D2FE28", ("lit", 6, 2021)),
    ("EE00D40C823060", ("op", 7, 3, [("lit", 2, 1), ("lit", 4, 2), ("lit", 1, 3)])),
])
def test_parse_packet(hexstring, packet):
    assert parse_packet(hexstring) == packet

def version_sum(packet):
    vsum = packet[1]
    if packet[0] == "op":
        vsum += sum(version_sum(p) for p in packet[3])
    return vsum

@pytest.mark.parametrize("hexstring, vsum", [
    ("8A004A801A8002F478", 16),
    ("620080001611562C8802118E34", 12),
    ("C0015000016115A2E0802F182340", 23),
    ("A0016C880162017C3686B18A3D4780", 31),
])
def test_version_sum(hexstring, vsum):
    assert version_sum(parse_packet(hexstring)) == vsum

if __name__ == "__main__":
    hexstring = Path("day16_input.txt").read_text().strip()
    ans = version_sum(parse_packet(hexstring))
    print(f"part 1: {ans}")

def packet_value(packet):
    match packet:
        case ("lit", _, v):
            return v
        case ("op", _, 0, packets):
            return sum(packet_value(p) for p in packets)
        case ("op", _, 1, packets):
            return math.prod(packet_value(p) for p in packets)
        case ("op", _, 2, packets):
            return min(packet_value(p) for p in packets)
        case ("op", _, 3, packets):
            return max(packet_value(p) for p in packets)
        case ("op", _, 5, packets):
            assert len(packets) == 2
            return packet_value(packets[0]) > packet_value(packets[1])
        case ("op", _, 6, packets):
            assert len(packets) == 2
            return packet_value(packets[0]) < packet_value(packets[1])
        case ("op", _, 7, packets):
            assert len(packets) == 2
            return packet_value(packets[0]) == packet_value(packets[1])

@pytest.mark.parametrize("hexstring, value", [
    ("C200B40A82", 3),
    ("04005AC33890", 54),
    ("880086C3E88112", 7),
    ("CE00C43D881120", 9),
    ("D8005AC2A8F0", 1),
    ("F600BC2D8F", 0),
    ("9C005AC2F8F0", 0),
    ("9C0141080250320F1802104A08", 1),
])
def test_packet_value(hexstring, value):
    assert packet_value(parse_packet(hexstring)) == value

if __name__ == "__main__":
    hexstring = Path("day16_input.txt").read_text().strip()
    ans = packet_value(parse_packet(hexstring))
    print(f"part 2: {ans}")
