# test.py — EmulAI Minimal N64 Emulator Core (WIP v0.1)

import tkinter as tk
from tkinter import filedialog
import os

def load_rom(path):
    with open(path, 'rb') as f:
        data = f.read()
    if data[:4] == b'\x80\x37\x12\x40':
        rom_type = 'Z64 (Big Endian)'
    elif data[:4] == b'\x37\x80\x40\x12':
        rom_type = 'V64 (Byte Swapped)'
    elif data[:4] == b'\x40\x12\x37\x80':
        rom_type = 'N64 (Little Endian)'
    else:
        rom_type = 'Unknown Format'
    return data, rom_type

def disassemble_word(word):
    opcode = (word >> 26) & 0x3F
    if opcode == 0x00:
        return "NOP"
    elif opcode == 0x08:
        return "ADDI"
    elif opcode == 0x23:
        return "LW"
    elif opcode == 0x2B:
        return "SW"
    else:
        return f"UNKNOWN OPCODE 0x{opcode:X}"

def run_dummy_loop(rom_data, output_box):
    pc = 0x1000
    output_box.set("🧠 EmulAI Interpreter Started\n")
    while pc < 0x1100 and pc + 4 <= len(rom_data):
        word = int.from_bytes(rom_data[pc:pc+4], 'big')
        instr = disassemble_word(word)
        output_box.set(output_box.get() + f"0x{pc:08X}: {instr}\n")
        pc += 4

def open_and_run_rom():
    rom_path = filedialog.askopenfilename(
        title="Select N64 ROM",
        filetypes=[("N64 ROMs", "*.z64 *.n64 *.v64")]
    )
    if rom_path:
        rom_data, rom_type = load_rom(rom_path)
        rom_name = os.path.basename(rom_path)
        output_text.set(
            f"💾 EmulAI ROM Loaded: {rom_name} ({rom_type})\n"
            "🔍 Beginning Disassembly...\n"
        )
        run_dummy_loop(rom_data, output_text)
    else:
        output_text.set("No ROM selected.")

root = tk.Tk()
root.title("EmulAI Core - test.py")
root.geometry("600x400")
root.configure(bg="#1c1c1c")

title = tk.Label(
    root, text="🧠 EMULAI TEST CORE 🧠",
    font=("Courier", 14), fg="#ff4444", bg="#1c1c1c"
)
title.pack(pady=10)

output_text = tk.StringVar()
output_text.set("Awaiting ROM...\n")

output_label = tk.Label(
    root, textvariable=output_text,
    font=("Courier", 10), fg="#00ff88",
    bg="#000000", width=70, height=15,
    justify="left", anchor="nw", relief="sunken", bd=3
)
output_label.pack(pady=10)

launch_button = tk.Button(
    root, text="🎮 Load & Run ROM",
    font=("Courier", 12), command=open_and_run_rom,
    bg="#333", fg="#ffffff", width=25
)
launch_button.pack(pady=10)

root.mainloop()
