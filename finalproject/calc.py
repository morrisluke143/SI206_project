import sqlite3
import matplotlib.pyplot as plt

def calculate_average_goals_per_appearance():
    db_path = r"finalproject\football.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''SELECT last_name, appearances, goals FROM attackers''')
    player_data = cursor.fetchall()
    average_goals_per_appearance = {}
    for player in player_data:
        last_name = player[0]
        appearances = player[1]
        goals = player[2]

        if appearances is not None and appearances > 0:            
            average_goals = goals / appearances
            average_goals_per_appearance[last_name] = (goals, appearances)

    conn.close()
    return average_goals_per_appearance

average_goals_per_appearance = calculate_average_goals_per_appearance()
top_10 = sorted(average_goals_per_appearance.items(), key=lambda x: x[1][0], reverse=True)[:10]

x_values = []
y_values = []
names = []

for name, data in top_10:
    goals, appearances = data
    x_values.append(goals)
    y_values.append(appearances)
    names.append(name)

plt.subplot(1, 2, 1)
plt.scatter(x_values, y_values, color='blue', alpha=0.5)

for i, name in enumerate(names):
    plt.text(x_values[i], y_values[i], f'{name}\navg: {x_values[i]/y_values[i]:.2f}', fontsize=6, ha='center', va='bottom')

plt.title('Top 10 Goal Scorers: Goals vs Appearances for Players')
plt.xlabel('Goals')
plt.ylabel('Appearances')
plt.xticks(range(1, max(x_values) + 1, 2))
plt.yticks(range(1, max(y_values) + 1, 4))
plt.grid(True)

plt.subplot(1, 2, 2)

db_path = r"finalproject\football.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


cursor.execute('''
    SELECT 
        SUM(a.goals) AS total_goals,
        COALESCE(SUM(CASE WHEN p.firstname IS NOT NULL THEN a.goals ELSE 0 END), 0) AS scottish_goals
    FROM attackers a
    LEFT JOIN players p ON a.first_name = p.firstname AND a.last_name = p.lastname
''')

result = cursor.fetchone()

conn.close()

total_goals = result[0]
scottish_goals = result[1]

non_scottish_goals = total_goals - scottish_goals

labels = ['Scottish Goals', 'Non-Scottish Goals']
sizes = [scottish_goals, non_scottish_goals]
colors = ['#66b3ff', '#99ff99']

plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
plt.axis('equal')  
plt.title('Distribution of Goals')
plt.show()