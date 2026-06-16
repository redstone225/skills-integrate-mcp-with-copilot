# Persistent storage: add a database backend

Description:

Replace the current in-memory `activities` storage with a persistent database (e.g. PostgreSQL or SQLite for local/dev). Move data access into a clear data layer and add migrations.

Acceptance criteria:
- Activities, participants, and student records persist across server restarts.
- Provide a simple migration or seed script to create sample activities.
- Update `README` with DB setup instructions.

Labels: enhancement, backend, database

Estimate: medium
