# arm64-emulator
(Work in Progress) CLI arm64 emulator using unicorn

## Usage
Edit the assembly code in `test.inst` and run `python main.py` 

Example output:

```bash
>>> Tracing basic block at 0x10000, block size = 0x44
>>> Tracing instruction at 0x10000, instruction size = 0x4
>>> Emulation done.

>>> Registers
X0: 0x124       X1: 0x124       X2: 0x1         X3: 0x1
X4: 0x123456789abcdef   X5: 0x0         X6: 0x0         X7: 0x0
X8: 0x0         X9: 0x0         X10: 0x0        X11: 0x0
X12: 0x0        X13: 0x0        X14: 0x0        X15: 0x15
X16: 0x0        X17: 0x0        X18: 0x0        X19: 0x0
X20: 0x0        X21: 0x0        X22: 0x0        X23: 0x0
X24: 0x0        X25: 0x0        X26: 0x0        X27: 0x0
X28: 0x0        V0: 0x0         SP: 0x210000    PC: 0x10044

>>> Stack 0x210000
00000000: EF CD AB 89 67 45 23 01  EF CD AB 89 67 45 23 01  ....gE#.....gE#.
00000010: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000020: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000030: EF CD AB 89 67 45 23 01  EF CD AB 89 67 45 23 01  ....gE#.....gE#.
00000040: EF CD AB 89 67 45 23 01  EF CD AB 89 67 45 23 01  ....gE#.....gE#.
00000050: EF CD AB 89 67 45 23 01  EF CD AB 89 67 45 23 01  ....gE#.....gE#.
00000060: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000070: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
```
