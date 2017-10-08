drop table if exists products;
create table products (
  id integer primary key autoincrement,
  title text not null,
  price integer not null,
  image1 text not null,
  image2 text null,
  image3 text null,
  description text not null
);