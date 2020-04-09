import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(dbname = 'encyclopedia', user='postgres', 
                        password='', host='127.0.0.1')
cursor = conn.cursor()

# cursor.execute('CREATE DATABASE encyclopedia')
cursor.execute('CREATE table IF NOT EXISTS world_areas (id serial PRIMARY KEY, name varchar(40) UNIQUE  NOT NULL, description text)')

cursor.execute('CREATE table IF NOT EXISTS countries (id serial PRIMARY KEY, name varchar(40) UNIQUE  NOT NULL, world_area_id integer NOT NULL, description text, FOREIGN KEY (world_area_id) REFERENCES world_areas (id) ON DELETE CASCADE);')

cursor.execute('CREATE table IF NOT EXISTS domains (id serial PRIMARY KEY, name varchar(40) UNIQUE  NOT NULL, description text NOT NULL)')

cursor.execute('CREATE table IF NOT EXISTS kinds (id serial PRIMARY KEY, name varchar(40) UNIQUE  NOT NULL, domain_id integer NOT NULL, description text, FOREIGN KEY(domain_id) REFERENCES domains (id) ON DELETE CASCADE);')

cursor.execute('CREATE table IF NOT EXISTS types (id serial PRIMARY KEY, name varchar(40) UNIQUE  NOT NULL, kind_id integer NOT NULL,  description text,  FOREIGN KEY(kind_id) REFERENCES kinds (id) ON DELETE CASCADE);')
cursor.execute('CREATE table IF NOT EXISTS sub_types (id serial PRIMARY KEY, name varchar(40) UNIQUE , description text);')
cursor.execute('CREATE table IF NOT EXISTS types_sub_types (type_id integer NOT NULL, sub_type_id integer NOT NULL, FOREIGN KEY (type_id) REFERENCES types (id) ON DELETE CASCADE, FOREIGN KEY (sub_type_id) REFERENCES sub_types (id) ON DELETE CASCADE);')

cursor.execute('CREATE table IF NOT EXISTS classes (id serial PRIMARY KEY, name varchar(40) UNIQUE , description text);')
cursor.execute('CREATE table IF NOT EXISTS sub_types_classes (sub_type_id integer NOT NULL, class_id integer NOT NULL, FOREIGN KEY (sub_type_id) REFERENCES sub_types (id) ON DELETE CASCADE, FOREIGN KEY (class_id) REFERENCES classes (id) ON DELETE CASCADE);')

cursor.execute('CREATE table IF NOT EXISTS sub_classes (id serial PRIMARY KEY, name varchar(40) UNIQUE , description text);')
cursor.execute('CREATE table IF NOT EXISTS classes_sub_classes (class_id integer NOT NULL, sub_class_id integer NOT NULL, FOREIGN KEY (class_id) REFERENCES classes (id) ON DELETE CASCADE, FOREIGN KEY (sub_class_id) REFERENCES sub_classes (id) ON DELETE CASCADE);')

cursor.execute('CREATE table IF NOT EXISTS ordos (id serial PRIMARY KEY, name varchar(40) UNIQUE , description text);')
cursor.execute('CREATE table IF NOT EXISTS sub_classes_ordos (sub_class_id integer, ordo_id integer, FOREIGN KEY (sub_class_id) REFERENCES sub_classes (id) ON DELETE CASCADE, FOREIGN KEY (ordo_id) REFERENCES ordos (id));')

cursor.execute('CREATE table IF NOT EXISTS familias (id serial PRIMARY KEY, name varchar(40) UNIQUE , description text);')
cursor.execute('CREATE table IF NOT EXISTS ordos_familias (ordo_id integer, familia_id integer, FOREIGN KEY (ordo_id) REFERENCES ordos (id) ON DELETE CASCADE, FOREIGN KEY (familia_id) REFERENCES familias (id))')

cursor.execute('CREATE table IF NOT EXISTS genuses (id serial PRIMARY KEY, name varchar(40) UNIQUE , description text);')
cursor.execute('CREATE table IF NOT EXISTS familias_genuses (familia_id integer, genus_id integer, FOREIGN KEY (familia_id) REFERENCES familias (id) ON DELETE CASCADE, FOREIGN KEY (genus_id) REFERENCES genuses (id) ON DELETE CASCADE);')

cursor.execute('CREATE table IF NOT EXISTS specieses (id serial PRIMARY KEY, name varchar(40) UNIQUE , image varchar(255) NOT NULL, description text);')
cursor.execute('CREATE table IF NOT EXISTS genuses_specieses (genus_id integer, species_id integer, FOREIGN KEY (genus_id) REFERENCES genuses (id) ON DELETE CASCADE, FOREIGN KEY (species_id) REFERENCES specieses (id) ON DELETE CASCADE);')

cursor.execute('CREATE table IF NOT EXISTS countries_specieses (country_id integer, species_id integer, FOREIGN KEY (country_id) REFERENCES countries (id) ON DELETE CASCADE, FOREIGN KEY (species_id) REFERENCES specieses (id) ON DELETE CASCADE);')


#FUNCTION
# cursor.execute("""
# CREATE FUNCTION world_area_delete(int id) RETURNS integer
#     AS 'select $1 + $2;'
#     LANGUAGE SQL
#     RETURNS NULL ON NULL INPUT;
#     """)

# TRIGGERS 
# cursor.execute(CREATE TRIGGER log_update
#     AFTER UPDATE ON accounts
#     FOR EACH ROW
#     WHEN (OLD.* IS DISTINCT FROM NEW.*)
#     EXECUTE PROCEDURE log_account_update();
# )



def check():
	count = 0
	s = ""
	s += "SELECT"
	s += " table_schema"
	s += ", table_name"
	s += " FROM information_schema.tables"
	s += " WHERE"
	s += " ("
	s += " table_schema = 'public'"
	s += " )"
	s += " ORDER BY table_schema, table_name;"
	cursor.execute(s)
	list_tables = cursor.fetchall()

	for t_name_table in list_tables:
	    print(t_name_table)
	    count += 1
	print(count)
check()
conn.commit()
cursor.close()
conn.close()
