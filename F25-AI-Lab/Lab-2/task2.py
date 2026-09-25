movies = [
    ("Avatar", 237),
    ("Titanic", 200),
    ("Avengers: Endgame", 356),
    ("Joker", 55),
    ("Inception", 160)
]

total_budget = sum(budget for title, budget in movies)
average_budget = total_budget / len(movies)

print("Average Budget:", average_budget)

count = 0

for title, budget in movies:
    if budget > average_budget:
        difference = budget - average_budget
        print(title, "exceeds average by", difference)
        count += 1

print("Movies above average:", count)