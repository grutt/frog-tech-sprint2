drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);

drop table if exists highlights;
create table highlights (
  id integer primary key autoincrement,
  startPos integer not null,
  endPos integer not null,
  'text' text not null
);
