# DNA Storage Lab - Version 1

DNA_MAP = {
    "00": "A",
    "01": "C",
    "10": "G",
    "11": "T"
}

REVERSE_MAP = {
    value: key for key, value in DNA_MAP.items()
}


def encode_text(text):
    # Convert text into binary
    binary = "".join(
        format(byte, "08b")
        for byte in text.encode("utf-8")
    )

    # Make the binary length even
    if len(binary) % 2 != 0:
        binary += "0"

    # Convert every 2 bits into a DNA base
    dna = "".join(
        DNA_MAP[binary[i:i + 2]]
        for i in range(0, len(binary), 2)
    )

    return binary, dna


def decode_dna(dna):
    # Convert DNA bases back to binary
    binary = "".join(REVERSE_MAP[base] for base in dna)

    # Convert binary bytes back to text
    byte_values = [
        int(binary[i:i + 8], 2)
        for i in range(0, len(binary), 8)
    ]

    return bytes(byte_values).decode("utf-8")


message = input("Enter a message to store in DNA: ")

binary, dna_sequence = encode_text(message)
recovered_message = decode_dna(dna_sequence)

print("\n--- DNA STORAGE RESULTS ---")
print("Original text:", message)
print("Binary data:", binary)
print("DNA sequence:", dna_sequence)
print("Recovered text:", recovered_message)
print("Recovery successful:", message == recovered_message)
print("DNA bases used:", len(dna_sequence))