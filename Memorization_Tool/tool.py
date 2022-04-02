# "Memorization Tool" project from the "Flask Developer" track
# Learned about SQLAlchemy and how to use (some parts of) it. Probably not using it optimally or efficiently yet.
# The functions should be pretty self-explanatory

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random


Base = declarative_base()

engine = create_engine("sqlite:///flashcard.db?check_same_thread=False")

Session = sessionmaker(bind=engine)


class Flashcards(Base):
    """The class used for ORM (Object-Relational Mapping) here, representing a flashcard in the database.
    A flashcard has an id, a question, an answer and the number of a box it is in. A flashcard starts in box 1, and when
    answered correctly it is moved to the next box, if answered wrong it goes back to the previous box. If a flashcard
    in box 3 is answered correctly, it is considered as "known" and deleted from the database."""

    __tablename__ = "flashcard"

    card_id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer)


Base.metadata.create_all(engine)


def main_loop(menu: str):
    while True:
        match menu:
            case "main_menu":
                menu = main_menu_loop()
            case "add":
                menu = add_card_menu_loop()
            case "practice":
                menu = practice()
            case "exit":
                print("Bye!")
                exit()


def main_menu_loop() -> str:
    menu_text = "\n".join([
        "1. Add flashcards",
        "2. Practice flashcards",
        "3. Exit"
    ])
    while True:
        user_input = get_user_input(menu_text)
        if user_input not in ["1", "2", "3"]:
            print_key_error(user_input)
        elif user_input == "1":
            return "add"
        elif user_input == "2":
            return "practice"
        else:
            return "exit"


def add_card_menu_loop() -> str:
    menu_text = "\n".join([
        "1. Add a new flashcard",
        "2. Exit"
    ])
    while True:
        user_input = get_user_input(menu_text)
        if user_input not in ["1", "2"]:
            print_key_error(user_input)
        elif user_input == "1":
            add_card()
            return "add"
        elif user_input == "2":
            return "main_menu"


def add_card() -> None:
    while True:
        question = get_user_input("Question:")
        if question.strip():
            break
    while True:
        answer = get_user_input("Answer:")
        if answer.strip():
            break
    flashcard = Flashcards(question=question, answer=answer, box=1)
    with Session.begin() as session:
        session.add(flashcard)


def practice() -> str:
    menu_text = "\n".join([
        "press \"y\" to see the answer:",
        "press \"n\" to skip:",
        "press \"u\" to update:"
    ])
    with Session.begin() as session:
        flashcards = session.query(Flashcards).all()
        if not flashcards:
            print("There is no flashcard to practice!\n")
            return "main_menu"

        for flashcard in flashcards:
            print(f"Question: {flashcard.question}:")
            while True:
                user_input = get_user_input(menu_text)
                if user_input not in ["y", "n", "u"]:
                    print_key_error(user_input)
                    continue
                elif user_input == "y":
                    learn(flashcard, session)
                elif user_input == "n":
                    pass  # these two line are unnecessary, just for completeness' sake
                elif user_input == "u":
                    update_flashcard(flashcard, session)
                break
    return "main_menu"


def update_flashcard(flashcard, session) -> None:
    menu_text = "\n".join([
        "press \"d\" to delete the flashcard:",
        "press \"e\" to edit the flashcard:"
    ])
    while True:
        user_input = get_user_input(menu_text)
        if user_input not in ["d", "e"]:
            print_key_error(user_input)
            continue

        # delete flashcard
        elif user_input == "d":
            session.delete(flashcard)

        # edit the flashcard and update it in the database
        elif user_input == "e":
            new_question = get_user_input(f"current question: {flashcard.question}\nplease write a new question:")
            new_answer = get_user_input(f"current answer: {flashcard.answer}\nplease write a new answer:")
            if new_question:
                flashcard.question = new_question
            if new_answer:
                flashcard.answer = new_answer
        break


def learn(flashcard, session) -> None:
    menu_text = "\n".join([
        "press \"y\" if your answer is correct:",
        "press \"n\" if your answer is wrong:"
    ])
    query = session.query(Flashcards.answer)
    random_answer = random.choice(list(query))[0]

    print(f"Answer: {random_answer}")

    while True:
        user_input = get_user_input(menu_text)
        if user_input not in ["y", "n"]:
            print_key_error(user_input)
            continue

        # logic to move a flashcard to a different box and update it in database
        elif user_input == "y":
            if flashcard.answer == random_answer:
                if flashcard.box == 3:
                    session.delete(flashcard)
                else:
                    flashcard.box += 1
            else:
                flashcard.box = max(1, flashcard.box - 1)
        elif user_input == "n":
            if flashcard.answer != random_answer:
                if flashcard.box == 3:
                    session.delete(flashcard)
                else:
                    flashcard.box += 1
            else:
                flashcard.box = max(1, flashcard.box - 1)
        break


def get_user_input(msg: str) -> str:
    """Get the user input after printing the passed message with project specific formatting."""

    user_input = input(msg + "\n")
    print()
    return user_input


def print_key_error(key: str) -> None:
    print(f"{key} is not an option" + "\n")


def main():
    main_loop("main_menu")


if __name__ == "__main__":
    main()
