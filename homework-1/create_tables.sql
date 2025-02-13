-- SQL-команды для создания таблиц
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS employees;


CREATE TABLE customers (
    customer_id VARCHAR(5) PRIMARY KEY,
    company_name VARCHAR(50) NOT NULL,
    contact_name VARCHAR(50) NOT NULL
    );
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    title VARCHAR(50),
    birth_date VARCHAR(10),
    notes TEXT
    );
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id VARCHAR(5) REFERENCES customers(customer_id) NOT NULL,
    employee_id INT REFERENCES employees(employee_id) NOT NULL,
    order_date VARCHAR(10),
    ship_city VARCHAR(50)
    )