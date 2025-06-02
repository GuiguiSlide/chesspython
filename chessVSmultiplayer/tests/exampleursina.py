import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

original[0][0] = 999

print("Original:", original)       # [[999, 2], [3, 4]]
print("Shallow Copy:", shallow)   # [[999, 2], [3, 4]] → still affected
print("Deep Copy:", deep)    