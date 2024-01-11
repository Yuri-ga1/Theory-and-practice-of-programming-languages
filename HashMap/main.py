import re

class SpecialHashMap(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def iloc(self):
        keys_sorted = sorted(self.keys())
        return HashMapIloc(self, keys_sorted)

    @property
    def ploc(self):
        return HashMapPloc(self)


class HashMapIloc:
    def __init__(self, special_hash_map, sorted_keys):
        self.special_hash_map = special_hash_map
        self.sorted_keys = sorted_keys

    def __getitem__(self, index):
        try:
            key = self.sorted_keys[index]
            return self.special_hash_map[key]
        except IndexError:
            raise IndexError("Index out of range")


class HashMapPloc:
    def __init__(self, special_hash_map):
        self.special_hash_map = special_hash_map

    def _evaluate_condition(self, condition, keys):
        result = {}
        for key in keys:
            values = [part.strip() for part in key.split(",")]
            
            if values[0][0] == '(':
                values[0] = values[0][1:]
                values[-1] = values[-1][:-1]

            condition_parts = re.findall(r'([<>]=?|<>),?\s*([^\s,]+)', condition)
            
            odcl = [item for parts in condition_parts for item in parts] #one-dimensional condition list

            try:
                values = [float(x) for x in values]
            except:
                continue
            
            operators = odcl[::2]
            numbers = odcl[1::2]

            try:
                numbers = [float(x) for x in numbers]
            except:
                raise SyntaxError('Argument must be number')

            if len(values) == len(condition_parts):
                is_conditions_completed = True
                for value, op, cond_value in zip(values, operators, numbers):

                    if op == ">=" and not value >= cond_value:
                        is_conditions_completed = False
                        break
                    elif op == ">" and not value > cond_value:
                        is_conditions_completed = False
                        break
                    elif op == "<=" and not value <= cond_value:
                        is_conditions_completed = False
                        break
                    elif op == "<" and not value < cond_value:
                        is_conditions_completed = False
                        break
                    elif op == "=" and not value == cond_value:
                        is_conditions_completed = False
                        break
                    elif op == "<>" and not value != cond_value:
                        is_conditions_completed = False
                        break

                if is_conditions_completed:
                    result[key] = self.special_hash_map[key]
        return result

    def __getitem__(self, condition):
        keys = self.special_hash_map.keys()
        result = self._evaluate_condition(condition, keys)
        return result


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