🗃️ Database Schema Documentation



Overview

The Smart School Bus System uses SQLite database with 10+ relational tables implementing proper constraints and relationships.



Core Tables



accounts\_user

Description: Custom user model with role-based authentication

```sql

CREATE TABLE accounts\_user (

&nbsp;   id INTEGER PRIMARY KEY AUTOINCREMENT,

&nbsp;   password VARCHAR(128) NOT NULL,

&nbsp;   last\_login DATETIME,

&nbsp;   is\_superuser BOOLEAN NOT NULL,

&nbsp;   username VARCHAR(150) UNIQUE NOT NULL,

&nbsp;   first\_name VARCHAR(30) NOT NULL,

&nbsp;   last\_name VARCHAR(150) NOT NULL,

&nbsp;   email VARCHAR(254) NOT NULL,

&nbsp;   is\_staff BOOLEAN NOT NULL,

&nbsp;   is\_active BOOLEAN NOT NULL,

&nbsp;   date\_joined DATETIME NOT NULL,

&nbsp;   user\_type VARCHAR(20) NOT NULL,

&nbsp;   phone\_number VARCHAR(15),

&nbsp;   address TEXT

);





buses\_bus



Description: Bus information with unique identifiers



sql

CREATE TABLE buses\_bus (

&nbsp;   id INTEGER PRIMARY KEY AUTOINCREMENT,

&nbsp;   bus\_number VARCHAR(20) UNIQUE NOT NULL,

&nbsp;   capacity INTEGER NOT NULL,

&nbsp;   license\_plate VARCHAR(15) UNIQUE NOT NULL,

&nbsp;   gps\_device\_id VARCHAR(50) UNIQUE,

&nbsp;   is\_active BOOLEAN NOT NULL,

&nbsp;   driver\_id INTEGER REFERENCES accounts\_user(id)

);





students\_student



Description: Student records with parent relationships



sql

CREATE TABLE students\_student (

&nbsp;   id INTEGER PRIMARY KEY AUTOINCREMENT,

&nbsp;   student\_id VARCHAR(20) UNIQUE NOT NULL,

&nbsp;   first\_name VARCHAR(30) NOT NULL,

&nbsp;   last\_name VARCHAR(30) NOT NULL,

&nbsp;   grade VARCHAR(10) NOT NULL,

&nbsp;   parent\_id INTEGER NOT NULL REFERENCES accounts\_user(id),

&nbsp;   home\_address TEXT NOT NULL

);



bus\_notifications\_notification



Description: Notification system with multi-recipient support



sql

CREATE TABLE bus\_notifications\_notification (

&nbsp;   id INTEGER PRIMARY KEY AUTOINCREMENT,

&nbsp;   notification\_type VARCHAR(20) NOT NULL,

&nbsp;   title VARCHAR(200) NOT NULL,

&nbsp;   message TEXT NOT NULL,

&nbsp;   sender\_id INTEGER NOT NULL REFERENCES accounts\_user(id),

&nbsp;   bus\_id INTEGER REFERENCES buses\_bus(id),

&nbsp;   created\_at DATETIME NOT NULL,

&nbsp;   is\_sent BOOLEAN NOT NULL,

&nbsp;   is\_read BOOLEAN NOT NULL

);



bus\_notifications\_notification\_recipients



Description: Many-to-many relationship table (auto-created)



sql

CREATE TABLE bus\_notifications\_notification\_recipients (

&nbsp;   id INTEGER PRIMARY KEY AUTOINCREMENT,

&nbsp;   notification\_id INTEGER NOT NULL REFERENCES bus\_notifications\_notification(id),

&nbsp;   user\_id INTEGER NOT NULL REFERENCES accounts\_user(id)

);



routes\_route



Description: Bus routes and path management



sql

CREATE TABLE routes\_route (

&nbsp;   id INTEGER PRIMARY KEY AUTOINCREMENT,

&nbsp;   route\_name VARCHAR(100) NOT NULL,

&nbsp;   bus\_id INTEGER NOT NULL REFERENCES buses\_bus(id),

&nbsp;   is\_active BOOLEAN NOT NULL,

&nbsp;   created\_at DATETIME NOT NULL

);



routes\_routepoint



Description: Individual stops on routes



sql

CREATE TABLE routes\_routepoint (

&nbsp;   id INTEGER PRIMARY KEY AUTOINCREMENT,

&nbsp;   route\_id INTEGER NOT NULL REFERENCES routes\_route(id),

&nbsp;   location\_name VARCHAR(100) NOT NULL,

&nbsp;   latitude DECIMAL(9,6),

&nbsp;   longitude DECIMAL(9,6),

&nbsp;   sequence\_order INTEGER NOT NULL,

&nbsp;   estimated\_time INTERVAL

);



tracking\_buslocation



Description: GPS location tracking history



sql

CREATE TABLE tracking\_buslocation (

&nbsp;   id INTEGER PRIMARY KEY AUTOINCREMENT,

&nbsp;   bus\_id INTEGER NOT NULL REFERENCES buses\_bus(id),

&nbsp;   latitude DECIMAL(9,6) NOT NULL,

&nbsp;   longitude DECIMAL(9,6) NOT NULL,

&nbsp;   speed DECIMAL(5,2),

&nbsp;   timestamp DATETIME NOT NULL

);



tracking\_studentattendance



Description: Student attendance records



sql

CREATE TABLE tracking\_studentattendance (

&nbsp;   id INTEGER PRIMARY KEY AUTOINCREMENT,

&nbsp;   student\_id INTEGER NOT NULL REFERENCES students\_student(id),

&nbsp;   bus\_id INTEGER NOT NULL REFERENCES buses\_bus(id),

&nbsp;   date DATE NOT NULL,

&nbsp;   status VARCHAR(10) NOT NULL,

&nbsp;   check\_in\_time DATETIME,

&nbsp;   check\_out\_time DATETIME

);



**Key Relationships**

**One-to-Many Relationships:**

* One User (Parent) → Many Students
* One Bus → Many Location Updates
* One Route → Many Route Points
* One Bus → Many Attendance Records



**Many-to-Many Relationships:**

* Notifications ↔ Users (via bus\_notifications\_notification\_recipients)



**One-to-One Relationships:**

* User ↔ Student (for student user accounts)



**Data Integrity Features**

**Unique Constraints:**

* username in accounts\_user
* bus\_number in buses\_bus
* license\_plate in buses\_bus
* gps\_device\_id in buses\_bus
* student\_id in students\_student



**Foreign Key Constraints:**

* All related tables have proper foreign key relationships
* Cascade deletions where appropriate
* SET NULL for optional relationships



**Business Logic Enforcement:**

* Role validation through application logic
* Data validation at model and form levels
* Permission checks in views



**Indexing Strategy**

**Automatic Indexes (Django created):**

* Primary key indexes on all tables
* Foreign key indexes for relationships
* Unique constraint indexes



**Performance Considerations:**

* Frequent queries on user roles and bus status
* Location data queries for real-time tracking
* Notification queries by recipient and date



Data Models Summary

Table	Records	Key Fields	Relationships

accounts\_user	Users	username, user\_type	Parent of students

buses\_bus	Buses	bus\_number, license\_plate	Has driver, locations

students\_student	Students	student\_id, grade	Belongs to parent, bus

bus\_notifications\_notification	Notifications	type, title, message	Has recipients, bus

routes\_route	Routes	route\_name, bus\_id	Has points

tracking\_buslocation	Locations	bus\_id, timestamp	Belongs to bus

tracking\_studentattendance	Attendance	student\_id, date	

