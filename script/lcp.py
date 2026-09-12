import time
import subprocess
import base64
import sys
import os
from validate_config import validate_config
from load_config import load_config
from check_args import check_args, collect_files

def send(text):
    p = subprocess.Popen(
        ['xclip', '-selection', 'clipboard'],
        stdin=subprocess.PIPE
    )
    p.communicate(input=text.encode())

    subprocess.run([
        'xdotool',
        'key',
        '--clearmodifiers',
        'ctrl+shift+v'
    ])


path_to_config = ("config.yml")

validate_config(path_to_config)

config = load_config(path_to_config)



chunk_size = config["chunk_size"]
paste_delay = config["paste_delay"]



print(chunk_size)


path = check_args()
file_name = check_args()

files = collect_files(path)
for file in files:
    print(file)



# 700 Base64-Zeichen entsprechen 525 Bytes Rohdaten.
# 525 ist durch 3 teilbar -> saubere Base64-Chunks.
RAW_chunk_size = (chunk_size // 4) * 3


file_size = os.path.getsize(file_name)

print(f"File: {file_name}")
print(f"Size: {file_size:,} bytes")
print(f"Chunk: {RAW_chunk_size} bytes -> max. {chunk_size} Base64 chars")


print()
print("Switch NOW to VNC Window...")

for i in range(5, 0, -1):
    print(i)
    time.sleep(1)


print("Starting...")


# Terminal aktivieren
send("\n")
time.sleep(3)


# Remote-Dateinamen
b64_file = os.path.basename(file_name) + ".b64"
remote_file = os.path.basename(file_name)


# Alte Base64-Datei löschen und neue anlegen
send(f"> '{b64_file}'\n")
time.sleep(0.5)


# ------------------------------------------------------------
# Datei Stück für Stück lesen und übertragen
# ------------------------------------------------------------

sent = 0
chunk_number = 0

with open(file_name, "rb") as f:

    while True:

        raw = f.read(RAW_chunk_size)

        if not raw:
            break

        # Nur diesen Chunk Base64-kodieren
        part = base64.b64encode(raw).decode("ascii")

        cmd = f"printf '%s' '{part}' >> '{b64_file}'\n"

        send(cmd)

        sent += len(raw)
        chunk_number += 1

        progress = sent / file_size * 100

        print(
            f"\rChunk {chunk_number} | "
            f"{sent:,} / {file_size:,} bytes "
            f"({progress:6.2f}%)",
            end="",
            flush=True
        )

        time.sleep(0.4)


print()
print()
print("Transfer finished.")


# ------------------------------------------------------------
# Base64 dekodieren
# ------------------------------------------------------------

send(
    f"base64 -d '{b64_file}' > '{remote_file}'\n"
)

time.sleep(0.5)


# ------------------------------------------------------------
# Base64-Zwischendatei löschen
# ------------------------------------------------------------

send(f"rm '{b64_file}'\n")

time.sleep(0.5)


# ------------------------------------------------------------
# Fertig
# ------------------------------------------------------------

send('echo "DONE"\n')

print("DONE")

