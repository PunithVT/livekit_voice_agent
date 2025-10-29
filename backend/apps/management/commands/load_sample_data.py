from django.core.management.base import BaseCommand
from apps.models import Module, Lesson

class Command(BaseCommand):
    help = 'Load sample data for modules and lessons'

    def handle(self, *args, **options):
        # Clear existing data
        Module.objects.all().delete()
        
        self.stdout.write("Creating sample modules and lessons...")
        
        # Module 1: Python Basics
        module1 = Module.objects.create(
            title="Python Basics",
            description="Learn the fundamentals of Python programming",
            icon_name="python",
            duration="2 hours",
            order=1,
            is_active=True
        )
        
        Lesson.objects.create(
            module=module1,
            title="Introduction to Python",
            content="Get started with Python programming language",
            code_snippet="print('Hello, World!')",
            explanation="This is a simple Python program that prints 'Hello, World!' to the console.",
            order=1,
            is_exercise=False
        )

        # Module 2: Control Flow
        module2 = Module.objects.create(
            title="Control Flow",
            description="Master if statements, loops, and control structures",
            icon_name="flow",
            duration="2.5 hours",
            order=2,
            is_active=True
        )
        
        Lesson.objects.create(
            module=module2,
            title="If-Else Statements",
            content="Learn how to make decisions in your code",
            code_snippet="""age = 18
if age >= 18:
    print("Adult")
else:
    print("Minor")""",
            explanation="Using if-else statements to control program flow",
            order=1,
            is_exercise=False
        )

        # Module 3: Data Structures
        module3 = Module.objects.create(
            title="Data Structures",
            description="Learn about lists, dictionaries, and more",
            icon_name="data",
            duration="3 hours",
            order=3,
            is_active=True
        )
        
        Lesson.objects.create(
            module=module3,
            title="Lists and Dictionaries",
            content="Working with Python's built-in data structures",
            code_snippet="""fruits = ['apple', 'banana', 'cherry']
person = {'name': 'John', 'age': 30}""",
            explanation="Lists are ordered collections, dictionaries store key-value pairs",
            order=1,
            is_exercise=False
        )

        # Module 4: Functions
        module4 = Module.objects.create(
            title="Functions",
            description="Learn to create and use functions",
            icon_name="function",
            duration="2 hours",
            order=4,
            is_active=True
        )
        
        Lesson.objects.create(
            module=module4,
            title="Defining Functions",
            content="Create reusable code with functions",
            code_snippet="""def greet(name):
    return f'Hello, {name}!'
    
print(greet('Alice'))""",
            explanation="Functions help organize code into reusable blocks",
            order=1,
            is_exercise=False
        )

        # Module 5: File Handling
        module5 = Module.objects.create(
            title="File Operations",
            description="Learn to work with files in Python",
            icon_name="file",
            duration="1.5 hours",
            order=5,
            is_active=True
        )
        
        Lesson.objects.create(
            module=module5,
            title="Reading and Writing Files",
            content="Basic file I/O operations in Python",
            code_snippet="""# Writing to a file
with open('example.txt', 'w') as f:
    f.write('Hello, World!')
    
# Reading from a file
with open('example.txt', 'r') as f:
    content = f.read()""",
            explanation="Using context managers for safe file handling",
            order=1,
            is_exercise=False
        )

        self.stdout.write(self.style.SUCCESS('Successfully loaded 5 modules with sample data!'))