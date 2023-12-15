CREATE DATABASE warehouses;

\c warehouses;

CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    name varchar (50) NOT NULL,
    password varchar (25) NOT NULL,
    head_of int[],
    activities TEXT[]
);

CREATE TABLE warehouse (
    id serial PRIMARY KEY,
    name varchar (30)
);

CREATE TABLE item (
    id SERIAL PRIMARY KEY,
    state TEXT NOT NULL,
    category varchar(30) NOT NULL,
    warehouse_id int REFERENCES warehouse(id),
    date_of_stock timestamp
);

