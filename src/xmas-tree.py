import time
import os

width = int(input("tree input: "))
sideWidth = int((width - 1) / 2)
print(sideWidth)
light = True
ON = "⬤"
OFF = "◯"

while(True):
    os.system('cls')
    offset = 0
    distance = 2
    for i in range(sideWidth+1):
        space = " " * (sideWidth-i)
        txt = ""
        for j in range((i)*2+1):
            txt += "*" if (j+1-offset)%distance != 0 else ON if light else OFF
        print(f"{space}{txt}")
        if offset:
            offset -= 1 
            distance+=1
        else:
            offset = 2
    print(f"{' ' * (sideWidth-1)}| |\n" * 3)
    print("MERRY CHRISTMAS")
    time.sleep(0.5)
    light = not light