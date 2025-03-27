import matplotlib.pyplot as plt
import numpy as np

#students' scores data
students = ['jack', 'BOb', "EVe", "David"]
scores = [100, 90, 70, 45]
print("list of the scores")
for student, score  in zip(students, scores):
    print(f"{student}: {score}")

#average scores calculating
average = np.mean(scores)
print(f"\n学生成绩平均值 ：{average : .2f}")

# visualize the data
plt.figure(figsize=(6, 6))

#the bars
plt.bar(students, scores, color="skyblue")
plt.title("grades")
plt.xlabel("name")
plt.ylabel("score")

for i, v  in enumerate(scores):
    plt.text(i, v+1,str(v) ,ha="center")

plt.show()
