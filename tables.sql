CREATE TABLE bank_accounts (
    id SERIAL PRIMARY KEY,
    bank_name character varying NOT NULL,
    inn character varying NOT NULL,
    bik character varying NOT NULL,
    account character varying NOT NULL
);


CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name character varying NOT NULL
);


CREATE TABLE contractors (
    id SERIAL PRIMARY KEY,
    title character varying NOT NULL,
    address character varying NOT NULL,
    director character varying NOT NULL,
    accountant character varying NOT NULL,
    bank_account_id integer NOT NULL REFERENCES bank_accounts (id) ON DELETE CASCADE
);


CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    title character varying NOT NULL,
    address character varying NOT NULL,
    phone character varying NOT NULL,
    first_name character varying NOT NULL,
    middle_name character varying,
    last_name character varying NOT NULL,
    bank_account_id integer NOT NULL REFERENCES bank_accounts (id) ON DELETE CASCADE,
    notes text,
    user_id integer REFERENCES users (id) ON DELETE CASCADE
);


CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id integer NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
    product_id integer NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    product_count integer NOT NULL
);


CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    number integer NOT NULL,
    date timestamp without time zone NOT NULL,
    note text,
    delivery_terms character varying NOT NULL,
    customer_id integer NOT NULL REFERENCES customers (id) ON DELETE CASCADE,
    is_paid boolean NOT NULL,
    is_deliver boolean NOT NULL
);


CREATE TABLE product_contractor_association (
    product_id integer PRIMARY KEY REFERENCES contractors (id) ON DELETE CASCADE,
    contractor_id integer PRIMARY KEY REFERENCES products (id) ON DELETE CASCADE
);


CREATE TABLE product_supplies (
    id SERIAL PRIMARY KEY,
    contractor_id integer NOT NULL REFERENCES contractors (id) ON DELETE CASCADE,
    product_id integer NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    amount integer NOT NULL,
    date timestamp without time zone NOT NULL
);


CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    title character varying NOT NULL,
    description character varying,
    image_url character varying NOT NULL,
    price double precision NOT NULL,
    package character varying NOT NULL,
    category_id integer NOT NULL REFERENCES categories (id) ON DELETE CASCADE
);


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username character varying NOT NULL,
    hashed_password character varying NOT NULL,
    is_admin boolean
);