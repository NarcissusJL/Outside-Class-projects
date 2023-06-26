# COVID-19 Health Information Management System

This project is a COVID-19 Health Information Management System developed in Python. It automates the process of collecting, analyzing, and reporting health-related data for college department.


# Description(email.py)

The COVID-19 Health Information Management System is designed to help departments or organizations manage health-related information of their members during the COVID-19 pandemic. It connects to a MySQL database and performs various data processing tasks, including generating reports, exporting data to CSV files, and sending email notifications.

The system performs the following tasks:

- Retrieves department information from the MySQL database.
- Collects data on individuals who have not reported their health status for the day.
- Identifies individuals with high body temperature.
- Flags individuals with non-green health codes.
- Detects individuals with non-green or starred trip codes.
- Tracks individuals who participated in contact tracing activities.
- Records individuals who are not currently in the local area.
- Manages other exceptional cases specified in the database.
- Generates CSV files for each type of exception.
- Sends email notifications to department representatives with the exception reports attached.

# Description(monitor.py)

- Monitors multiple MySQL databases for non-compliant health codes and trip codes.
- Sends notifications to stakeholders through the DingDing API.
- Supports separate databases for teachers, students, and other groups.
- Configurable sleep time between iterations for customization.
- Easy configuration and setup.
