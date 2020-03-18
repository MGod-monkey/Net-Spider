s = input().split(" ")
number = 0
end_pos = [int(s[0]), int(s[1])]
m_pos = [int(s[2]), int(s[3])]
start_pos = [0, 0]
stop_pos = [
    [m_pos[0]+1,m_pos[1]+2],
   [m_pos[0]+2,m_pos[1]+1],
   [m_pos[0]+1,m_pos[1]-2],
    [m_pos[0]-1,m_pos[1]+2],
   [m_pos[0]-1,m_pos[1]-2],
   [m_pos[0]-1,m_pos[1]+2],
   [m_pos[0]+2,m_pos[1]-1],
   [m_pos[0]-2,m_pos[1]+1],
    [m_pos[0]-2,m_pos[1]-1],
    m_pos
]
for x in range(1,end_pos[0]+1):
    for y in range(1,end_pos[1]+1):
        start_pos[0] += 1
        if start_pos in stop_pos:
           start_pos = [0, 0]
        if start_pos == end_pos:
            start_pos = [0, 0]
            number += 1
    start_pos[1] += 1
    if start_pos in stop_pos:
        start_pos = [0, 0]
        # print(start_pos, end="\t")
    if start_pos == end_pos:
       start_pos = [0, 0]
       number += 1
print(number)