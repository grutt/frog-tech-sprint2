drop table if exists users;
create table users (
  uid integer primary key autoincrement,
  name text not null
);

drop table if exists respondents;
create table respondents (
  rid integer primary key autoincrement,
  name text not null,
  description text
);

drop table if exists transcripts;
create table transcripts (
    tid integer primary key autoincrement,
    rid integer,
    uid integer,
    'time' datetime
);

drop table if exists blurbs;
create table blurbs(
    bid integer primary key autoincrement,
    rid integer,
    uid integer,
    tid integer,
    blurb text,
    'time' datetime,
    score integer
);

drop table if exists comments;
create table comments(
    cid integer primary key autoincrement,
    bid integer,
    uid integer,
    blurb text,
    'time' datetime
);

drop table if exists tagTypes;
create table tagTypes(
    tagTypeid integer primary key autoincrement,
    name text,
    color text,
    icon text,
    score integer
);

drop table if exists tags;
create table tags(
    tagid integer primary key autoincrement,
    bid integer,
    tagType integer,
    uid integer
);

drop table if exists insights;
create table insights(
    iid integer primary key autoincrement,
    blurb text,
    count integer
);

drop table if exists insightPool;
create table insightPool(
    pid integer primary key autoincrement,
    iid text,
    bid integer,
    uid integer
);
