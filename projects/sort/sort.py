def my_key(student_data):
    name = student_data[0]
    math = student_data[1]
    english = student_data[2]
    avg = (math + english) / 2
    return avg, min(math, english), math

x = []
x.append(("Alice", 90, 95))
x.append(("Bob", 80, 75))
x.append(("Charlie", 0, 100))
x.append(("Dave", 75, 80))
x.append(("Ellen", 77, 78))

x.sort(key=my_key, reverse = True)
print(x)