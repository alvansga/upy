import gc

gc.collect()
free = gc.mem_free()
alloc = gc.mem_alloc()

print("Free memory :", free, "bytes")
print("Used memory :", alloc, "bytes")
print("Total heap  :", free + alloc, "bytes")
