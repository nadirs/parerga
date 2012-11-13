drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    date_added integer not null,
    path text not null
);

drop table if exists comments;
create table comments (
    id integer primary key autoincrement,
    entry_id integer not null,
    author text not null default 'anonymous',
    content text not null,
    foreign key(entry_id) references entries(id)
);
