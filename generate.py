import random
import huffman as dm
import time

def generate(n):
    """
    generate a string of n random ASSCI chars
    """
    str = ""
    for i in range(n):
        str += chr(int(random.triangular(0,256)))
        #str += chr(int(random.randint(0,255)))
    return str

print("generating ...")
str = generate(1000000)
print("finished generating.")
print("GO")


t = time.time()
data,tree = dm.compress(str)
tc = time.time() - t
decompressed = dm.decompress(data[0],data[1],tree[0],tree[1])
t = time.time()-t
print("compression time = ",tc)
print("decompression time = ",t - tc)
print("total time = ",t)
