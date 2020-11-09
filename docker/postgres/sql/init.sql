
CREATE SCHEMA myschema;

SET search_path TO myschema,public;

REVOKE CREATE ON SCHEMA public FROM PUBLIC;

CREATE ROLE db_admin LOGIN PASSWORD 'db_admin' NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
CREATE ROLE test_user LOGIN PASSWORD 'psswd' NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;

CREATE DATABASE movie_database with ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' CONNECTION LIMIT = -1 template=template0;
CREATE DATABASE test_db with ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' CONNECTION LIMIT = -1 template=template0;

ALTER DATABASE movie_database OWNER TO db_admin;

ALTER DATABASE movie_database SET timezone TO 'UTC';

ALTER DATABASE test_db OWNER TO test_user;

ALTER DATABASE test_db SET timezone TO 'UTC';

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

GRANT USAGE ON SCHEMA public to db_admin;
GRANT CREATE ON SCHEMA public to db_admin;

GRANT USAGE ON SCHEMA public to test_user;
GRANT CREATE ON SCHEMA public to test_user;