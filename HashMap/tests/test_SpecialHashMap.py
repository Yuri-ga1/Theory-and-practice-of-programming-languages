import pytest
from hashMap import SpecialHashMap

@pytest.fixture()
def hashMapIloc():
    map = SpecialHashMap()
    map["value1"] = 1
    map["value2"] = 2
    map["value3"] = 3
    map["1"] = 10
    map["2"] = 20
    map["3"] = 30
    map["1, 5"] = 100
    map["5, 5"] = 200
    map["10, 5"] = 300
    return map

@pytest.fixture()
def hashMapPloc():
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
    map["(1, 5, 3)"] = 400
    map["(5, 5, 4)"] = 500
    map["(10, 5, 5)"] = 600
    return map

class Test_SpecialHashMap:

    def test_iloc(self, hashMapIloc):
        assert hashMapIloc.iloc[0] == 10
        assert hashMapIloc.iloc[2] == 300
        assert hashMapIloc.iloc[5] == 200
        assert hashMapIloc.iloc[8] == 3

    def test_iloc_exception(self, hashMapIloc):
        with pytest.raises(IndexError):
            hashMapIloc.iloc[10]

    def test_ploc_bad_condition(self, hashMapPloc):
        with pytest.raises(SyntaxError):
            hashMapPloc.ploc["<5, =>b, =1"]


    def test_ploc(self, hashMapPloc):
        assert hashMapPloc.ploc[">=1"] == {'1': 10, '2': 20, '3': 30}
        assert hashMapPloc.ploc["<>2"] == {'1': 10, '3': 30}
        assert hashMapPloc.ploc["<3"] == {'1': 10, '2': 20}

        assert hashMapPloc.ploc[">0, >0"] == {'(1, 5)': 100, '(5, 5)': 200, '(10, 5)': 300}
        assert hashMapPloc.ploc[">=10, >0"] == {'(10, 5)': 300}
        assert hashMapPloc.ploc["<5, >=5, >=3"] == {'(1, 5, 3)': 400}

        assert hashMapPloc.ploc["==5, <=6, >3"] == {'(5, 5, 4)': 500}