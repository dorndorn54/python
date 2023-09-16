list = ["monkey", "donkey", "elephant", "hippo", "cat", "dog", "bird"]

print("the first three items in the list are ", end="")

for i in list[: 3]:
    print(" ", end="")
    print(i, end="")
print("")