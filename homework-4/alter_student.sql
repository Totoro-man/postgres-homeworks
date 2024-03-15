-- 1. Создать таблицу student с полями student_id serial, first_name varchar, last_name varchar, birthday date, phone varchar
CREATE TABLE student
(
    student_id serial,
    first_name varchar,
    last_name varchar,
    birthday date,
    phone varchar
);

-- 2. Добавить в таблицу student колонку middle_name varchar
ALTER TABLE student ADD COLUMN middle_name varchar;

-- 3. Удалить колонку middle_name
ALTER TABLE student DROP COLUMN middle_name;

-- 4. Переименовать колонку birthday в birth_date
ALTER TABLE student RENAME birthday TO birth_date;

-- 5. Изменить тип данных колонки phone на varchar(32)
ALTER TABLE student ALTER COLUMN phone SET DATA TYPE varchar(32);

-- 6. Вставить три любых записи с автогенерацией идентификатора
INSERT INTO student (first_name, last_name, birth_date, phone)
VALUES ('Giovanni', 'Rodari', TO_DATE('23/10/1920', 'DD/MM/YYYY'), 01);
INSERT INTO student (first_name, last_name, birth_date, phone)
VALUES ('Rudyard', 'Kipling', TO_DATE('18/01/1936', 'DD/MM/YYYY'), 02);
INSERT INTO student (first_name, last_name, birth_date, phone)
VALUES ('Николай', 'Носов', TO_DATE('23/11/1908', 'DD/MM/YYYY'), 03);
INSERT INTO student (first_name, last_name, birth_date, phone)
VALUES ('Charles', 'Dodgson', TO_DATE('27/01/1832', 'DD/MM/YYYY'), 04);
-- 7. Удалить все данные из таблицы со сбросом идентификатор в исходное состояние
TRUNCATE TABLE student RESTART IDENTITY