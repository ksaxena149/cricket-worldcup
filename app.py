from flask import Flask, render_template, request
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
    cursor.execute("SELECT match_id, match_date, stadium FROM match_details")
    matches = cursor.fetchall()
    
    return render_template('index.html', matches=matches)

@app.route('/match/<int:match_id>')
def match_details(match_id):
    cursor = mydb.cursor()
    
    # Fetch match details
    cursor.execute("SELECT match_date, stadium FROM match_details WHERE match_id = %s", (match_id,))
    match = cursor.fetchone()
    
    # Fetch distinct team IDs that played in the match
    cursor.execute("SELECT DISTINCT team_id FROM played WHERE match_id = %s", (match_id,))
    teams = [row[0] for row in cursor.fetchall()]
    
    # Fetch players and their scores for each team
    team_scorecards = {}
    for team_id in teams:
        cursor.execute("SELECT p.player_name, pl.score FROM played pl JOIN player p ON pl.player_id = p.player_id WHERE pl.match_id = %s AND pl.team_id = %s ORDER BY p.player_id", (match_id, team_id))
        team_scorecards[team_id] = cursor.fetchall()
    
    return render_template('match_details.html', match_id=match_id, match_date=match[0], stadium=match[1], team_scorecards=team_scorecards)

if __name__ == '__main__':
    app.run(debug=True)
