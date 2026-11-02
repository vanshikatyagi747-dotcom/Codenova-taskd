import json
import os

class Student:
    def __init__(self, roll_no, name, age, grade):
        self.roll_no = roll_no
        self.name = name
        self.age = age
        self.grade = grade

    def to_dict(self):
        """Converts object data into a dictionary for JSON serialization."""
        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "age": self.age,
            "grade": self.grade
        }

class StudentManagementSystem:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = {}
        self.load_data()

    def load_data(self):
        """Loads student data from a JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    # Convert dict back into Student objects
                    for roll_no, info in data.items():
                        self.students[roll_no] = Student(
                            info['roll_no'], info['name'], info['age'], info['grade']
                        )
            except json.JSONDecodeError:
                print("Error reading data file. Starting with an empty database.")

    def save_data(self):
        """Saves current student data to the JSON file."""
        with open(self.filename, 'w') as file:
            # Convert Student objects to dictionaries
            serialized_data = {roll_no: stud.to_dict() for roll_no, stud in self.students.items()}
            json.dump(serialized_data, file, indent=4)

    def add_student(self, roll_no, name, age, grade):
        """Adds a new student if the roll number is unique."""
        if roll_no in self.students:
            print(f"\n❌ Error: Student with Roll Number {roll_no} already exists!")
            return False
        
        self.students[roll_no] = Student(roll_no, name, age, grade)
        self.save_data()
        print(f"\n✅ Student '{name}' added successfully!")
        return True

    def view_all_students(self):
        """Displays all student records."""
        if not self.students:
            print("\n📂 No records found.")
            return

        print("\n" + "="*50)
        print(f"{'Roll No':<10} | {'Name':<20} | {'Age':<5} | {'Grade':<5}")
        print("="*50)
        for stud in self.students.values():
            print(f"{stud.roll_no:<10} | {stud.name:<20} | {stud.age:<5} | {stud.grade:<5}")
        print("="*50)

    def search_student(self, roll_no):
        """Searches for a specific student by roll number."""
        stud = self.students.get(roll_no)
        if stud:
            print("\n🔍 Student Found:")
            print(f"📌 Roll Number: {stud.roll_no}")
            print(f"👤 Name:        {stud.name}")
            print(f"🎂 Age:         {stud.age}")
            print(f"📊 Grade:       {stud.grade}")
        else:
            print(f"\n❌ Student with Roll Number {roll_no} not found.")

    def update_student(self, roll_no):
        """Updates an existing student's details."""
        stud = self.students.get(roll_no)
        if not stud:
            print(f"\n❌ Student with Roll Number {roll_no} not found.")
            return

        print(f"\n📝 Updating details for {stud.name} (Press Enter to keep current value)")
        
        new_name = input(f"Enter New Name [{stud.name}]: ").strip()
        if new_name:
            stud.name = new_name

        new_age = input(f"Enter New Age [{stud.age}]: ").strip()
        if new_age:
            try:
                stud.age = int(new_age)
            except ValueError:
                print("Invalid age input. Keeping original value.")

        new_grade = input(f"Enter New Grade [{stud.grade}]: ").strip()
        if new_grade:
            stud.grade = new_grade

        self.save_data()
        print("\n✅ Student record updated successfully!")

    def delete_student(self, roll_no):
        """Removes a student record from the system."""
        if roll_no in self.students:
            del self.students[roll_no]
            self.save_data()
            print(f"\n🗑️ Student with Roll Number {roll_no} deleted successfully.")
        else:
            print(f"\n❌ Student with Roll Number {roll_no} not found.")

def main():
    sms = StudentManagementSystem()

    while True:
        print("\n--- Student Record Management System ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            roll_no = input("Enter Roll Number: ").strip()
            name = input("Enter Name: ").strip()
            try:
                age = int(input("Enter Age: ").strip())
            except ValueError:
                print("❌ Invalid input for Age. Must be an integer.")
                continue
            grade = input("Enter Grade/Class: ").strip()
            
            if roll_no and name and grade:
                sms.add_student(roll_no, name, age, grade)
            else:
                print("❌ All fields are required.")

        elif choice == '2':
            sms.view_all_students()

        elif choice == '3':
            roll_no = input("Enter Roll Number to Search: ").strip()
            sms.search_student(roll_no)

        elif choice == '4':
            roll_no = input("Enter Roll Number to Update: ").strip()
            sms.update_student(roll_no)

        elif choice == '5':
            roll_no = input("Enter Roll Number to Delete: ").strip()
            sms.delete_student(roll_no)

        elif choice == '6':
            print("\nExiting System. Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please select between 1 and 6.")

if __name__ == "__main__":
    main()
