--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO peacecorpsuser;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO peacecorpsuser;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO peacecorpsuser;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO peacecorpsuser;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO peacecorpsuser;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO peacecorpsuser;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO peacecorpsuser;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO peacecorpsuser;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO peacecorpsuser;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO peacecorpsuser;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO peacecorpsuser;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO peacecorpsuser;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO peacecorpsuser;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO peacecorpsuser;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO peacecorpsuser;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO peacecorpsuser;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO peacecorpsuser;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO peacecorpsuser;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO peacecorpsuser;

--
-- Name: peacecorps_country; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE peacecorps_country (
    id integer NOT NULL,
    code character varying(5) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.peacecorps_country OWNER TO peacecorpsuser;

--
-- Name: peacecorps_country_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE peacecorps_country_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peacecorps_country_id_seq OWNER TO peacecorpsuser;

--
-- Name: peacecorps_country_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE peacecorps_country_id_seq OWNED BY peacecorps_country.id;


--
-- Name: peacecorps_countryfund; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE peacecorps_countryfund (
    id integer NOT NULL,
    fundcurrent integer,
    fundtotal integer,
    country_id integer NOT NULL
);


ALTER TABLE public.peacecorps_countryfund OWNER TO peacecorpsuser;

--
-- Name: peacecorps_countryfund_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE peacecorps_countryfund_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peacecorps_countryfund_id_seq OWNER TO peacecorpsuser;

--
-- Name: peacecorps_countryfund_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE peacecorps_countryfund_id_seq OWNED BY peacecorps_countryfund.id;


--
-- Name: peacecorps_featuredissue; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE peacecorps_featuredissue (
    id integer NOT NULL,
    issue_id integer NOT NULL
);


ALTER TABLE public.peacecorps_featuredissue OWNER TO peacecorpsuser;

--
-- Name: peacecorps_featuredcampaign_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE peacecorps_featuredcampaign_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peacecorps_featuredcampaign_id_seq OWNER TO peacecorpsuser;

--
-- Name: peacecorps_featuredcampaign_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE peacecorps_featuredcampaign_id_seq OWNED BY peacecorps_featuredissue.id;


--
-- Name: peacecorps_featuredprojectfrontpage; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE peacecorps_featuredprojectfrontpage (
    id integer NOT NULL,
    project_id integer NOT NULL
);


ALTER TABLE public.peacecorps_featuredprojectfrontpage OWNER TO peacecorpsuser;

--
-- Name: peacecorps_featuredprojectfrontpage_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE peacecorps_featuredprojectfrontpage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peacecorps_featuredprojectfrontpage_id_seq OWNER TO peacecorpsuser;

--
-- Name: peacecorps_featuredprojectfrontpage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE peacecorps_featuredprojectfrontpage_id_seq OWNED BY peacecorps_featuredprojectfrontpage.id;


--
-- Name: peacecorps_fund; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE peacecorps_fund (
    id integer NOT NULL,
    name character varying(120) NOT NULL,
    description text,
    fundcurrent integer,
    fundtotal integer,
    featured_image_id integer NOT NULL
);


ALTER TABLE public.peacecorps_fund OWNER TO peacecorpsuser;

--
-- Name: peacecorps_fund_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE peacecorps_fund_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peacecorps_fund_id_seq OWNER TO peacecorpsuser;

--
-- Name: peacecorps_fund_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE peacecorps_fund_id_seq OWNED BY peacecorps_fund.id;


--
-- Name: peacecorps_issue; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE peacecorps_issue (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    icon character varying(100),
    featured_image_id integer NOT NULL,
    fundcurrent integer,
    fundgoal integer,
    slug character varying(100) NOT NULL,
    tagline character varying(140) NOT NULL,
    call character varying(40) NOT NULL
);


ALTER TABLE public.peacecorps_issue OWNER TO peacecorpsuser;

--
-- Name: peacecorps_issue_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE peacecorps_issue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peacecorps_issue_id_seq OWNER TO peacecorpsuser;

--
-- Name: peacecorps_issue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE peacecorps_issue_id_seq OWNED BY peacecorps_issue.id;


--
-- Name: peacecorps_media; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE peacecorps_media (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    file character varying(100) NOT NULL,
    mediatype character varying(3) NOT NULL,
    caption text,
    author_id integer,
    country_id integer,
    description text NOT NULL,
    transcript text
);


ALTER TABLE public.peacecorps_media OWNER TO peacecorpsuser;

--
-- Name: peacecorps_media_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE peacecorps_media_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peacecorps_media_id_seq OWNER TO peacecorpsuser;

--
-- Name: peacecorps_media_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE peacecorps_media_id_seq OWNED BY peacecorps_media.id;


--
-- Name: peacecorps_project; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE peacecorps_project (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    volunteer_id integer NOT NULL,
    description text NOT NULL,
    country_id integer NOT NULL,
    issue_id integer NOT NULL,
    featured_image_id integer NOT NULL,
    fundcurrent integer,
    fundtotal integer,
    issue_feature boolean NOT NULL,
    slug character varying(100) NOT NULL,
    tagline character varying(240) NOT NULL
);


ALTER TABLE public.peacecorps_project OWNER TO peacecorpsuser;

--
-- Name: peacecorps_project_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE peacecorps_project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peacecorps_project_id_seq OWNER TO peacecorpsuser;

--
-- Name: peacecorps_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE peacecorps_project_id_seq OWNED BY peacecorps_project.id;


--
-- Name: peacecorps_project_issues_related; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE peacecorps_project_issues_related (
    id integer NOT NULL,
    project_id integer NOT NULL,
    issue_id integer NOT NULL
);


ALTER TABLE public.peacecorps_project_issues_related OWNER TO peacecorpsuser;

--
-- Name: peacecorps_project_issues_related_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE peacecorps_project_issues_related_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peacecorps_project_issues_related_id_seq OWNER TO peacecorpsuser;

--
-- Name: peacecorps_project_issues_related_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE peacecorps_project_issues_related_id_seq OWNED BY peacecorps_project_issues_related.id;


--
-- Name: peacecorps_project_media; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE peacecorps_project_media (
    id integer NOT NULL,
    project_id integer NOT NULL,
    media_id integer NOT NULL
);


ALTER TABLE public.peacecorps_project_media OWNER TO peacecorpsuser;

--
-- Name: peacecorps_project_media_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE peacecorps_project_media_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peacecorps_project_media_id_seq OWNER TO peacecorpsuser;

--
-- Name: peacecorps_project_media_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE peacecorps_project_media_id_seq OWNED BY peacecorps_project_media.id;


--
-- Name: peacecorps_volunteer; Type: TABLE; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE TABLE peacecorps_volunteer (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    pronouns character varying(2) NOT NULL,
    profile_image_id integer,
    homestate character varying(2),
    homecity character varying(120)
);


ALTER TABLE public.peacecorps_volunteer OWNER TO peacecorpsuser;

--
-- Name: peacecorps_volunteer_id_seq; Type: SEQUENCE; Schema: public; Owner: peacecorpsuser
--

CREATE SEQUENCE peacecorps_volunteer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peacecorps_volunteer_id_seq OWNER TO peacecorpsuser;

--
-- Name: peacecorps_volunteer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peacecorpsuser
--

ALTER SEQUENCE peacecorps_volunteer_id_seq OWNED BY peacecorps_volunteer.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_country ALTER COLUMN id SET DEFAULT nextval('peacecorps_country_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_countryfund ALTER COLUMN id SET DEFAULT nextval('peacecorps_countryfund_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_featuredissue ALTER COLUMN id SET DEFAULT nextval('peacecorps_featuredcampaign_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_featuredprojectfrontpage ALTER COLUMN id SET DEFAULT nextval('peacecorps_featuredprojectfrontpage_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_fund ALTER COLUMN id SET DEFAULT nextval('peacecorps_fund_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_issue ALTER COLUMN id SET DEFAULT nextval('peacecorps_issue_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_media ALTER COLUMN id SET DEFAULT nextval('peacecorps_media_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_project ALTER COLUMN id SET DEFAULT nextval('peacecorps_project_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_project_issues_related ALTER COLUMN id SET DEFAULT nextval('peacecorps_project_issues_related_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_project_media ALTER COLUMN id SET DEFAULT nextval('peacecorps_project_media_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_volunteer ALTER COLUMN id SET DEFAULT nextval('peacecorps_volunteer_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add country	7	add_country
20	Can change country	7	change_country
21	Can delete country	7	delete_country
25	Can add issue	9	add_issue
26	Can change issue	9	change_issue
27	Can delete issue	9	delete_issue
28	Can add media	10	add_media
29	Can change media	10	change_media
30	Can delete media	10	delete_media
31	Can add project	11	add_project
32	Can change project	11	change_project
33	Can delete project	11	delete_project
34	Can add volunteer	12	add_volunteer
35	Can change volunteer	12	change_volunteer
36	Can delete volunteer	12	delete_volunteer
37	Can add country fund	13	add_countryfund
38	Can change country fund	13	change_countryfund
39	Can delete country fund	13	delete_countryfund
40	Can add fund	14	add_fund
41	Can change fund	14	change_fund
42	Can delete fund	14	delete_fund
43	Can add featured issue	15	add_featuredissue
44	Can change featured issue	15	change_featuredissue
45	Can delete featured issue	15	delete_featuredissue
46	Can add featured project front page	16	add_featuredprojectfrontpage
47	Can change featured project front page	16	change_featuredprojectfrontpage
48	Can delete featured project front page	16	delete_featuredprojectfrontpage
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('auth_permission_id_seq', 48, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$12000$bRbG3bcaHDB5$3JztDFyXRsRdOJs9UuuF2Zn7Bt/BRbHp2Jv4skn8144=	2014-10-03 09:06:16.879111-04	t	annalee			anna.flowerhorne@gsa.gov	t	t	2014-09-28 21:24:33.281172-04
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2014-10-03 10:32:54.53002-04	1	Media object	1		10	1
2	2014-10-03 10:33:17.317266-04	1	Issue object	1		9	1
7	2014-10-03 14:25:48.083365-04	1	Volunteer object	1		12	1
8	2014-10-03 14:26:44.979165-04	2	Volunteer object	1		12	1
9	2014-10-03 14:30:02.9022-04	3	Miss Martian - Happy Harbor, RI	1		12	1
10	2014-10-03 14:34:51.342694-04	2	Colored Pencils	1		10	1
11	2014-10-03 14:34:54.527159-04	2	Women	1		9	1
12	2014-10-03 16:27:09.374689-04	3	Education	1		9	1
13	2014-10-03 16:27:49.429073-04	4	Hunger	1		9	1
14	2014-10-03 16:30:21.636846-04	3	Cat Smelling A Flower	1		10	1
15	2014-10-03 16:30:42.108644-04	5	Health	1		9	1
16	2014-10-03 16:33:11.794592-04	4	Industrial Sewing Machine	1		10	1
17	2014-10-03 16:33:14.016657-04	6	Housing	1		9	1
18	2014-10-03 19:01:11.930445-04	1	Women (Featured)	1		15	1
19	2014-10-03 19:17:42.99543-04	6	Housing	2	Changed slug.	9	1
20	2014-10-03 19:17:48.134131-04	5	Health	2	Changed slug.	9	1
21	2014-10-03 19:17:53.769678-04	4	Hunger	2	Changed slug.	9	1
22	2014-10-03 19:17:59.98797-04	3	Education	2	Changed slug.	9	1
23	2014-10-03 19:18:05.222976-04	2	Women	2	Changed slug.	9	1
24	2014-10-03 19:18:09.89754-04	1	Innovation	2	Changed slug.	9	1
25	2014-10-03 19:38:17.22502-04	2	Women	2	Changed call.	9	1
26	2014-10-03 19:45:25.067523-04	1	Project object	1		11	1
27	2014-10-03 19:46:54.202776-04	2	Project object	1		11	1
28	2014-10-03 19:48:08.771706-04	1	Send Gifted Girls To Superhero School	2	Changed featured_image.	11	1
29	2014-10-03 19:51:57.003699-04	4	Black Canary - Star City, MD	1		12	1
30	2014-10-03 19:54:33.05279-04	3	Teach Women How To Make Superhero Costumes	1		11	1
31	2014-10-03 19:54:39.567615-04	3	Teach Women How To Make Superhero Costumes	2	No fields changed.	11	1
32	2014-10-03 19:56:43.695161-04	2	Send Gifted Girls To Superhero School (Featured)	1		16	1
33	2014-10-03 19:56:49.310437-04	3	Build A Women's Health Center (Featured)	1		16	1
34	2014-10-03 20:34:43.335879-04	3	Teach Women How To Make Superhero Costumes	2	Changed tagline and issues_related.	11	1
35	2014-10-03 20:34:56.819631-04	2	Build A Women's Health Center	2	Changed tagline.	11	1
36	2014-10-03 20:35:17.591961-04	1	Send Gifted Girls To Superhero School	2	Changed tagline.	11	1
37	2014-10-03 20:43:07.800529-04	6	Housing	2	Changed icon.	9	1
38	2014-10-03 20:43:16.894409-04	5	Health	2	Changed icon.	9	1
39	2014-10-03 20:43:30.163938-04	4	Hunger	2	Changed icon.	9	1
40	2014-10-03 20:43:38.160466-04	3	Education	2	Changed icon.	9	1
41	2014-10-03 20:43:46.384518-04	2	Women	2	Changed icon.	9	1
42	2014-10-03 20:43:54.097633-04	1	Innovation	2	Changed icon.	9	1
43	2014-10-03 20:52:43.039625-04	6	Housing	2	Changed fundcurrent and fundgoal.	9	1
44	2014-10-03 20:52:57.417523-04	5	Health	2	Changed fundcurrent and fundgoal.	9	1
45	2014-10-03 20:53:13.103627-04	4	Hunger	2	Changed fundcurrent and fundgoal.	9	1
46	2014-10-03 20:53:40.519179-04	3	Education	2	Changed fundcurrent and fundgoal.	9	1
47	2014-10-03 20:53:58.55937-04	2	Women	2	Changed fundcurrent and fundgoal.	9	1
48	2014-10-03 20:54:23.179226-04	1	Innovation	2	Changed fundcurrent and fundgoal.	9	1
49	2014-10-03 20:56:37.282254-04	4	Hunger	2	Changed tagline and call.	9	1
50	2014-10-03 20:57:23.026628-04	5	Health	2	Changed tagline and call.	9	1
51	2014-10-03 20:59:35.271579-04	6	Housing	2	Changed tagline and call.	9	1
52	2014-10-03 20:59:47.575412-04	3	Teach Women How To Make Superhero Costumes	2	No fields changed.	11	1
53	2014-10-03 20:59:55.109081-04	2	Build A Women's Health Center	2	Changed fundtotal.	11	1
54	2014-10-03 21:00:02.303245-04	1	Send Gifted Girls To Superhero School	2	Changed fundtotal.	11	1
55	2014-10-03 21:09:50.179101-04	1	Send Gifted Girls To Superhero School	2	Changed description.	11	1
56	2014-10-03 21:10:10.296551-04	3	Teach Women How To Make Superhero Costumes	2	Changed description.	11	1
57	2014-10-03 21:10:34.274242-04	2	Build A Women's Health Center	2	Changed description.	11	1
58	2014-10-03 21:14:49.651627-04	2	Build A Women's Health Center	2	Changed fundcurrent and fundtotal.	11	1
59	2014-10-03 21:25:58.635526-04	5	Cherry Blossoms	1		10	1
60	2014-10-03 21:26:55.777603-04	4	Apprehend the Joker	1		11	1
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 60, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	log entry	admin	logentry
2	permission	auth	permission
3	group	auth	group
4	user	auth	user
5	content type	contenttypes	contenttype
6	session	sessions	session
7	country	peacecorps	country
9	issue	peacecorps	issue
10	media	peacecorps	media
11	project	peacecorps	project
12	volunteer	peacecorps	volunteer
13	country fund	peacecorps	countryfund
14	fund	peacecorps	fund
15	featured issue	peacecorps	featuredissue
16	featured project front page	peacecorps	featuredprojectfrontpage
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('django_content_type_id_seq', 16, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2014-09-28 21:23:51.080298-04
2	auth	0001_initial	2014-09-28 21:23:51.136445-04
3	admin	0001_initial	2014-09-28 21:23:51.168316-04
4	sessions	0001_initial	2014-09-28 21:23:51.178269-04
5	peacecorps	0001_initial	2014-10-03 10:19:41.216428-04
6	peacecorps	0002_auto_20141003_2022	2014-10-03 16:23:01.117643-04
7	peacecorps	0003_auto_20141003_2259	2014-10-03 18:59:28.576125-04
8	peacecorps	0004_issue_slug	2014-10-03 19:17:13.549575-04
9	peacecorps	0005_auto_20141003_2318	2014-10-03 19:18:36.646688-04
10	peacecorps	0006_project_slug	2014-10-03 19:29:12.997044-04
11	peacecorps	0007_auto_20141003_2330	2014-10-03 19:30:31.811333-04
12	peacecorps	0008_issue_tagline	2014-10-03 19:33:57.162116-04
13	peacecorps	0009_auto_20141003_2337	2014-10-03 19:37:16.840373-04
14	peacecorps	0010_auto_20141003_2345	2014-10-03 19:45:16.60184-04
15	peacecorps	0011_auto_20141004_0030	2014-10-03 20:30:26.48597-04
16	peacecorps	0012_auto_20141004_0052	2014-10-03 20:52:15.371189-04
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('django_migrations_id_seq', 16, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
ak3rohqnlb4x8m38hm3h5mjctg9ezvtx	Y2M5NTU2MDI0YmU1ZmE2ZWY3Yjc2NDhiYzdhNzg0NzIwYjQ1YTFkYTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOTM3NWFmZjY3ZTQxMGQwZWU4YTY0ZDIxY2RhMzAyYTY5YzQxZDMyZiIsIl9hdXRoX3VzZXJfaWQiOjF9	2014-10-17 09:06:16.882621-04
\.


--
-- Data for Name: peacecorps_country; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY peacecorps_country (id, code, name) FROM stdin;
1	USA	United States
2	AFG	Afghanistan
3	ALB	Albania
4	ALG	Algeria
5	AND	Andorra
6	ANG	Angola
7	ANT	Antigua and Barbuda
8	ARG	Argentina
9	ARM	Armenia
10	AUS	Australia
11	AUT	Austria
12	AZE	Azerbaijan
13	BAH	Bahamas
14	BAI	Bahrain
15	BAN	Bangladesh
16	BAR	Barbados
17	BES	Belarus
18	BEL	Belgium
19	BEM	Belize
20	BEN	Benin
21	BHU	Bhutan
22	BOL	Bolivia
23	BOS	Bosnia and Herzegovina
24	BOT	Botswana
25	BRA	Brazil
26	BRU	Brunei
27	BUL	Bulgaria
28	BUK	Burkina Faso
29	BUR	Burma
30	BUU	Burundi
31	CAN	Canada
32	CAB	Cambodia
33	CAM	Cameroon
34	CAP	Cape Verde
35	CAE	Central African Republic
36	CHA	Chad
37	CHL	Chile
38	CHN	China
39	COL	Colombia
40	COM	Comoros
41	RCB	Congo Brazzaville
42	CON	Congo Kinshasa
43	COS	Costa Rica
44	IVO	Cote D&#39; Ivoire
45	CRO	Croatia
46	CYP	Cyprus
47	CZE	Czech Republic
48	DEN	Denmark
49	DJI	Djibouti
50	DON	Dominica
51	DOM	Dominican Republic
52	ETM	East Timor
53	ECU	Ecuador
54	EGY	Egypt
55	ELS	El Salvador
56	EQU	Equatorial Guinea
57	ERI	Eritrea
58	EST	Estonia
59	ETH	Ethiopia
60	FIJ	Fiji
61	FIN	Finland
62	FRA	France
63	GAB	Gabon
64	GEO	Georgia
65	GER	Germany
66	GHA	Ghana
67	GRE	Greece
68	GRN	Grenada
69	GUA	Guatemala
70	GUI	Guinea
71	GUU	Guinea-Bissau
72	GUY	Guyana
73	HAI	Haiti
74	VAT	Holy See
75	HND	Honduras
76	HUN	Hungary
77	ICE	Iceland
78	IND	India
79	INS	Indonesia
80	IRC	Iraq
81	IRE	Ireland
82	ISR	Israel
83	ITA	Italy
84	JAM	Jamaica
85	JPN	Japan
86	JOR	Jordan
87	KAZ	Kazakhstan
88	KEN	Kenya
89	KIR	Kiribati
90	KUW	Kuwait
91	KYR	Kyrgyzstan
92	LAS	Laos
93	LAT	Latvia
94	LEB	Lebanon
95	LES	Lesotho
96	LIB	Liberia
97	LIY	Libya
98	LIE	Liechtenstein
99	LIT	Lithuania
100	LUX	Luxembourg
101	MAE	Macedonia
102	MDG	Madagascar
103	MAI	Malawi
104	MAL	Malaysia
105	MAM	Maldives
106	MAN	Mali
107	MAT	Malta
108	MHL	Marshall Islands
109	MAU	Mauritania
110	MAV	Mauritius
111	MEX	Mexico
112	FSM	Micronesia
113	MOL	Moldova
114	MOC	Monaco
115	MNE	Montenegro
116	MON	Mongolia
117	MOR	Morocco
118	MOZ	Mozambique
119	NAM	Namibia
120	NAU	Nauru
121	NEP	Nepal
122	NEA	Netherlands Antilles
123	NET	Netherlands
124	NEW	New Zealand
125	NIC	Nicaragua
126	NIE	Niger
127	NIG	Nigeria
128	NKO	North Korea
129	NOR	Norway
130	OMA	Oman
131	PAK	Pakistan
132	PLW	Palau
133	PAN	Panama
134	PAP	Papua New Guinea
135	PAR	Paraguay
136	PER	Peru
137	PHI	Philippines
138	POL	Poland
139	POR	Portugal
140	QAT	Qatar
141	ROM	Romania
142	RUS	Russia
143	RWA	Rwanda
144	SKA	Saint Kitts and Nevis
145	SLU	Saint Lucia
146	STV	Saint Vincent and the Grenadines
147	WSM	Samoa
148	SMA	San Marino
149	SAO	Sao Tome Principe
150	SAU	Saudi Arabia
151	SEN	Senegal
152	SER	Serbia
153	SEY	Seychelles
154	SIE	Sierra Leone
155	SIN	Singapore
156	SLA	Slovakia
157	SLO	Slovenia
158	SOL	Solomon Islands
159	SOM	Somalia
160	SOR	South Africa
161	SKO	South Korea
162	SPA	Spain
163	SRI	Sri Lanka
164	SUR	Suriname
165	SWA	Swaziland
166	SWE	Sweden
167	SWI	Switzerland
168	SYR	Syria
169	TAJ	Tajikistan
170	TAN	Tanzania
171	THA	Thailand
172	TOG	Togo
173	TON	Tonga
174	TRI	Trinidad and Tobago
175	TUN	Tunisia
176	TUR	Turkey
177	TUM	Turkmenistan
178	TUV	Tuvalo
179	UGA	Uganda
180	UKR	Ukraine
181	UAE	United Arab Emirates
182	GBR	United Kingdom
183	URN	Uruguay
184	UZB	Uzbekistan
185	VAN	Vanuatu
186	VEN	Venezuela
187	VIE	Vietnam
188	YEM	Yemen
189	ZAM	Zambia
190	ZIM	Zimbabwe
\.


--
-- Name: peacecorps_country_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('peacecorps_country_id_seq', 190, true);


--
-- Data for Name: peacecorps_countryfund; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY peacecorps_countryfund (id, fundcurrent, fundtotal, country_id) FROM stdin;
\.


--
-- Name: peacecorps_countryfund_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('peacecorps_countryfund_id_seq', 1, false);


--
-- Name: peacecorps_featuredcampaign_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('peacecorps_featuredcampaign_id_seq', 2, true);


--
-- Data for Name: peacecorps_featuredissue; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY peacecorps_featuredissue (id, issue_id) FROM stdin;
1	2
\.


--
-- Data for Name: peacecorps_featuredprojectfrontpage; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY peacecorps_featuredprojectfrontpage (id, project_id) FROM stdin;
2	1
3	2
\.


--
-- Name: peacecorps_featuredprojectfrontpage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('peacecorps_featuredprojectfrontpage_id_seq', 3, true);


--
-- Data for Name: peacecorps_fund; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY peacecorps_fund (id, name, description, fundcurrent, fundtotal, featured_image_id) FROM stdin;
\.


--
-- Name: peacecorps_fund_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('peacecorps_fund_id_seq', 1, false);


--
-- Data for Name: peacecorps_issue; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY peacecorps_issue (id, name, description, icon, featured_image_id, fundcurrent, fundgoal, slug, tagline, call) FROM stdin;
3	Education	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam lacinia metus metus, a finibus libero imperdiet eu. Mauris at laoreet felis, vel condimentum leo. Nam eu cursus nisi, eget egestas massa. Nam commodo turpis ac mollis pulvinar. Phasellus eu eleifend lacus. Integer posuere, est non aliquet pharetra, eros ligula ultricies dolor, non efficitur sem ipsum eu orci. Curabitur finibus nulla at dui consequat pellentesque. Nullam euismod odio eros, vehicula vestibulum velit finibus ac. Vestibulum ut dui arcu. Nullam ac est elit. Duis maximus pulvinar urna ut iaculis.	./house_SO2rcUg.png	2	30000	100000	education	Two out of three illiterate people are women.	donate to girl's education.
2	Women	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce quis eros eleifend nunc lobortis eleifend. Aliquam id nisi id dui egestas faucibus et id mauris. Cras posuere eu dolor ac dignissim. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Vivamus id nisi faucibus, pulvinar risus a, finibus lacus. Nullam porttitor elit vitae pellentesque placerat. Phasellus in auctor enim. Nulla facilisi.	./peopleicon_QK6SN51.png	2	260000	300000	women	Two out of three illiterate people are women.	Donate to girls' education
1	Innovation	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc sagittis libero diam, vitae cursus odio aliquam at. Sed convallis volutpat libero nec ultricies. Nulla blandit diam vel ex vestibulum, in sollicitudin justo convallis. Ut lobortis commodo luctus. Sed molestie lectus a ex gravida, eu tincidunt lorem molestie. Proin efficitur urna id massa cursus condimentum. Donec laoreet, quam a interdum semper, neque lorem pulvinar velit, eget pellentesque leo elit sit amet lorem. Duis commodo tortor quis velit euismod, sit amet tristique tortor bibendum.	./lightbulb.png	1	7200	50000	innovation	Two out of three illiterate people are women.	donate to girl's education.
4	Hunger	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vel mi ex. Cras pellentesque pulvinar pulvinar. Sed consequat varius sem quis volutpat. Fusce aliquet velit quis dignissim commodo. Praesent pretium dictum velit vitae ultricies. Donec eget tortor ut tellus bibendum pharetra quis mattis risus. Morbi non convallis ligula. Curabitur vel finibus ipsum, sit amet sagittis turpis.	./globeicon.png	1	50000	130000	hunger	925 million people do not have enough to eat.	Donate to world hunger.
5	Health	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque suscipit efficitur orci, ut pellentesque nisi tempor at. Phasellus tincidunt quis tellus ut facilisis. Morbi eu risus ultricies, cursus nunc vitae, euismod mauris. Nunc finibus nisi a dolor luctus, at suscipit diam rutrum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas feugiat feugiat ullamcorper. Phasellus ut enim nisl. Etiam porta vulputate metus, eget accumsan nunc maximus sit amet. Donec molestie pharetra ultricies. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Praesent sed semper turpis. Integer scelerisque congue arcu non molestie.	./peopleicon.png	3	1000	100000	health	925 million people do not have enough to eat	donate to world health
6	Housing	Vivamus sit amet magna id purus aliquet sodales. Mauris porttitor lacus neque, pellentesque rutrum est scelerisque egestas. Curabitur tempus justo justo, ac egestas purus consequat eu. Nunc risus leo, interdum ac lacus id, malesuada consequat risus. Integer porttitor, eros aliquam bibendum sollicitudin, ante ipsum molestie ipsum, consequat imperdiet lacus nibh ut lorem. Suspendisse mollis ex justo, a aliquam purus sagittis sed. Pellentesque purus enim, viverra vitae aliquet a, elementum non augue. Curabitur sed diam libero. Mauris pellentesque luctus accumsan. Nulla nunc est, egestas a feugiat blandit, congue eu mauris. Nam ornare commodo magna quis mollis. Sed blandit in est ut eleifend. Sed in vehicula lorem, ac consectetur eros. Sed sagittis ligula ipsum, vel tempus ante laoreet eu. In malesuada hendrerit vehicula.	./house.png	4	150000	240000	housing	Sub-Saharan Africa today has a slum population of 199.5 million representing 61.7 percent of its urban population.	Donate to safe housing for all.
\.


--
-- Name: peacecorps_issue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('peacecorps_issue_id_seq', 6, true);


--
-- Data for Name: peacecorps_media; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY peacecorps_media (id, title, file, mediatype, caption, author_id, country_id, description, transcript) FROM stdin;
1	Sewing Machine	./sewing-machine-flickr-usr-82473742N02.jpg	IMG	A treadle-powered Singer sewing machine.	\N	\N	A treadle-powered Singer sewing machine.	
2	Colored Pencils	./colored_pencils_2-wallpaper-2560x1600.jpg	IMG	Colored Pencils.	3	1	A group of colored pencils.	
3	Cat Smelling A Flower	./cat_smelling_flower-wallpaper-2560x1600.jpg	IMG	Photo courtesy Batgirl.	1	1	A cat smelling a flower.	
4	Industrial Sewing Machine	./sewing-machine-flickr-usr-chiotsrun.jpg	IMG	Sewing Machine, by flickr user Chiotsrun	\N	25	A picture of an old industrial sewing machine.	
5	Cherry Blossoms	./cherry_blossom_3-wallpaper-2560x1600.jpg	IMG	Cherry Blossom Wallpaper	2	1	A photo of cherry blossoms on a branch.	
\.


--
-- Name: peacecorps_media_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('peacecorps_media_id_seq', 5, true);


--
-- Data for Name: peacecorps_project; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY peacecorps_project (id, title, volunteer_id, description, country_id, issue_id, featured_image_id, fundcurrent, fundtotal, issue_feature, slug, tagline) FROM stdin;
3	Teach Women How To Make Superhero Costumes	4	<p>Curabitur pulvinar, ex eget cursus lacinia, lectus magna porttitor eros, sed tempus elit dolor et ipsum. Sed vel consequat magna, non dapibus urna. Praesent scelerisque justo ac velit malesuada, non euismod dui mollis. Nam neque turpis, tempor quis odio ac, lacinia faucibus felis. Nunc efficitur nisi augue, vitae lacinia sem pulvinar non. Nam sed nisi sed nisl blandit luctus. Nam lorem mi, accumsan mattis rhoncus sit amet, vulputate vitae enim. Etiam egestas egestas elementum. Sed fermentum pharetra mattis. Aenean pellentesque id ligula vitae maximus.\r\n</p><p>\r\nClass aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aenean id mi vel est fringilla laoreet. Morbi mattis hendrerit enim vitae scelerisque. Suspendisse potenti. Nulla purus ipsum, aliquam pulvinar leo et, egestas auctor lorem. Quisque sapien est, auctor pharetra luctus a, viverra porta sapien. Pellentesque ut libero sed diam rhoncus ultrices vel vitae massa. Donec dui urna, elementum et cursus sit amet, posuere id purus. Quisque tristique turpis eu tellus commodo, nec dictum mi sollicitudin. Pellentesque sit amet posuere magna. Integer consectetur tempus lorem, eu mollis augue aliquet a. Proin malesuada orci eu neque aliquam, nec lacinia tellus blandit. Pellentesque ac mauris quis nulla malesuada finibus non quis sapien.\r\n</p><p>\r\nInteger eget nisi sed felis finibus vulputate. Pellentesque elementum porttitor lorem, non ultricies risus tincidunt vel. Morbi hendrerit mauris posuere, imperdiet urna at, euismod tortor. Sed eget sapien volutpat purus mollis semper. Etiam varius quis mauris eu ornare. Donec ultricies pulvinar lacus at tincidunt. Nulla sagittis leo quis finibus congue. Mauris suscipit, augue sed pharetra luctus, arcu purus ultricies nulla, sed sodales orci elit vitae nibh. Proin eleifend vulputate laoreet. Aenean at mi tempor, ullamcorper massa ut, laoreet erat. Nulla pharetra nulla mi, vitae lacinia eros varius eu. Cras consequat ante id mi consectetur vestibulum. In urna lectus, malesuada et gravida sit amet, suscipit ac libero. Vestibulum feugiat consequat cursus.\r\n</p>	25	2	1	0	1000	f	superhero-costumes	Women need superhero costumes to fight crime.
1	Send Gifted Girls To Superhero School	2	<p>Nam in lobortis erat, non fringilla lectus. Donec et turpis id justo rhoncus ultrices. Vestibulum id tincidunt nulla. Nullam condimentum interdum lobortis. Fusce tempus quis augue eget pretium. Proin neque nunc, volutpat eget laoreet ut, posuere non felis. Aliquam erat volutpat. Vestibulum id neque at odio venenatis gravida at in ligula. Pellentesque et urna ante. Nam pretium ipsum sit amet nunc maximus, nec finibus erat dignissim. Mauris mollis, orci at semper rutrum, nibh diam maximus turpis, quis imperdiet justo augue nec ipsum. Nunc sagittis maximus aliquet. Mauris lorem lectus, rutrum vel aliquam et, feugiat eget metus. In velit enim, convallis at tempus ac, feugiat non quam. Integer mattis odio in eros maximus, consectetur ultrices lectus tristique.\r\n</p><p>\r\nVestibulum faucibus finibus ipsum sit amet congue. Suspendisse facilisis mauris non varius ultrices. Proin viverra, nibh at bibendum tristique, tortor sapien placerat nibh, quis hendrerit velit sapien sed dolor. Proin convallis tincidunt dolor nec cursus. Vivamus ac risus quis lectus mollis pellentesque. Nulla tristique libero nec quam egestas pulvinar. Phasellus vulputate arcu at eros lobortis tempus. Curabitur laoreet ligula ut tellus ornare dignissim. Ut finibus purus vel sapien eleifend cursus. Nunc nec maximus tortor, ac sagittis est. Nullam ut tortor dapibus nibh mattis pretium ut quis lorem. Pellentesque in nulla ut magna accumsan fermentum. Integer pellentesque diam sem, vel placerat erat vulputate sit amet. Sed vestibulum risus quis arcu mollis, ac iaculis lectus interdum. In dui mi, facilisis sit amet malesuada non, tempus suscipit ante.\r\n</p><p>\r\nCras eu metus lacus. Quisque ultrices dolor massa, ac commodo elit rutrum eu. Praesent in facilisis leo, eget dapibus mauris. Vivamus porta posuere purus, sed vestibulum tortor fringilla commodo. Interdum et malesuada fames ac ante ipsum primis in faucibus. Mauris fringilla, felis nec volutpat maximus, mi nibh vulputate mauris, ut egestas mauris lacus in nibh. Praesent ut eleifend urna. Sed porta risus hendrerit finibus semper.\r\n</p><p>\r\nDonec suscipit urna sem, ac pretium lacus egestas nec. Nulla facilisi. Cras sagittis nisi a justo aliquet venenatis. Cras non enim pretium, hendrerit dui id, tempor orci. Vivamus eu augue sapien. Donec aliquam lacus et magna suscipit, quis dictum urna egestas. Quisque nec massa vitae ex consequat fermentum. Suspendisse potenti. Aenean gravida, mi quis mollis ultrices, elit massa efficitur lacus, ac vehicula justo massa eget lectus. Quisque hendrerit justo nec metus eleifend, sit amet venenatis purus tempus. Proin eros ante, fringilla nec mi sed, vehicula rhoncus ligula. In porta hendrerit nisi sed euismod. Ut vitae auctor tellus, vel tristique ante.</p>	1	2	2	0	1000	t	gifted-girls-superhero-school	Superhero school is expensive. Everyone should have a chance to join the justice league.
2	Build A Women's Health Center	1	<p>Integer elementum ex id lobortis ultricies. Quisque in lorem commodo enim tincidunt vestibulum et eu nulla. Curabitur sit amet mauris lacinia, ornare dui id, pretium sapien. Donec suscipit eros vitae leo consectetur iaculis. Aliquam posuere, dolor ut tincidunt pellentesque, nulla orci porttitor ipsum, id fermentum nisi leo cursus risus. Etiam tempor, erat eu pretium rutrum, eros lorem egestas diam, id aliquam lectus turpis eu orci. Donec nec mauris nec lectus tincidunt finibus ac ut purus. Maecenas bibendum, tortor nec porta blandit, ex erat imperdiet diam, nec laoreet mi nibh ut ipsum. Sed fermentum porttitor massa, et imperdiet erat viverra et. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Proin sit amet urna vitae felis consequat bibendum vel at risus. In diam metus, dapibus varius nisi ac, malesuada ornare neque. Duis sed fermentum tellus, non dapibus elit.\r\n</p><p>\r\nNulla elementum porttitor metus, eu malesuada est pulvinar eget. Aliquam odio lacus, lacinia sit amet nibh et, congue convallis dui. Praesent et ipsum sem. Proin eu molestie lacus. Mauris vel sem a odio lobortis condimentum eget consequat tellus. Nunc at magna lacus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Proin non vestibulum felis, in suscipit nibh. Etiam bibendum tortor nec volutpat ornare.\r\n</p><p>\r\nNullam lobortis egestas lectus, nec ullamcorper libero feugiat sed. Ut sit amet sagittis orci. Ut nec magna vitae justo imperdiet luctus. Duis vel placerat mauris. Sed convallis leo sit amet elit faucibus maximus. Nunc ornare risus ac posuere laoreet. Fusce ex erat, convallis nec hendrerit sit amet, gravida non nunc. Aenean quis tortor et erat vehicula suscipit. In libero elit, pellentesque nec vestibulum nec, ultricies id mi. Donec in metus nisl. Nam dapibus ut nisl vel sagittis. In efficitur elit sed nunc aliquet sagittis. Nullam vestibulum congue turpis sit amet lacinia.\r\n</p><p>\r\nIn hac habitasse platea dictumst. Vivamus in elit nec ipsum accumsan egestas quis vitae lorem. Aliquam id risus nisl. Nulla accumsan velit sit amet ullamcorper scelerisque. Vivamus ac rutrum nibh. Pellentesque lobortis sit amet quam vel suscipit. Aenean lobortis, massa ac aliquet fermentum, neque elit volutpat mi, viverra faucibus nulla ante nec tellus. Donec venenatis in diam ut lobortis. Fusce maximus porta metus, eu efficitur ipsum. Nunc bibendum tincidunt arcu, a dignissim massa accumsan ut. Pellentesque ac nunc vitae est dignissim lobortis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.</p>	25	2	3	1000000	1000000	t	womens-heath-center	Integer elementum ex id lobortis ultricies. 
4	Apprehend the Joker	1	Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aenean id mi vel est fringilla laoreet. Morbi mattis hendrerit enim vitae scelerisque. Suspendisse potenti. Nulla purus ipsum, aliquam pulvinar leo et, egestas auctor lorem. Quisque sapien est, auctor pharetra luctus a, viverra porta sapien. Pellentesque ut libero sed diam rhoncus ultrices vel vitae massa. Donec dui urna, elementum et cursus sit amet, posuere id purus. Quisque tristique turpis eu tellus commodo, nec dictum mi sollicitudin. Pellentesque sit amet posuere magna. Integer consectetur tempus lorem, eu mollis augue aliquet a. Proin malesuada orci eu neque aliquam, nec lacinia tellus blandit. Pellentesque ac mauris quis nulla malesuada finibus non quis sapien.\r\n\r\nInteger eget nisi sed felis finibus vulputate. Pellentesque elementum porttitor lorem, non ultricies risus tincidunt vel. Morbi hendrerit mauris posuere, imperdiet urna at, euismod tortor. Sed eget sapien volutpat purus mollis semper. Etiam varius quis mauris eu ornare. Donec ultricies pulvinar lacus at tincidunt. Nulla sagittis leo quis finibus congue. Mauris suscipit, augue sed pharetra luctus, arcu purus ultricies nulla, sed sodales orci elit vitae nibh. Proin eleifend vulputate laoreet. Aenean at mi tempor, ullamcorper massa ut, laoreet erat. Nulla pharetra nulla mi, vitae lacinia eros varius eu. Cras consequat ante id mi consectetur vestibulum. In urna lectus, malesuada et gravida sit amet, suscipit ac libero. Vestibulum feugiat consequat cursus.	1	5	5	0	10000	f	catch-the-joker	He's running loose on the mean streets of Gotham
\.


--
-- Name: peacecorps_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('peacecorps_project_id_seq', 4, true);


--
-- Data for Name: peacecorps_project_issues_related; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY peacecorps_project_issues_related (id, project_id, issue_id) FROM stdin;
14	1	3
15	3	3
17	2	5
18	4	2
19	4	3
\.


--
-- Name: peacecorps_project_issues_related_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('peacecorps_project_issues_related_id_seq', 19, true);


--
-- Data for Name: peacecorps_project_media; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY peacecorps_project_media (id, project_id, media_id) FROM stdin;
\.


--
-- Name: peacecorps_project_media_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('peacecorps_project_media_id_seq', 1, false);


--
-- Data for Name: peacecorps_volunteer; Type: TABLE DATA; Schema: public; Owner: peacecorpsuser
--

COPY peacecorps_volunteer (id, name, pronouns, profile_image_id, homestate, homecity) FROM stdin;
1	Batgirl	T	\N	NY	Gotham
2	Wonder Woman	S	\N	VI	Themyscira
3	Miss Martian	S	\N	RI	Happy Harbor
4	Black Canary	S	\N	MD	Star City
\.


--
-- Name: peacecorps_volunteer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: peacecorpsuser
--

SELECT pg_catalog.setval('peacecorps_volunteer_id_seq', 4, true);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_63b55430ec14252c_uniq; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_63b55430ec14252c_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: peacecorps_country_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_country
    ADD CONSTRAINT peacecorps_country_pkey PRIMARY KEY (id);


--
-- Name: peacecorps_countryfund_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_countryfund
    ADD CONSTRAINT peacecorps_countryfund_pkey PRIMARY KEY (id);


--
-- Name: peacecorps_featuredcampaign_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_featuredissue
    ADD CONSTRAINT peacecorps_featuredcampaign_pkey PRIMARY KEY (id);


--
-- Name: peacecorps_featuredprojectfrontpage_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_featuredprojectfrontpage
    ADD CONSTRAINT peacecorps_featuredprojectfrontpage_pkey PRIMARY KEY (id);


--
-- Name: peacecorps_fund_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_fund
    ADD CONSTRAINT peacecorps_fund_pkey PRIMARY KEY (id);


--
-- Name: peacecorps_issue_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_issue
    ADD CONSTRAINT peacecorps_issue_pkey PRIMARY KEY (id);


--
-- Name: peacecorps_issue_slug_key; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_issue
    ADD CONSTRAINT peacecorps_issue_slug_key UNIQUE (slug);


--
-- Name: peacecorps_media_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_media
    ADD CONSTRAINT peacecorps_media_pkey PRIMARY KEY (id);


--
-- Name: peacecorps_project_issues_related_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_project_issues_related
    ADD CONSTRAINT peacecorps_project_issues_related_pkey PRIMARY KEY (id);


--
-- Name: peacecorps_project_issues_related_project_id_issue_id_key; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_project_issues_related
    ADD CONSTRAINT peacecorps_project_issues_related_project_id_issue_id_key UNIQUE (project_id, issue_id);


--
-- Name: peacecorps_project_media_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_project_media
    ADD CONSTRAINT peacecorps_project_media_pkey PRIMARY KEY (id);


--
-- Name: peacecorps_project_media_project_id_media_id_key; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_project_media
    ADD CONSTRAINT peacecorps_project_media_project_id_media_id_key UNIQUE (project_id, media_id);


--
-- Name: peacecorps_project_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_project
    ADD CONSTRAINT peacecorps_project_pkey PRIMARY KEY (id);


--
-- Name: peacecorps_volunteer_pkey; Type: CONSTRAINT; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

ALTER TABLE ONLY peacecorps_volunteer
    ADD CONSTRAINT peacecorps_volunteer_pkey PRIMARY KEY (id);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: peacecorps_countryfund_93bfec8a; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_countryfund_93bfec8a ON peacecorps_countryfund USING btree (country_id);


--
-- Name: peacecorps_featuredcampaign_issue_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_featuredcampaign_issue_id ON peacecorps_featuredissue USING btree (issue_id);


--
-- Name: peacecorps_featuredprojectfrontpage_b098ad43; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_featuredprojectfrontpage_b098ad43 ON peacecorps_featuredprojectfrontpage USING btree (project_id);


--
-- Name: peacecorps_fund_cdbc3e64; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_fund_cdbc3e64 ON peacecorps_fund USING btree (featured_image_id);


--
-- Name: peacecorps_issue_featured_image_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_issue_featured_image_id ON peacecorps_issue USING btree (featured_image_id);


--
-- Name: peacecorps_media_author_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_media_author_id ON peacecorps_media USING btree (author_id);


--
-- Name: peacecorps_media_country_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_media_country_id ON peacecorps_media USING btree (country_id);


--
-- Name: peacecorps_project_country_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_project_country_id ON peacecorps_project USING btree (country_id);


--
-- Name: peacecorps_project_featured_image_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_project_featured_image_id ON peacecorps_project USING btree (featured_image_id);


--
-- Name: peacecorps_project_issue_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_project_issue_id ON peacecorps_project USING btree (issue_id);


--
-- Name: peacecorps_project_issues_related_issue_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_project_issues_related_issue_id ON peacecorps_project_issues_related USING btree (issue_id);


--
-- Name: peacecorps_project_issues_related_project_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_project_issues_related_project_id ON peacecorps_project_issues_related USING btree (project_id);


--
-- Name: peacecorps_project_media_media_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_project_media_media_id ON peacecorps_project_media USING btree (media_id);


--
-- Name: peacecorps_project_media_project_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_project_media_project_id ON peacecorps_project_media USING btree (project_id);


--
-- Name: peacecorps_project_volunteer_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_project_volunteer_id ON peacecorps_project USING btree (volunteer_id);


--
-- Name: peacecorps_volunteer_profile_image_id; Type: INDEX; Schema: public; Owner: peacecorpsuser; Tablespace: 
--

CREATE INDEX peacecorps_volunteer_profile_image_id ON peacecorps_volunteer USING btree (profile_image_id);


--
-- Name: auth_content_type_id_379aedd149988fdf_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_content_type_id_379aedd149988fdf_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissio_group_id_6cf94cf7de52987b_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_6cf94cf7de52987b_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permission_id_147aab13e8ef112b_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_147aab13e8ef112b_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_5b5daf8adecb3605_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_5b5daf8adecb3605_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_25b13da368b5220d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_25b13da368b5220d_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_u_permission_id_124de480227a68c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_u_permission_id_124de480227a68c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permiss_user_id_3591d9630caf73ec_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_3591d9630caf73ec_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: author_id_refs_id_9643e4e6; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_media
    ADD CONSTRAINT author_id_refs_id_9643e4e6 FOREIGN KEY (author_id) REFERENCES peacecorps_volunteer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djan_content_type_id_2465074110d9e692_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT djan_content_type_id_2465074110d9e692_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_1a151c5a7c567f75_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_1a151c5a7c567f75_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: featured_image_id_refs_id_ce4bdc4f; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_issue
    ADD CONSTRAINT featured_image_id_refs_id_ce4bdc4f FOREIGN KEY (featured_image_id) REFERENCES peacecorps_media(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: issue_id_refs_id_38eaf316; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_featuredissue
    ADD CONSTRAINT issue_id_refs_id_38eaf316 FOREIGN KEY (issue_id) REFERENCES peacecorps_issue(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: peace_featured_image_id_5171e2d7c6dd9e96_fk_peacecorps_media_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_fund
    ADD CONSTRAINT peace_featured_image_id_5171e2d7c6dd9e96_fk_peacecorps_media_id FOREIGN KEY (featured_image_id) REFERENCES peacecorps_media(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: peacecorps_country_id_50c3ee9b05e96066_fk_peacecorps_country_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_countryfund
    ADD CONSTRAINT peacecorps_country_id_50c3ee9b05e96066_fk_peacecorps_country_id FOREIGN KEY (country_id) REFERENCES peacecorps_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: peacecorps_media_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_media
    ADD CONSTRAINT peacecorps_media_country_id_fkey FOREIGN KEY (country_id) REFERENCES peacecorps_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: peacecorps_pro_media_id_5cbe24fbd6d057a8_fk_peacecorps_media_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_project_media
    ADD CONSTRAINT peacecorps_pro_media_id_5cbe24fbd6d057a8_fk_peacecorps_media_id FOREIGN KEY (media_id) REFERENCES peacecorps_media(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: peacecorps_project_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_project
    ADD CONSTRAINT peacecorps_project_country_id_fkey FOREIGN KEY (country_id) REFERENCES peacecorps_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: peacecorps_project_featured_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_project
    ADD CONSTRAINT peacecorps_project_featured_image_id_fkey FOREIGN KEY (featured_image_id) REFERENCES peacecorps_media(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: peacecorps_project_id_1ed45a9d2fd0304c_fk_peacecorps_project_id; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_featuredprojectfrontpage
    ADD CONSTRAINT peacecorps_project_id_1ed45a9d2fd0304c_fk_peacecorps_project_id FOREIGN KEY (project_id) REFERENCES peacecorps_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: peacecorps_project_issue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_project
    ADD CONSTRAINT peacecorps_project_issue_id_fkey FOREIGN KEY (issue_id) REFERENCES peacecorps_issue(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: peacecorps_project_issues_related_issue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_project_issues_related
    ADD CONSTRAINT peacecorps_project_issues_related_issue_id_fkey FOREIGN KEY (issue_id) REFERENCES peacecorps_issue(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: peacecorps_volunteer_profile_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_volunteer
    ADD CONSTRAINT peacecorps_volunteer_profile_image_id_fkey FOREIGN KEY (profile_image_id) REFERENCES peacecorps_media(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_id_refs_id_163c5a9b; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_project_media
    ADD CONSTRAINT project_id_refs_id_163c5a9b FOREIGN KEY (project_id) REFERENCES peacecorps_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_id_refs_id_6becaae1; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_project_issues_related
    ADD CONSTRAINT project_id_refs_id_6becaae1 FOREIGN KEY (project_id) REFERENCES peacecorps_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: volunteer_id_refs_id_52a71d08; Type: FK CONSTRAINT; Schema: public; Owner: peacecorpsuser
--

ALTER TABLE ONLY peacecorps_project
    ADD CONSTRAINT volunteer_id_refs_id_52a71d08 FOREIGN KEY (volunteer_id) REFERENCES peacecorps_volunteer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: annaleeflowerhorne
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM annaleeflowerhorne;
GRANT ALL ON SCHEMA public TO annaleeflowerhorne;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

