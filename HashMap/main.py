from hashMap import SpecialHashMap

map = SpecialHashMap()
map["value1"] = 1
map["value2"] = 2
map["value3"] = 3
map["1"] = 10
map["2"] = 20
map["3"] = 30
map["(1, 5)"] = 100
map["(5, 5)"] = 200
map["(10, 5)"] = 300

print(map.iloc[0])  # >>> 100
print(map.iloc[2])  # >>> 200
print(map.iloc[5])  # >>> 30
print(map.iloc[8])  # >>> 3

map["(1, 5, 3)"] = 400
map["(5, 5, 4)"] = 500
map["(10, 5, 5)"] = 600

print(map.ploc[">=1"])  # >>> {'1': 10, '2': 20, '3': 30}
print(map.ploc["<3"])   # >>> {'1': 10, '2': 20}

print(map.ploc[">0, >0"])          # >>> {'1, 5': 100, '5, 5': 200, '10, 5': 300}
print(map.ploc[">=10, >0"])        # >>> {'10, 5': 300}

print(map.ploc["<5, >=5, >=3"])    # >>> {'1, 5, 3'=400}