import time
import subprocess
import base64
import sys
import os


if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} <file>")
    sys.exit(1)

file_name = sys.argv[1]

if not os.path.isfile(file_name):
    print(f"File not found: {file_name}")
    sys.exit(1)


CHUNK = 700

with open(file_name, "rb") as f:
    data = base64.b64encode(f.read()).decode()

parts = [data[i:i + CHUNK] for i in range(0, len(data), CHUNK)]

print(f"{len(parts)} chunks")

print("Switch NOW to VNC Window...")
for i in range(5, 0, -1):
    print(i)
    time.sleep(1)

print("Starting...")


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


b64_file = file_name + ".b64"

# create file
send(f"> {b64_file}\n")
time.sleep(0.5)

# send chunks
for i, part in enumerate(parts):
    cmd = f"printf '%s' '{part}' >> {b64_file}\n"

    send(cmd)

    print(f"Sent: {i + 1} / {len(parts)}")

    time.sleep(0.4)

# decode in cluster
send(f"\nbase64 -d {b64_file} > {file_name}\n")
time.sleep(0.5)
send(f"rm {b64_file}\n")

print("DONE")
