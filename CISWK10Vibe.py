"""Student Grade Calculator.

Student records are stored in a list of Student objects and saved in the
required pipe-delimited format.
"""

from dataclasses import dataclass
from pathlib import Path


DATA_FILE = Path("student_grades.txt")


@dataclass
class Student:
	"""A student and the calculated results for three tests."""

	name: str
	student_id: str
	test1: float
	test2: float
	test3: float

	@property
	def average(self):
		return (self.test1 + self.test2 + self.test3) / 3

	@property
	def grade(self):
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	def to_file_line(self):
		return (
			f"{self.name}|{self.student_id}|{self.test1:.2f}|{self.test2:.2f}|"
			f"{self.test3:.2f}|{self.average:.2f}|{self.grade}"
		)

	@classmethod
	def from_file_line(cls, line):
		fields = line.rstrip("\n").split("|")
		if len(fields) != 7:
			raise ValueError("expected 7 pipe-delimited fields")
		return cls(fields[0], fields[1], float(fields[2]), float(fields[3]), float(fields[4]))


def load_students(file_path=DATA_FILE):
	"""Load valid student records, reporting file or record errors clearly."""
	students = []
	try:
		with file_path.open("r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				if not line.strip():
					continue
				try:
					students.append(Student.from_file_line(line))
				except (ValueError, IndexError) as error:
					print(f"Skipping invalid record on line {line_number}: {error}")
	except FileNotFoundError:
		return students
	except OSError as error:
		print(f"Unable to load student records: {error}")
	return students


def save_students(students, file_path=DATA_FILE):
	"""Save all student records and report file errors to the user."""
	try:
		with file_path.open("w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line() + "\n")
		print(f"Saved {len(students)} student record(s) to {file_path}.")
	except OSError as error:
		print(f"Unable to save student records: {error}")


def get_score(test_number):
	while True:
		value = input(f"Test {test_number} score (0-100): ").strip()
		try:
			score = float(value)
			if 0 <= score <= 100:
				return score
			print("Score must be between 0 and 100.")
		except ValueError:
			print("Please enter a numeric score.")


def add_student(students):
	print("\nAdd Student")
	name = input("Student name: ").strip()
	student_id = input("Student ID: ").strip()
	if not name or not student_id:
		print("Name and student ID cannot be blank.")
		return
	scores = [get_score(number) for number in range(1, 4)]
	student = Student(name, student_id, *scores)
	students.append(student)
	print(f"Added {student.name}. Average: {student.average:.2f}, Grade: {student.grade}")


def display_students(students):
	if not students:
		print("\nNo student records found.")
		return
	print("\nStudent Records")
	print(f"{'Name':<20} {'ID':<12} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>9} {'Grade':>5}")
	print("-" * 76)
	for student in students:
		print(
			f"{student.name:<20.20} {student.student_id:<12.12} "
			f"{student.test1:>8.2f} {student.test2:>8.2f} {student.test3:>8.2f} "
			f"{student.average:>9.2f} {student.grade:>5}"
		)


def display_statistics(students):
	if not students:
		print("\nNo student records available for statistics.")
		return
	averages = [student.average for student in students]
	print("\nClass Statistics")
	print(f"Highest average: {max(averages):.2f}")
	print(f"Lowest average:  {min(averages):.2f}")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_student(students):
	search_name = input("\nEnter a student name to search: ").strip().casefold()
	matches = [student for student in students if search_name in student.name.casefold()]
	if not matches:
		print("No matching student found.")
		return
	display_students(matches)


def show_menu():
	print("\nStudent Grade Calculator")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search by name")
	print("5. Save and exit")
	print("Press ESC to save and exit")


def save_and_exit(students):
	save_students(students)
	print("Thank you for using Student Grade Calculator!")


def main():
	students = load_students()
	if students:
		print(f"Loaded {len(students)} student record(s).")

	while True:
		show_menu()
		try:
			choice = input("Select an option: ")
		except (EOFError, KeyboardInterrupt):
			print("\nInput closed. Saving and exiting...")
			save_and_exit(students)
			return
		if choice in ("5", "\x1b"):
			save_and_exit(students)
			return
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		else:
			print("Invalid option. Press 1-5 or ESC to exit.")


if __name__ == "__main__":
	main()