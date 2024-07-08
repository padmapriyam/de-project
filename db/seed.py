"""Usage:
    PGUSER=<user> PGHOST=<host> PGPORT=<port> PGDATABASE=<database> PGPASSWORD=<password> seed.py
"""

from db.connection import con
from pg8000.native import literal
from db.data.address import addresses
from db.data.counterparty import counterparties
from db.data.currency import currencies
from db.data.department import departments
from db.data.design import designs
from db.data.payment_type import payment_types
from db.data.payment import payments
from db.data.purchase_order import purchase_orders
from db.data.sales_order import sales_orders
from db.data.staff import staff
from db.data.transaction import transactions


def seed(
    addresses,
    counterparties,
    currencies,
    departments,
    designs,
    payment_types,
    payments,
    purchase_orders,
    sales_orders,
    staff,
    transactions,
):

    con.run("DROP TABLE IF EXISTS payment;")
    con.run("DROP TABLE IF EXISTS transaction;")
    con.run("DROP TABLE IF EXISTS sales_order;")
    con.run("DROP TABLE IF EXISTS purchase_order;")
    con.run("DROP TABLE IF EXISTS staff;")
    con.run("DROP TABLE IF EXISTS counterparty;")
    con.run("DROP TABLE IF EXISTS address;")
    con.run("DROP TABLE IF EXISTS currency;")
    con.run("DROP TABLE IF EXISTS department;")
    con.run("DROP TABLE IF EXISTS design;")
    con.run("DROP TABLE IF EXISTS payment_type;")
    con.run('DROP TYPE IF EXISTS "TransactionType";')
    con.run('DROP TYPE IF EXISTS "PaymentTypeName";')

    create_types()
    create_address()
    create_counterparty()
    create_currency()
    create_department()
    create_design()
    create_payment_type()
    create_staff()
    create_purchase_order()
    create_sales_order()
    create_transaction()
    create_payment()
    add_constraints()

    insert_addresses(addresses)
    insert_counterparties(counterparties)
    insert_currencies(currencies)
    insert_departments(departments)
    insert_designs(designs)
    insert_payment_types(payment_types)
    insert_staff(staff)
    insert_purchase_orders(purchase_orders)
    insert_sales_orders(sales_orders)
    insert_transactions(transactions)
    insert_payments(payments)


def create_types():
    con.run(
        (
            'CREATE TYPE public."PaymentTypeName" AS ENUM ('
            "    'SALES_RECEIPT',"
            "    'SALES_REFUND',"
            "    'PURCHASE_PAYMENT',"
            "    'PURCHASE_REFUND'"
            ");"
        )
    )
    con.run(
        (
            'CREATE TYPE public."TransactionType" AS ENUM ('
            "    'SALE',"
            "    'PURCHASE'"
            ");"
        )
    )


def create_address():
    con.run(
        (
            "CREATE TABLE public.address ("
            "    address_id integer NOT NULL,"
            "    address_line_1 text NOT NULL,"
            "    address_line_2 text,"
            "    district text,"
            "    city text NOT NULL,"
            "    postal_code text NOT NULL,"
            "    country text NOT NULL,"
            "    phone text NOT NULL,"
            "    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL"
            ","
            "last_updated timestamp(3) without time zone NOT NULL"
            ");"
        )
    )


def create_counterparty():
    con.run(
        (
            "CREATE TABLE public.counterparty ("
            "    counterparty_id integer NOT NULL,"
            "    counterparty_legal_name text NOT NULL,"
            "    legal_address_id integer NOT NULL,"
            "    commercial_contact text,"
            "    delivery_contact text,"
            "    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,"
            "    last_updated timestamp(3) without time zone NOT NULL"
            ");"
        )
    )


def create_currency():
    con.run(
        (
            "CREATE TABLE public.currency ("
            "    currency_id integer NOT NULL,"
            "    currency_code character varying(3) NOT NULL,"
            "    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,"
            "    last_updated timestamp(3) without time zone NOT NULL"
            ");"
        )
    )


def create_department():
    con.run(
        (
            "CREATE TABLE public.department ("
            "    department_id integer NOT NULL,"
            "    department_name text NOT NULL,"
            "    location text,"
            "    manager text,"
            "    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,"
            "    last_updated timestamp(3) without time zone NOT NULL"
            ");"
        )
    )


def create_design():
    con.run(
        (
            "CREATE TABLE public.design ("
            "    design_id integer NOT NULL,"
            "    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,"
            "    design_name text NOT NULL,"
            "    file_location text NOT NULL,"
            "    file_name text NOT NULL,"
            "    last_updated timestamp(3) without time zone NOT NULL"
            ");"
        )
    )


def create_payment_type():
    con.run(
        (
            "CREATE TABLE public.payment_type ("
            "    payment_type_id integer NOT NULL,"
            '    payment_type_name public."PaymentTypeName" NOT NULL,'
            "    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,"
            "    last_updated timestamp(3) without time zone NOT NULL"
            ");"
        )
    )


def create_staff():
    con.run(
        (
            "CREATE TABLE public.staff ("
            "    staff_id integer NOT NULL,"
            "    first_name text NOT NULL,"
            "    last_name text NOT NULL,"
            "    department_id integer NOT NULL,"
            "    email_address text NOT NULL,"
            "    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,"
            "    last_updated timestamp(3) without time zone NOT NULL"
            ");"
        )
    )


def create_purchase_order():
    con.run(
        (
            "CREATE TABLE public.purchase_order ("
            "    purchase_order_id integer NOT NULL,"
            "    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL"
            ","
            "    last_updated timestamp(3) without time zone NOT NULL,"
            "    staff_id integer NOT NULL,"
            "    counterparty_id integer NOT NULL,"
            "    item_code text NOT NULL,"
            "    item_quantity integer NOT NULL,"
            "    item_unit_price numeric(10,2) NOT NULL,"
            "    currency_id integer NOT NULL,"
            "    agreed_delivery_date text NOT NULL,"
            "    agreed_payment_date text NOT NULL,"
            "    agreed_delivery_location_id integer NOT NULL"
            ");"
        )
    )


def create_sales_order():
    con.run(
        (
            "CREATE TABLE public.sales_order ("
            "    sales_order_id integer NOT NULL,"
            "    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,"
            "    last_updated timestamp(3) without time zone NOT NULL,"
            "    design_id integer NOT NULL,"
            "    staff_id integer NOT NULL,"
            "    counterparty_id integer NOT NULL,"
            "    units_sold integer NOT NULL,"
            "    unit_price numeric(10,2) NOT NULL,"
            "    currency_id integer NOT NULL,"
            "    agreed_delivery_date text NOT NULL,"
            "    agreed_payment_date text NOT NULL,"
            "    agreed_delivery_location_id integer NOT NULL"
            ");"
        )
    )


def create_transaction():
    con.run(
        (
            "CREATE TABLE public.transaction ("
            "    transaction_id integer NOT NULL,"
            '    transaction_type public."TransactionType" NOT NULL,'
            "    sales_order_id integer,"
            "    purchase_order_id integer,"
            "    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,"
            "    last_updated timestamp(3) without time zone NOT NULL"
            ");"
        )
    )


def create_payment():
    con.run(
        (
            "CREATE TABLE public.payment ("
            "    payment_id integer NOT NULL,"
            "    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,"
            "    last_updated timestamp(3) without time zone NOT NULL,"
            "    transaction_id integer NOT NULL,"
            "    counterparty_id integer NOT NULL,"
            "    payment_amount numeric(10,2) NOT NULL,"
            "    currency_id integer NOT NULL,"
            "    payment_type_id integer NOT NULL,"
            "    paid boolean NOT NULL,"
            "    payment_date text NOT NULL,"
            "    company_ac_number integer NOT NULL,"
            "    counterparty_ac_number integer NOT NULL"
            ");"
        )
    )


def add_constraints():
    con.run(
        (
            "ALTER TABLE ONLY address"
            "    ADD CONSTRAINT address_pkey PRIMARY KEY (address_id);"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY counterparty"
            "    ADD CONSTRAINT counterparty_pkey PRIMARY KEY (counterparty_id);"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY currency"
            "    ADD CONSTRAINT currency_pkey PRIMARY KEY (currency_id);"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY department"
            "    ADD CONSTRAINT department_pkey PRIMARY KEY (department_id);"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY design"
            "    ADD CONSTRAINT design_pkey PRIMARY KEY (design_id);"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY payment"
            "    ADD CONSTRAINT payment_pkey PRIMARY KEY (payment_id);"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY payment_type"
            "    ADD CONSTRAINT payment_type_pkey PRIMARY KEY (payment_type_id);"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY purchase_order"
            "    ADD CONSTRAINT purchase_order_pkey PRIMARY KEY (purchase_order_id);"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY sales_order"
            "    ADD CONSTRAINT sales_order_pkey PRIMARY KEY (sales_order_id);"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY staff"
            "    ADD CONSTRAINT staff_pkey PRIMARY KEY (staff_id);"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY transaction"
            "    ADD CONSTRAINT transaction_pkey PRIMARY KEY (transaction_id);"
        )
    )

    con.run(
        (
            "CREATE UNIQUE INDEX payment_transaction_id_key ON public.payment"
            " USING btree (transaction_id);"
        )
    )
    con.run(
        (
            "CREATE UNIQUE INDEX transaction_purchase_order_id_key ON public.transaction"
            " USING btree (purchase_order_id);"
        )
    )
    con.run(
        (
            "CREATE UNIQUE INDEX transaction_sales_order_id_key ON public.transaction"
            " USING btree (sales_order_id);"
        )
    )

    con.run(
        (
            "ALTER TABLE ONLY public.counterparty"
            "    ADD CONSTRAINT counterparty_legal_address_id_fkey "
            "FOREIGN KEY (legal_address_id) REFERENCES public.address(address_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY public.payment"
            "    ADD CONSTRAINT payment_counterparty_id_fkey "
            "FOREIGN KEY (counterparty_id) REFERENCES public.counterparty(counterparty_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY public.payment"
            "    ADD CONSTRAINT payment_currency_id_fkey "
            "FOREIGN KEY (currency_id) REFERENCES public.currency(currency_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY public.payment"
            "    ADD CONSTRAINT payment_payment_type_id_fkey "
            "FOREIGN KEY (payment_type_id) REFERENCES public.payment_type(payment_type_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    # con.run(
    #     (
    #         "ALTER TABLE ONLY public.payment"
    #         "    ADD CONSTRAINT payment_transaction_id_fkey "
    #         "FOREIGN KEY (transaction_id) REFERENCES public.transaction(transaction_id) "
    #         "ON UPDATE CASCADE ON DELETE RESTRICT;"
    #     )
    # )
    con.run(
        (
            "ALTER TABLE ONLY public.purchase_order"
            "    ADD CONSTRAINT purchase_order_agreed_delivery_location_id_fkey "
            "FOREIGN KEY (agreed_delivery_location_id) REFERENCES public.address(address_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY public.purchase_order"
            "    ADD CONSTRAINT purchase_order_counterparty_id_fkey "
            "FOREIGN KEY (counterparty_id) REFERENCES public.counterparty(counterparty_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY public.purchase_order"
            "    ADD CONSTRAINT purchase_order_currency_id_fkey "
            "FOREIGN KEY (currency_id) REFERENCES public.currency(currency_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY public.purchase_order"
            "    ADD CONSTRAINT purchase_order_staff_id_fkey "
            "FOREIGN KEY (staff_id) REFERENCES public.staff(staff_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY public.sales_order"
            "    ADD CONSTRAINT sales_order_agreed_delivery_location_id_fkey "
            "FOREIGN KEY (agreed_delivery_location_id) REFERENCES public.address(address_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY public.sales_order"
            "    ADD CONSTRAINT sales_order_counterparty_id_fkey "
            "FOREIGN KEY (counterparty_id) REFERENCES public.counterparty(counterparty_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY public.sales_order"
            "    ADD CONSTRAINT sales_order_currency_id_fkey "
            "FOREIGN KEY (currency_id) REFERENCES public.currency(currency_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    # con.run(
    #     (
    #         "ALTER TABLE ONLY public.sales_order"
    #         "    ADD CONSTRAINT sales_order_design_id_fkey "
    #         "FOREIGN KEY (design_id) REFERENCES public.design(design_id) "
    #         "ON UPDATE CASCADE ON DELETE RESTRICT;"
    #     )
    # )
    con.run(
        (
            "ALTER TABLE ONLY public.sales_order"
            "    ADD CONSTRAINT sales_order_staff_id_fkey "
            "FOREIGN KEY (staff_id) REFERENCES public.staff(staff_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    con.run(
        (
            "ALTER TABLE ONLY public.staff"
            "    ADD CONSTRAINT staff_department_id_fkey "
            "FOREIGN KEY (department_id) REFERENCES public.department(department_id) "
            "ON UPDATE CASCADE ON DELETE RESTRICT;"
        )
    )
    # con.run(
    #     (
    #         "ALTER TABLE ONLY public.transaction"
    #         "    ADD CONSTRAINT transaction_purchase_order_id_fkey "
    #         "FOREIGN KEY (purchase_order_id) REFERENCES public.purchase_order(purchase_order_id) "
    #         "ON UPDATE CASCADE ON DELETE SET NULL;"
    #     )
    # )
    # con.run(
    #     (
    #         "ALTER TABLE ONLY public.transaction"
    #         "    ADD CONSTRAINT transaction_sales_order_id_fkey "
    #         "FOREIGN KEY (sales_order_id) REFERENCES public.sales_order(sales_order_id) "
    #         "ON UPDATE CASCADE ON DELETE SET NULL;"
    #     )
    # )


def insert_addresses(addresses):
    start_of_query = (
        "INSERT INTO public.address "
        "(address_id, address_line_1, address_line_2, district, city, "
        "postal_code, country, phone, created_at, last_updated) "
        "VALUES "
    )

    values = ", ".join(
        [
            (
                f"({literal(address['address_id'])}, "
                f"{literal(address['address_line_1'])}, "
                f"{literal(address['address_line_2'])}, "
                f"{literal(address['district'])}, "
                f"{literal(address['city'])}, "
                f"{literal(address['postal_code'])}, "
                f"{literal(address['country'])}, "
                f"{literal(address['phone'])}, "
                f"{literal(address['created_at'])}, "
                f"{literal(address['last_updated'])})"
            )
            for address in addresses
        ]
    )

    query = start_of_query + values

    con.run(query)


def insert_counterparties(counterparties):
    start_of_query = (
        "INSERT INTO public.counterparty "
        "(counterparty_id, counterparty_legal_name, legal_address_id, "
        "delivery_contact, created_at, last_updated) "
        "VALUES "
    )

    values = ", ".join(
        [
            (
                f"({literal(counterparty['counterparty_id'])}, "
                f"{literal(counterparty['counterparty_legal_name'])}, "
                f"{literal(counterparty['legal_address_id'])}, "
                f"{literal(counterparty['delivery_contact'])}, "
                f"{literal(counterparty['created_at'])}, "
                f"{literal(counterparty['last_updated'])})"
            )
            for counterparty in counterparties
        ]
    )

    query = start_of_query + values

    con.run(query)


def insert_currencies(currencies):
    start_of_query = (
        "INSERT INTO public.currency "
        "(currency_id, currency_code, created_at, last_updated) "
        "VALUES "
    )

    values = ", ".join(
        [
            (
                f"({literal(currency['currency_id'])}, "
                f"{literal(currency['currency_code'])}, "
                f"{literal(currency['created_at'])}, "
                f"{literal(currency['last_updated'])})"
            )
            for currency in currencies
        ]
    )

    query = start_of_query + values

    con.run(query)


def insert_departments(departments):
    start_of_query = (
        "INSERT INTO public.department "
        "(department_id, department_name, location, "
        "manager, created_at, last_updated) "
        "VALUES "
    )

    values = ", ".join(
        [
            (
                f"({literal(department['department_id'])}, "
                f"{literal(department['department_name'])}, "
                f"{literal(department['location'])}, "
                f"{literal(department['manager'])}, "
                f"{literal(department['created_at'])}, "
                f"{literal(department['last_updated'])})"
            )
            for department in departments
        ]
    )

    query = start_of_query + values

    con.run(query)


def insert_designs(designs):
    start_of_query = (
        "INSERT INTO public.design "
        "(design_id, created_at, design_name, "
        "file_location, file_name, last_updated) "
        "VALUES "
    )

    values = ", ".join(
        [
            (
                f"({literal(design['design_id'])}, "
                f"{literal(design['created_at'])}, "
                f"{literal(design['design_name'])}, "
                f"{literal(design['file_location'])}, "
                f"{literal(design['file_name'])}, "
                f"{literal(design['last_updated'])})"
            )
            for design in designs
        ]
    )

    query = start_of_query + values

    con.run(query)


def insert_payment_types(payment_types):
    start_of_query = (
        "INSERT INTO public.payment_type "
        "(payment_type_id, payment_type_name, created_at, last_updated) "
        "VALUES "
    )

    values = ", ".join(
        [
            (
                f"({literal(payment_type['payment_type_id'])}, "
                f"{literal(payment_type['payment_type_name'])}, "
                f"{literal(payment_type['created_at'])}, "
                f"{literal(payment_type['last_updated'])})"
            )
            for payment_type in payment_types
        ]
    )

    query = start_of_query + values

    con.run(query)


def insert_staff(staff):
    start_of_query = (
        "INSERT INTO public.staff "
        "(staff_id, first_name, last_name, department_id, "
        "email_address, created_at, last_updated) "
        "VALUES "
    )

    values = ", ".join(
        [
            (
                f"({literal(staff_member['staff_id'])}, "
                f"{literal(staff_member['first_name'])}, "
                f"{literal(staff_member['last_name'])}, "
                f"{literal(staff_member['department_id'])}, "
                f"{literal(staff_member['email_address'])}, "
                f"{literal(staff_member['created_at'])}, "
                f"{literal(staff_member['last_updated'])})"
            )
            for staff_member in staff
        ]
    )

    query = start_of_query + values

    con.run(query)


def insert_purchase_orders(purchase_orders):
    start_of_query = (
        "INSERT INTO public.purchase_order "
        "(purchase_order_id, created_at, last_updated, staff_id, "
        "counterparty_id, item_code, item_quantity, item_unit_price, currency_id, "
        "agreed_delivery_date, agreed_payment_date, agreed_delivery_location_id) "
        "VALUES "
    )

    values = ", ".join(
        [
            (
                "("
                f"{literal(purchase_order['purchase_order_id'])}, "
                f"{literal(purchase_order['created_at'])}, "
                f"{literal(purchase_order['last_updated'])}, "
                f"{literal(purchase_order['staff_id'])}, "
                f"{literal(purchase_order['counterparty_id'])}, "
                f"{literal(purchase_order['item_code'])}, "
                f"{literal(purchase_order['item_quantity'])}, "
                f"{literal(purchase_order['item_unit_price'])}, "
                f"{literal(purchase_order['currency_id'])}, "
                f"{literal(purchase_order['agreed_delivery_date'])}, "
                f"{literal(purchase_order['agreed_payment_date'])}, "
                f"{literal(purchase_order['agreed_delivery_location_id'])})"
            )
            for purchase_order in purchase_orders
        ]
    )

    query = start_of_query + values

    con.run(query)


def insert_sales_orders(sales_orders):
    start_of_query = (
        "INSERT INTO public.sales_order "
        "(sales_order_id, created_at, last_updated, design_id, staff_id, "
        "counterparty_id, units_sold, unit_price, currency_id, "
        "agreed_delivery_date, agreed_payment_date, agreed_delivery_location_id) "
        "VALUES "
    )

    values = ", ".join(
        [
            (
                "("
                f"{literal(sales_order['sales_order_id'])}, "
                f"{literal(sales_order['created_at'])}, "
                f"{literal(sales_order['last_updated'])}, "
                f"{literal(sales_order['design_id'])}, "
                f"{literal(sales_order['staff_id'])}, "
                f"{literal(sales_order['counterparty_id'])}, "
                f"{literal(sales_order['units_sold'])}, "
                f"{literal(sales_order['unit_price'])}, "
                f"{literal(sales_order['currency_id'])}, "
                f"{literal(sales_order['agreed_delivery_date'])}, "
                f"{literal(sales_order['agreed_payment_date'])}, "
                f"{literal(sales_order['agreed_delivery_location_id'])})"
            )
            for sales_order in sales_orders
        ]
    )

    query = start_of_query + values

    con.run(query)


def insert_transactions(transactions):
    start_of_query = (
        "INSERT INTO public.transaction "
        "(transaction_id, transaction_type, sales_order_id, "
        "purchase_order_id, created_at, last_updated) "
        "VALUES "
    )

    values = ", ".join(
        [
            (
                "("
                f"{literal(transaction['transaction_id'])}, "
                f"{literal(transaction['transaction_type'])}, "
                f"{literal(transaction['sales_order_id'])}, "
                f"{literal(transaction['purchase_order_id'])}, "
                f"{literal(transaction['created_at'])}, "
                f"{literal(transaction['last_updated'])})"
            )
            for transaction in transactions
        ]
    )

    query = start_of_query + values

    con.run(query)


def insert_payments(payments):
    start_of_query = (
        "INSERT INTO public.payment "
        "(payment_id, created_at, last_updated, transaction_id, counterparty_id, "
        "payment_amount, currency_id, payment_type_id, paid, payment_date, "
        "company_ac_number, counterparty_ac_number) "
        "VALUES "
    )

    values = ", ".join(
        [
            (
                "("
                f"{literal(payment['payment_id'])}, "
                f"{literal(payment['created_at'])}, "
                f"{literal(payment['last_updated'])}, "
                f"{literal(payment['transaction_id'])}, "
                f"{literal(payment['counterparty_id'])}, "
                f"{literal(payment['payment_amount'])}, "
                f"{literal(payment['currency_id'])}, "
                f"{literal(payment['payment_type_id'])}, "
                f"{literal(payment['paid'])}, "
                f"{literal(payment['payment_date'])}, "
                f"{literal(payment['company_ac_number'])}, "
                f"{literal(payment['counterparty_ac_number'])})"
            )
            for payment in payments
        ]
    )

    query = start_of_query + values

    con.run(query)


if __name__ == "__main__":
    try:
        seed(
            addresses,
            counterparties,
            currencies,
            departments,
            designs,
            payment_types,
            payments,
            purchase_orders,
            sales_orders,
            staff,
            transactions,
        )

    except Exception as e:
        print(f"Error: {e}")

    finally:
        con.close()
