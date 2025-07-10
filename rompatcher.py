"""
Patch rom after it's been built
usage: rompatcher.py romin romout
romin is the input rom, romout is the output rom
"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("romin")
parser.add_argument("romout")
args = parser.parse_args()
checksum_std = 0
with open(args.romin,"r+b") as rom:
    buffer = bytearray()
    buffer.extend(rom.read())
"""
Pad rom, then write new rom end
Note that rom end is how much rom the cartridge maps to the system, not the overall size of the rom
This distinction matters for mappers like SSF2
"""
print("padfrom:",hex(len(buffer)))
while len(buffer) % 32 != 0:
# while len(buffer) < 0x400000:
    buffer.append(0x69)
romend = len(buffer)-1
print("romend:",hex(romend))
buffer[0x1A4] = 0x00
buffer[0x1A5] = romend >>16 & 0xFF
buffer[0x1A6] = romend >>8 & 0xFF
buffer[0x1A7] = romend & 0xFF

# calc standard, iterates in 32 bytes for performance
iterate = 0x200
while iterate < romend:
    checksum_std += buffer[iterate]<<8 | buffer[iterate+1]
    checksum_std += buffer[iterate+2]<<8 | buffer[iterate+3]
    checksum_std += buffer[iterate+4]<<8 | buffer[iterate+5]
    checksum_std += buffer[iterate+6]<<8 | buffer[iterate+7]
    checksum_std += buffer[iterate+8]<<8 | buffer[iterate+9]
    checksum_std += buffer[iterate+10]<<8 | buffer[iterate+11]
    checksum_std += buffer[iterate+12]<<8 | buffer[iterate+13]
    checksum_std += buffer[iterate+14]<<8 | buffer[iterate+15]
    checksum_std += buffer[iterate+16]<<8 | buffer[iterate+17]
    checksum_std += buffer[iterate+18]<<8 | buffer[iterate+19]
    checksum_std += buffer[iterate+20]<<8 | buffer[iterate+21]
    checksum_std += buffer[iterate+22]<<8 | buffer[iterate+23]
    checksum_std += buffer[iterate+24]<<8 | buffer[iterate+25]
    checksum_std += buffer[iterate+26]<<8 | buffer[iterate+27]
    checksum_std += buffer[iterate+28]<<8 | buffer[iterate+29]
    checksum_std += buffer[iterate+30]<<8 | buffer[iterate+31]
    checksum_std &= 0xFFFF
    iterate += 32
print("std:",hex(checksum_std))
buffer[0x18E] = checksum_std >>8 & 0xFF ; buffer[0x18F] = checksum_std & 0xFF 

# finish up
with open(args.romout,"w+b") as rom:
    rom.write(buffer)