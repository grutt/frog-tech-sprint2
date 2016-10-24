#!/bin/bash
echo -e ".mode csv \n.import static/csv/Blurbs.csv blurbs" | sqlite3 pond.db;
echo -e ".mode csv \n.import static/csv/Transcripts.csv transcripts" | sqlite3 pond.db;
echo -e ".mode csv \n.import static/csv/Respondent.csv respondents" | sqlite3 pond.db;
echo -e ".mode csv \n.import static/csv/User.csv users" | sqlite3 pond.db;
echo -e ".mode csv \n.import static/csv/tagType.csv tagTypes" | sqlite3 pond.db;
