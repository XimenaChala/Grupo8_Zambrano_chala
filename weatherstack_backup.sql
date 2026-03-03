--
-- PostgreSQL database dump
--

\restrict t3ymtn6Fqa62yfHvszjLMcaHCli49843Lbh8WcOjnS4ZYXF2H4Gd3SwecDN752v

-- Dumped from database version 15.17 (Debian 15.17-1.pgdg13+1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

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

SET default_table_access_method = heap;

--
-- Name: clima; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.clima (
    id integer NOT NULL,
    ciudad character varying(100),
    pais character varying(100),
    latitud double precision,
    longitud double precision,
    temperatura double precision,
    sensacion_termica double precision,
    humedad integer,
    velocidad_viento double precision,
    descripcion text,
    fecha_extraccion timestamp without time zone,
    codigo_tiempo integer
);


--
-- Name: clima_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.clima_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: clima_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.clima_id_seq OWNED BY public.clima.id;


--
-- Name: clima id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clima ALTER COLUMN id SET DEFAULT nextval('public.clima_id_seq'::regclass);


--
-- Data for Name: clima; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.clima (id, ciudad, pais, latitud, longitud, temperatura, sensacion_termica, humedad, velocidad_viento, descripcion, fecha_extraccion, codigo_tiempo) FROM stdin;
1	Bogota	Colombia	4.6	-74.083	18	18	73	7	Shower In Vicinity	2026-02-27 19:38:33.773036	122
2	Medellin	Colombia	6.291	-75.536	25	28	61	6	Partly cloudy	2026-02-27 19:38:36.71546	116
3	Cali	Colombia	3.437	-76.523	27	31	66	8	Partly cloudy	2026-02-27 19:38:39.472444	116
4	Barranquilla	Colombia	10.964	-74.796	28	33	79	29	Clear 	2026-02-27 19:38:42.448589	113
5	Cartagena	Colombia	10.4	-75.514	30	38	70	25	Clear 	2026-02-27 19:38:45.226074	113
6	Bogota	Colombia	4.6	-74.083	17	17	83	8	Partly cloudy	2026-03-02 19:43:16.64417	116
7	Medellin	Colombia	6.291	-75.536	24	27	69	5	Partly cloudy	2026-03-02 19:43:19.408571	116
8	Cali	Colombia	3.437	-76.523	27	32	66	7	Overcast	2026-03-02 19:43:22.172795	122
9	Barranquilla	Colombia	10.964	-74.796	28	33	74	38	Clear 	2026-03-02 19:43:25.960833	113
10	Cartagena	Colombia	10.4	-75.514	29	35	70	35	Partly cloudy	2026-03-02 19:43:28.622922	116
11	Bogota	Colombia	4.6	-74.083	17	17	83	8	Partly cloudy	2026-03-02 19:43:16.64417	116
12	Medellin	Colombia	6.291	-75.536	24	27	69	5	Partly cloudy	2026-03-02 19:43:19.408571	116
13	Cali	Colombia	3.437	-76.523	27	32	66	7	Overcast	2026-03-02 19:43:22.172795	122
14	Barranquilla	Colombia	10.964	-74.796	28	33	74	38	Clear 	2026-03-02 19:43:25.960833	113
15	Cartagena	Colombia	10.4	-75.514	29	35	70	35	Partly cloudy	2026-03-02 19:43:28.622922	116
16	Bogota	Colombia	4.6	-74.083	17	17	83	8	Partly cloudy	2026-03-02 19:43:16.64417	116
17	Medellin	Colombia	6.291	-75.536	24	27	69	5	Partly cloudy	2026-03-02 19:43:19.408571	116
18	Cali	Colombia	3.437	-76.523	27	32	66	7	Overcast	2026-03-02 19:43:22.172795	122
19	Barranquilla	Colombia	10.964	-74.796	28	33	74	38	Clear 	2026-03-02 19:43:25.960833	113
20	Cartagena	Colombia	10.4	-75.514	29	35	70	35	Partly cloudy	2026-03-02 19:43:28.622922	116
21	Bogota	Colombia	4.6	-74.083	17	17	83	8	Partly cloudy	2026-03-02 19:43:16.64417	116
22	Medellin	Colombia	6.291	-75.536	24	27	69	5	Partly cloudy	2026-03-02 19:43:19.408571	116
23	Cali	Colombia	3.437	-76.523	27	32	66	7	Overcast	2026-03-02 19:43:22.172795	122
24	Barranquilla	Colombia	10.964	-74.796	28	33	74	38	Clear 	2026-03-02 19:43:25.960833	113
25	Cartagena	Colombia	10.4	-75.514	29	35	70	35	Partly cloudy	2026-03-02 19:43:28.622922	116
\.


--
-- Name: clima_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.clima_id_seq', 25, true);


--
-- Name: clima clima_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clima
    ADD CONSTRAINT clima_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict t3ymtn6Fqa62yfHvszjLMcaHCli49843Lbh8WcOjnS4ZYXF2H4Gd3SwecDN752v

