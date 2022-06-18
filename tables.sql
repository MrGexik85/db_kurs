CREATE TABLE bank_accounts (
    id integer NOT NULL,
    bank_name character varying NOT NULL,
    inn character varying NOT NULL,
    bik character varying NOT NULL,
    account character varying NOT NULL
);

CREATE TABLE categories (
    id integer NOT NULL,
    name character varying NOT NULL
);


CREATE TABLE contractors (
    id integer NOT NULL,
    title character varying NOT NULL,
    address character varying NOT NULL,
    director character varying NOT NULL,
    accountant character varying NOT NULL,
    bank_account_id integer NOT NULL
);


CREATE TABLE customers (
    id integer NOT NULL,
    title character varying NOT NULL,
    address character varying NOT NULL,
    phone character varying NOT NULL,
    first_name character varying NOT NULL,
    middle_name character varying,
    last_name character varying NOT NULL,
    bank_account_id integer NOT NULL,
    notes text,
    user_id integer
);

CREATE TABLE order_items (
    id integer NOT NULL,
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    product_count integer NOT NULL
);

CREATE TABLE orders (
    id integer NOT NULL,
    number integer NOT NULL,
    date timestamp without time zone NOT NULL,
    note text,
    delivery_terms character varying NOT NULL,
    customer_id integer NOT NULL,
    is_paid boolean NOT NULL,
    is_deliver boolean NOT NULL
);

CREATE TABLE product_contractor_association (
    product_id integer NOT NULL,
    contractor_id integer NOT NULL
);

CREATE TABLE product_supplies (
    id integer NOT NULL,
    contractor_id integer NOT NULL,
    product_id integer NOT NULL,
    amount integer NOT NULL,
    date timestamp without time zone NOT NULL
);

CREATE TABLE products (
    id integer NOT NULL,
    title character varying NOT NULL,
    description character varying,
    image_url character varying NOT NULL,
    price double precision NOT NULL,
    package character varying NOT NULL,
    category_id integer NOT NULL
);

CREATE TABLE users (
    id integer NOT NULL,
    username character varying NOT NULL,
    hashed_password character varying NOT NULL,
    is_admin boolean
);


ALTER TABLE ONLY public.contractors
    ADD CONSTRAINT contractors_bank_account_id_fkey FOREIGN KEY (bank_account_id) REFERENCES public.bank_accounts(id) ON DELETE CASCADE;


--
-- Name: customers customers_bank_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_bank_account_id_fkey FOREIGN KEY (bank_account_id) REFERENCES public.bank_accounts(id) ON DELETE CASCADE;


--
-- Name: customers customers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: order_items order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: orders orders_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id) ON DELETE CASCADE;


--
-- Name: product_contractor_association product_contractor_association_contractor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_contractor_association
    ADD CONSTRAINT product_contractor_association_contractor_id_fkey FOREIGN KEY (contractor_id) REFERENCES public.contractors(id) ON DELETE CASCADE;


--
-- Name: product_contractor_association product_contractor_association_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_contractor_association
    ADD CONSTRAINT product_contractor_association_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: product_supplies product_supplies_contractor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_supplies
    ADD CONSTRAINT product_supplies_contractor_id_fkey FOREIGN KEY (contractor_id) REFERENCES public.contractors(id) ON DELETE CASCADE;


--
-- Name: product_supplies product_supplies_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_supplies
    ADD CONSTRAINT product_supplies_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

