# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
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
2) Week's tasks
3) All tasks
4) Add task
0) Exit""")
    return input()


def find_tasks(dates):
    # function to get items from the to-do list, filtered by a date and print them to the screen.
    tasks = session.query(Table).filter(Table.deadline == dates).all()
    if tasks:
        n = 1
        for instance in tasks:
            print(f"{n}. {instance.task}")
            n += 1
        print('\r')
    else:
        print('Nothing to do!\n')


def all_tasks():
    # retrieves all tasks in the _todo_ list
    tasks = session.query(Table).order_by(Table.deadline).all()
    print('\nAll tasks:')
    n = 1
    for item in tasks:
        print(f"{n}. {item.task}. {item.deadline.strftime('%d %b')}")
        n += 1
    print('\r')


def add_task():
    # function to add items to a user's to-do list
    task_string = input('\nEnter task\n')
    task_deadline = input('Enter deadline\n')
    task_deadline = datetime.strptime(task_deadline, '%Y-%m-%d')
    new_task = Table(task=task_string, deadline=task_deadline)
    session.add(new_task)
    session.commit()
    print('The task has been added!\n')


# while loop that cycles through the user menu until the user wishes to exit the program
while True:
    today = datetime.today()
    choice = menu()
    if choice == '1':  # today's tasks
        print(f"\nToday {today.strftime('%d %b')}:")
        find_tasks(today.date())
        continue
    elif choice == '2':  # tasks throughout the week
        print('\r')
        for i in range(7):
            days = today + timedelta(days=i)
            print(f"{days.strftime('%A %d %b')}:")
            find_tasks(days.date())
        continue
    elif choice == '3':  # display all tasks with deadline
        all_tasks()
        continue
    elif choice == '4':  # add a task to your _todo_ list
        add_task()
        continue
    elif choice == '0':  # exit the program
        print('Bye!')
        exit()
    else:
        continue
