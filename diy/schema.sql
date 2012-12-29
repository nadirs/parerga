drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    date_added integer not null,
    path text not null
);
