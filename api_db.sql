--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6
-- Dumped by pg_dump version 11.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: users; Type: TABLE; Schema: public; Owner: apiappuser
--

CREATE TABLE public.users (
    name text NOT NULL,
    dob date
);


ALTER TABLE public.users OWNER TO apiappuser;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: apiappuser
--

COPY public.users (name, dob) FROM stdin;
Alfred	1960-06-10
Jon	1980-10-15
Cersei	1970-05-26
Aria	1990-05-23
\.


--
-- Name: users firstkey; Type: CONSTRAINT; Schema: public; Owner: apiappuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT firstkey PRIMARY KEY (name);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: apiappuser
--

REVOKE ALL ON SCHEMA public FROM rdsadmin;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO apiappuser;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

