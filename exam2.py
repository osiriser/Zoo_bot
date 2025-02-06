with open('INPUT.TXT', 'r') as file:
    w, h = map(int, file.readline().strip().split())
    n = int(file.readline().strip())
    
    canvas = [[0] * w for _ in range(h)]
    
    
    for _ in range(n):
        x1, y1, x2, y2 = map(int, file.readline().strip().split())
        for y in range(y1, y2):
            for x in range(x1, x2):
                canvas[y][x] = 1  

unpainted_area = 0
for row in canvas:
    unpainted_area += row.count(0)  

with open('OUTPUT.TXT', 'w') as file:
    file.write(str(unpainted_area))