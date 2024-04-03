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

if __name__ == '__main__':
    app.run(debug=True)
