# Ad Campaigns and Channels

IT 566: Computer Scripting Techniques — Summer 2026 Semester Project

A console-based, multi-layered, data-driven Python application for managing
ad campaigns and the channels they run on. Campaigns can run across many
channels (search, social, email, video), and channels can host many
campaigns — a many-to-many relationship tracked through a cross-reference
table that also records the budget allocated to each specific
campaign-channel pairing.

## Architecture

The app follows a three-layer architecture:

- **Persistence layer** (`src/application_name/persistence_layer/`) — talks
  directly to MySQL, running queries and returning raw rows.
- **Service layer** (`src/application_name/service_layer/`) — sits between
  the persistence layer and the UI, turning raw database rows into real
  `Campaign` and `Channel` objects.
- **Presentation layer** (`src/application_name/presentation_layer/`) — the
  console menu the user actually interacts with.

Primary entities: `Campaign`, `Channel`.
Cross-reference table: `campaign_channel_xref`.

## Requirements

- Python 3.12+
- MySQL Server 8.0+
- The `mysql-connector-python` package:
```bash
  pip install mysql-connector-python
```

## Database setup

All database scripts live in the `database/` folder. To build the database
from scratch (drops and recreates everything — safe to run repeatedly):

```bash
cd database
chmod +x initialize_database.sh
./initialize_database.sh
```

This will prompt once for your MySQL root password, then automatically:
1. Drop the database and dedicated user if they exist
2. Recreate the database
3. Create a dedicated `ad_project_user` with scoped privileges
4. Create the `campaign`, `channel`, and `campaign_channel_xref` tables
5. Insert sample test data

Logs for each step are written to `database/logs/`.

To verify it worked:
```bash
mysql -u root -p -e "USE dipika_ad_project; SHOW TABLES; SELECT * FROM campaign;"
```

## Configuration

Database connection details live in
`config/application_name_app_config.json`. Update the `user`, `password`,
`host`, and `port` fields to match your local MySQL setup if they differ
from the defaults.

## Running the application

From the project root:

```bash
python src/main.py -c config/application_name_app_config.json
```

## Using the console menu
View Campaigns - lists all campaigns
Add Campaign - prompts for and creates a new campaign
View Channels - lists all channels
Add Channel - prompts for and creates a new channel
Link Channel to Campaign - links an existing channel to an existing
campaign, with an allocated spend amount
Exit

## Project structure

IT566_final_project/
├── config/
│ └── application_name_app_config.json
├── database/
│ ├── db_version_1/
│ │ ├── create_database.sql
│ │ ├── create_tables.sql
│ │ ├── create_user.sql
│ │ ├── drop_database.sql
│ │ ├── drop_tables.sql
│ │ ├── drop_user.sql
│ │ └── insert_test_data.sql
│ └── initialize_database.sh
├── src/
│ ├── main.py
│ └── application_name/
│ ├── campaign.py
│ ├── channel.py
│ ├── persistence_layer/
│ │ └── mysql_persistence_wrapper.py
│ ├── service_layer/
│ │ └── app_services.py
│ └── presentation_layer/
│ └── user_interface.py
└── README.md

