import time
def ham1(n):
  count = 0
  for i in range (1 , n+1):
    count+=i
    yield count
def main():
  n = 500000
  for i in ham1(n):
    print(i)
start = time.time()
main()
stop = time.time()
times = stop - start
print(times)