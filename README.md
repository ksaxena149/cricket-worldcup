# Relational Database Management System Project - ICC World Cup 2023 Match Details

## Description

This project is designed to manage and store information related to the ICC World Cup 2023 matches. It's intended for cricket enthusiasts, statisticians, and anyone interested in accessing, analyzing, and managing data related to the tournament. The system will include details such as teams, players, match schedules and scores. It provides an efficient way to query and manipulate this data, offering valuable insights into the tournament.

### Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- Git

### Installation

Follow these steps to get a copy of the project up and running on your local machine for development and testing purposes.

1. Clone the GitHub repository:

```bash
git clone https://github.com/ksaxena149/cricket-worldcup
```

2. Navigate to the directory where MySQL is installed and import the worldcup.sql file:

```bash
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
mysql -u your_username -p your_database < path_to_your_project_directory/data/worldcup.sql
```
Replace `your_username` with your MySQL username, `your_database` with the name of your MySQL database, and `path_to_your_project_directory` with the path to the directory where you cloned the repository.

3. Install the dependencies:

```bash
# Navigate back to your project directory
cd path_to_your_project_directory

# Install dependencies
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```
