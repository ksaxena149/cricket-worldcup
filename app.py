from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aaaa",
    database="worldcup"
)

# Define routes
@app.route('/')
def index():
    cursor = mydb.cursor()
    
    # Fetch match details
    cursor.execute("SELECT match_id, match_date, stadium FROM match_details")
    matches = cursor.fetchall()
    
    # Fetch team names for each match
    match_teams = {}
    for match in matches:
        cursor.execute("""
            SELECT t.team_s_name 
            FROM played p 
            JOIN team t ON p.team_id = t.team_id 
            WHERE p.match_id = %s
            GROUP BY t.team_s_name
        """, (match[0],))
        teams = [row[0] for row in cursor.fetchall()]
        match_teams[match[0]] = teams
    
    return render_template('index.html', matches=matches, match_teams=match_teams)

@app.route('/match/<int:match_id>')
def match_details(match_id):
    cursor = mydb.cursor()
    
    # Fetch match details
    cursor.execute("SELECT match_date, stadium FROM match_details WHERE match_id = %s", (match_id,))
    match = cursor.fetchone()
    
    # Fetch distinct team names that played in the match
    cursor.execute("""
        SELECT DISTINCT t.team_name 
        FROM played p 
        JOIN team t ON p.team_id = t.team_id 
        WHERE p.match_id = %s
    """, (match_id,))
    teams = [row[0] for row in cursor.fetchall()]
    
    # Fetch players and their scores for each team
    team_scorecards = {}
    for team_name in teams:
        cursor.execute("""
            SELECT p.player_name, pl.score 
            FROM played pl 
            JOIN player p ON pl.player_id = p.player_id 
            JOIN team t ON pl.team_id = t.team_id 
            WHERE pl.match_id = %s AND t.team_name = %s 
            ORDER BY p.player_id
        """, (match_id, team_name))
        team_scorecards[team_name] = cursor.fetchall()
    
    return render_template('match_details.html', match_id=match_id, match_date=match[0], stadium=match[1], team_scorecards=team_scorecards)

@app.route('/add_match', methods=['GET', 'POST'])
def add_match():
    if request.method == 'POST':
        match_date = request.form['match_date']
        stadium = request.form['stadium']
        teams = request.form.getlist('teams')
        players = request.form.getlist('players')
        scores = request.form.getlist('scores')

        cursor = mydb.cursor()
        cursor.execute("INSERT INTO match_details (match_date, stadium) VALUES (%s, %s)", (match_date, stadium))
        match_id = cursor.lastrowid

        for team, player, score in zip(teams, players, scores):
            cursor.execute("INSERT INTO played (match_id, score, team_id, player_id) VALUES (%s, %s, (SELECT team_id FROM team WHERE team_name = %s), (SELECT player_id FROM player WHERE player_name = %s))", (match_id, score, team, player))

        mydb.commit()
        return redirect(url_for('index'))

    else:
        cursor = mydb.cursor()
        cursor.execute("SELECT team_name FROM team")
        teams = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT player_name FROM player")
        players = [row[0] for row in cursor.fetchall()]
        return render_template('add_match.html', teams=teams, players=players)

@app.route('/delete_match/<int:match_id>', methods=['POST'])
def delete_match(match_id):
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM match_details WHERE match_id = %s", (match_id,))
    mydb.commit()
    return redirect(url_for('index'))

@app.route('/update_match/<int:match_id>', methods=['GET', 'POST'])
def update_match(match_id):
    cursor = mydb.cursor()

    if request.method == 'POST':
        match_date = request.form['match_date']
        stadium = request.form['stadium']
        cursor.execute("UPDATE match_details SET match_date = %s, stadium = %s WHERE match_id = %s", (match_date, stadium, match_id))
        mydb.commit()
        return redirect(url_for('match_details', match_id=match_id))

    else:
        cursor.execute("SELECT match_date, stadium FROM match_details WHERE match_id = %s", (match_id,))
        match = cursor.fetchone()
        return render_template('update_match.html', match_id=match_id, match_date=match[0], stadium=match[1])

if __name__ == '__main__':
    app.run(debug=True)
