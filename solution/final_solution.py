
from math import sqrt, atan2


"""
Concept:
    - Imagine the bottom line and the left wall line of the room are the x and y axes
    - And all the points are just mirrored points in a mirrored room
    - So we just need to find the first area of the points 
    - The rest is just to reverse the x and y direction
    
Approach:
    1. Find all points(me and targets) on the first area(including original room and mirrored room)
    2. Find the rest of the 3 areas by reversing the x, y
    3. Filter out the points that are too far    
    4. Calculate the direction and give the ID tags(me, target, or corners)
    5. Sort the list by distance
    6. Filter out the points you can't hit(points that are blocked by points with shorter distance)
    7. Calculate the many points with "target" tag
"""
area1_mes = []
area1_targets = []


def solution(room, me, target, distance):

    # No need to calculate further if the weapon is too weak
    if cal_dist(target, me) > distance:
        return 0
    # Mirror distances

    # Include the rooms that's just out reach the shooting radius
    right_maximum = (me[0] + distance) // room[0] + 1
    up_maximum = (me[1] + distance) // room[1] + 1

    # Find the points that are in the first area
    cal_area1(right_maximum, up_maximum, me, target, room)

    # Get the rest point in other areas
    area2_mes = [[-x, y] for [x, y] in area1_mes]
    area2_targets = [[-x, y] for [x, y] in area1_targets]

    area3_mes = [[-x, -y] for [x, y] in area1_mes]
    area3_targets = [[-x, -y] for [x, y] in area1_targets]

    area4_mes = [[x, -y] for [x, y] in area1_mes]
    area4_targets = [[x, -y] for [x, y] in area1_targets]

    # Divide them into 3 groups
    M = area1_mes + area2_mes + area3_mes + area4_mes
    M.remove(me)  # It's pointless to include original me point
    T = area1_targets + area2_targets + area3_targets + area4_targets
    # 4 Corners
    C = [
        [0, 0],
        [0, room[1]],
        [room[0], 0],
        [room[0], room[1]]
    ]

    MEs = [[cal_direct(p, me), cal_dist(p, me), "m"] for p in M]
    TARGETs = [[cal_direct(p, me), cal_dist(p, me), "t"] for p in T]
    CORNERs = [[cal_direct(p, me), cal_dist(p, me), "c"] for p in C]
    # Filter out the point too far
    all_points = list(filter(lambda p: p[1] <= float(distance), MEs + TARGETs + CORNERs))
    all_points.sort(key=lambda p: p[1])

    # # Detailed version for test
    # MEs = [[cal_direct(p, me), [p[0] - me[0], p[1] - me[1]], p, cal_dist(p, me), "m"] for p in M]
    # TARGETs = [[cal_direct(p, me), [p[0] - me[0], p[1] - me[1]], p, cal_dist(p, me), "t"] for p in T]
    # CORNERs = [[cal_direct(p, me), [p[0] - me[0], p[1] - me[1]], p, cal_dist(p, me), "c"] for p in C]
    # all_points = list(filter(lambda p: p[3] <= float(distance), TARGETs + MEs + CORNERs))
    # all_points.sort(key=lambda p: p[3])

    # Goal:
    #   1. Select the unique and the shortest distance points
    #   2. Select the ones with "t" tags
    selected_points = {}
    for p in all_points:
        if p[0] not in selected_points:
            selected_points[p[0]] = p[2]

    return sum(1 for v in selected_points.values() if v == "t")


def cal_area1(r_max, u_max, me, target, room):

    for i in range(0, r_max + 1):
        for j in range(0, u_max + 1):
            mirrored_me = [me[0] + i * room[0], me[1] + j * room[1]]
            mirrored_target = [target[0] + i * room[0], target[1] + j * room[1]]

            # Odd room positions are mirrored positions, below are the method to correct the values of the coordinates
            if i % 2 != 0:
                mirrored_me[0] = mirrored_me[0] - 2 * me[0] + room[0]
                mirrored_target[0] = mirrored_target[0] - 2 * target[0] + room[0]
            if j % 2 != 0:
                mirrored_me[1] = mirrored_me[1] - 2 * me[1] + room[1]
                mirrored_target[1] = mirrored_target[1] - 2 * target[1] + room[1]

            area1_mes.append(mirrored_me)
            area1_targets.append(mirrored_target)


def cal_dist(t, m):
    return sqrt((t[1] - m[1]) ** 2 + (t[0] - m[0]) ** 2)


def cal_direct(t, m):
    return atan2((t[1] - m[1]), (t[0] - m[0]))


# print(solution([3, 2], [1, 1], [2, 1], 4))  # ans: 7
# print(solution([2, 5], [1, 2], [1, 4], 11))  # ans:27
# print(solution([23, 10], [6, 4], [3, 2], 23)) # ans:8
# print(solution([1250, 1250], [1000, 1000], [500, 400], 10000)) # ans: 196
# print(solution([10, 10], [4, 4], [3, 3], 5000)) # ans:739323
# print(solution([3, 2], [1, 1], [2, 1], 7)) # ans:19
# print(solution([2, 3], [1, 1], [1, 2], 4)) # ans:7
# print(solution([3, 4], [1, 2], [2, 1], 7)) # ans: 10
# print(solution([4, 4], [2, 2], [3, 1], 6)) # ans: 7
# print(solution([300, 275], [150, 150], [180, 100], 500)) # ans: 9
print(solution([3, 4], [1, 1], [2, 2], 500)) # ans: 54243

# def test():
#     assert solution([3, 2], [1, 1], [2, 1], 4) == 7
#     # assert solution([2, 5], [1, 2], [1, 4], 11) == 27
#     # assert solution([23, 10], [6, 4], [3, 2], 23) == 8
#     # assert solution([1250, 1250], [1000, 1000], [500, 400], 10000) == 196
#     # assert solution([10, 10], [4, 4], [3, 3], 5000) == 739323
#     # assert solution([3, 2], [1, 1], [2, 1], 7) == 19
#     # assert solution([2, 3], [1, 1], [1, 2], 4) == 7
#     # assert solution([3, 4], [1, 2], [2, 1], 7) == 10
#     # assert solution([4, 4], [2, 2], [3, 1], 6) == 7
#     # assert solution([300, 275], [150, 150], [180, 100], 500) == 9
#     # assert solution([3, 4], [1, 1], [2, 2], 500) == 54243
#
# test()