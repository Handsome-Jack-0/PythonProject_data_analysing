import matplotlib.pyplot as plt
import numpy as np

def get_valid_integer_input(prompt):
    """
    Get a valid integer input from the user.
    If the input is invalid, prompt the user to re-enter until a valid integer is provided.

    :param prompt: The message to prompt the user for input
    :return: A valid integer
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_valid_float_input(prompt):
    """
    Get a valid floating-point number input from the user.
    If the input is invalid, prompt the user to re-enter until a valid number is provided.

    :param prompt: The message to prompt the user for input
    :return: A valid floating-point number
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_student_scores():
    """
    Get the names and scores of students, and validate the scores (between 0 and 100).

    :return: A list of student names and a corresponding list of scores
    """
    num_students = get_valid_integer_input("Please enter the number of students: ")
    students = []
    scores = []
    for i in range(num_students):
        name = input(f"Please enter the name of student {i + 1}: ")
        while True:
            score = get_valid_float_input(f"Please enter {name}'s score (0 - 100): ")
            if 0 <= score <= 100:
                students.append(name)
                scores.append(score)
                break
            else:
                print("The score must be between 0 and 100. Please re-enter.")
    return students, scores

def display_scores(students, scores):
    """
    Display the list of student names and their corresponding scores.

    :param students: A list of student names
    :param scores: A list of student scores
    """
    print("Student Score List:")
    for student, score in zip(students, scores):
        print(f"{student}: {score}")

def calculate_average(scores):
    """
    Calculate the average score of the students.

    :param scores: A list of student scores
    :return: The average score
    """
    return np.mean(scores)

def plot_scores(students, scores, save_path=None):
    """
    Plot a bar chart of student scores and optionally save the chart as an image.

    :param students: A list of student names
    :param scores: A list of student scores
    :param save_path: The path to save the image. If None, the image will not be saved.
    """
    try:
        plt.figure(figsize=(10, 6))
        bars = plt.bar(students, scores, color='skyblue', edgecolor='black')
        plt.title("Student Score Bar Chart", fontsize=16)
        plt.xlabel("Student Names", fontsize=12)  # Added x-axis label
        plt.ylabel("Scores", fontsize=12)  # Added y-axis label
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 1, str(height), ha='center', va='bottom', fontsize=10)

        if save_path:
            plt.savefig(save_path)
            print(f"The bar chart has been saved as {save_path}")

        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting the bar chart: {e}")

def main():
    """
    The main function, the entry point of the program, responsible for calling other functions to complete student score analysis and visualization.
    """
    students, scores = get_student_scores()
    if students and scores:
        display_scores(students, scores)
        average_score = calculate_average(scores)
        print(f"\nAverage Score of Students: {average_score:.2f}")
        save_path = input("Please enter the file name to save the bar chart (leave blank to not save): ")
        if save_path:
            plot_scores(students, scores, save_path)
        else:
            plot_scores(students, scores)
    else:
        print("No valid score data was obtained. The program ends.")

if __name__ == "__main__":
    main()