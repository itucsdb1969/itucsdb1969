Developer Guide
===============

Database Design
---------------

Our database consists of 6 main tables.
These tables have at least 1 primary key, 5 non-key attributes.

**Our Main tables: Users, Team, Player, Match, Stadium, Appointment**

.. figure:: tables_diagram.jpg

**Main Tables** 


Every user has user_id as a primary key, name as a unique attribute, password, email, is_active, and is_admin.

*user_id, name, password, email, is_active, is_admin*


Each player has a player_id as a primary key, team_id that references Team(team_id), user_id that references Users(user_id), name, rating, age, country, phone_number.

*player_id, team_id, user_id, name, rating, age, country, phone_number*


Each team has a team_id as a primary key, name as a unique attribute, rating, created_at, max_player_number, is_available.

*team_id, name, rating, created_at, max_player_number, is_available*


Each match has a match_id as a primary key, team1_id references Team(team_id), team2_id references Team(team_id), created_at, updated_at, date, referee, length.

*match_id, team1_id, team2_id, created_at, updated_at, date, referee, length*


Each stadium has a stadium_id as a primary key, name as a unique attribute, city, created_at, is_available, rating.

*stadium_id, name, city, created_at, is_available, and rating*


Each appointment has a appointment_id which is the primary key, match_id that references Match(match_id), stadium_id references Stadium(stadium_id).

*appointment_id, name, match_id, stadium_id, start_time, end_time, date, created_at*


.. toctree::

   ihsan
   huseyin

