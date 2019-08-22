import sys
import subprocess
from subprocess import *
import ctypes
from ctypes import *
import binascii
if len (sys.argv) != 3 :
    print("1337C001's Memory Dumper Help")
    print("")
    print("./"+sys.argv[0]+" pid dropletname")
    print("")
else:
    pid = sys.argv[1]
    grep_str = sys.argv[2]
    start_addr_cmd = "tsudo cat /proc/"+pid+"/maps | grep -i '"+grep_str+"""' | awk '{print $1}'| sed -n 1p | cut -d '-' -f 1"""
    start_addr = subprocess.check_output(start_addr_cmd, shell=True).decode('UTF-8').rstrip()
    final_addr_cmd = "tsudo cat /proc/"+pid+"/maps | grep -i '"+grep_str+"""' | awk '{print $1}'| sed '$!d' | cut -d '-' -f 2"""
    final_addr = subprocess.check_output(final_addr_cmd, shell=True).decode('UTF-8').rstrip()
    diff = hex(int(final_addr, 16) - int(start_addr, 16))[2:]
    print("Target PID is " + pid)
    print("Initial Address of "+grep_str+" is " + start_addr)
    print("Final Address of "+grep_str+" is " + final_addr)
    print("Difference is " + diff)
    print("Dumping Starts now........")
    print("")
    print("Wait for process it may take some time........")
    print("")
    final_size = int(diff, 16)
    class iovec(Structure):
        _fields_ = [("iov_base",c_void_p),("iov_len",c_size_t)]

    local = (iovec*2)()             #create local iovec array
    remote =  (iovec*1)()[0]        #create remote iovec
    buf1 = (c_char*final_size)()
    local[0].iov_base = cast(byref(buf1),c_void_p)
    local[0].iov_len = final_size
    remote.iov_base =  ctypes.cast(ctypes.c_char_p(int(start_addr, 16)), ctypes.c_void_p ) 
    remote.iov_len = final_size
    libc = CDLL("libc.so")
    vm = libc.process_vm_readv
    vm.argtypes = [c_int, POINTER(iovec), c_ulong, POINTER(iovec), c_ulong, c_ulong]
    nread = vm(int(pid),local,2,remote,1,0)
    if nread != -1:
        lol = ""
        print("[+] received " + str(nread) + " Bytes")
        finalbin = open (grep_str,'a+b')
        for i in buf1: 
            lol = "{:02x}".format(ord(i))
            binc = binascii.unhexlify(lol)
            finalbin.write(binc)
        finalbin.close()
        print("")
        print("Dumped "+grep_str+" Successfully........")