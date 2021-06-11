'''
from time import sleep
import os


def clocktime(hour, min, seg):
  while hour < 24:
    hour += 1

    while min < 60:
      min += 1

      while seg < 60:
        print('| RELÓGIO DIGITAL |\n')
        print('{}:{}:{} h'.format(hour, min, seg))
        seg += 1
        sleep(1)
        os.system('cls')

      seg = 0

    min = 0

  hour = 0


hour = int(input('HORA: ')) - 1
min = int(input('MIN: ')) - 1
seg = int(input('SEG: '))

clock = True
while clock == True:
  clocktime(hour, min, seg)
'''

'''
from time import sleep
import os

temp = int(input('Set_Time: '))
print('TMER BOMB')

cont = temp
for i in range(0, temp + 1):
  print(cont)
  cont -= 1
  sleep(1)
  os.system('cls')

print('BUM!!!!!\n\n')
'''