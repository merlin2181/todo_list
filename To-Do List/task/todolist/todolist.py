# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

# link the database _todo_ using the create_engine()
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    # class to make a table 'task' in the database _todo_
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"<(id={self.id}, task={self.task}, deadline={self.deadline})>"


# create the Table 'task' in the database _todo_ and link the database to the sessionmaker()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def menu():
    # function to display a menu to the user and returns user's selection
    print("""1) Today's tasks
2) Add task
0) Exit""")
    return input()


def today_task():
    # function to get items from the to-do list and print them to the screen.
    print('\nToday:')
    tasks = session.query(Table).all()
    if tasks:
        n = 1
        for instance in tasks:
            print(f"{n}. {instance.task}")
            n += 1
        print('\r')
    else:
        print('Nothing to do!\n')


def add_task():
    # function to add items to a user's to-do list
    task_string = input('\nEnter task\n')
    new_task = Table(task=task_string)
    session.add(new_task)
    session.commit()
    print('The task has been added!\n')


# while loop that cycles through the user menu until the user wishes to exit the program
while True:
    choice = menu()
    if choice == '1':
        today_task()
        continue
    elif choice == '2':
        add_task()
        continue
    elif choice == '0':
        print('Bye!')
        exit()
    else:
        continue
