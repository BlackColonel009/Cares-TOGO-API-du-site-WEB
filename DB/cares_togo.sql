PGDMP  *                    }         
   cares_togo    15.11    17.3 M    \           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            ]           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            ^           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            _           1262    16398 
   cares_togo    DATABASE     p   CREATE DATABASE cares_togo WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'fr-FR';
    DROP DATABASE cares_togo;
                     postgres    false            �            1259    40985    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap r       postgres    false            �            1259    49176    blog_post_categories    TABLE     r   CREATE TABLE public.blog_post_categories (
    blog_post_id integer NOT NULL,
    category_id integer NOT NULL
);
 (   DROP TABLE public.blog_post_categories;
       public         heap r       postgres    false            �            1259    34415 
   blog_posts    TABLE     �   CREATE TABLE public.blog_posts (
    id integer NOT NULL,
    title character varying,
    content text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    user_id integer,
    image_url character varying(255)
);
    DROP TABLE public.blog_posts;
       public         heap r       postgres    false            �            1259    34414    blog_posts_id_seq    SEQUENCE     �   CREATE SEQUENCE public.blog_posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.blog_posts_id_seq;
       public               postgres    false    219            `           0    0    blog_posts_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.blog_posts_id_seq OWNED BY public.blog_posts.id;
          public               postgres    false    218            �            1259    34405    books    TABLE     C  CREATE TABLE public.books (
    id integer NOT NULL,
    title character varying NOT NULL,
    author character varying NOT NULL,
    description text,
    file_url character varying,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    user_id integer
);
    DROP TABLE public.books;
       public         heap r       postgres    false            �            1259    34404    books_id_seq    SEQUENCE     �   CREATE SEQUENCE public.books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.books_id_seq;
       public               postgres    false    217            a           0    0    books_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.books_id_seq OWNED BY public.books.id;
          public               postgres    false    216            �            1259    49155 
   categories    TABLE     f   CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);
    DROP TABLE public.categories;
       public         heap r       postgres    false            �            1259    49154    categories_id_seq    SEQUENCE     �   CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.categories_id_seq;
       public               postgres    false    226            b           0    0    categories_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;
          public               postgres    false    225            �            1259    40991    comments    TABLE     �   CREATE TABLE public.comments (
    id integer NOT NULL,
    content text NOT NULL,
    created_at timestamp without time zone,
    user_id integer,
    blog_id integer
);
    DROP TABLE public.comments;
       public         heap r       postgres    false            �            1259    40990    comments_id_seq    SEQUENCE     �   CREATE SEQUENCE public.comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.comments_id_seq;
       public               postgres    false    224            c           0    0    comments_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;
          public               postgres    false    223            �            1259    40961    media    TABLE       CREATE TABLE public.media (
    id integer NOT NULL,
    name character varying NOT NULL,
    file_url character varying NOT NULL,
    media_type character varying NOT NULL,
    description character varying,
    blog_post_id integer,
    user_id integer
);
    DROP TABLE public.media;
       public         heap r       postgres    false            �            1259    40960    media_id_seq    SEQUENCE     �   CREATE SEQUENCE public.media_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.media_id_seq;
       public               postgres    false    221            d           0    0    media_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.media_id_seq OWNED BY public.media.id;
          public               postgres    false    220            �            1259    49206    partners    TABLE       CREATE TABLE public.partners (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    logo_url character varying,
    website_url character varying,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);
    DROP TABLE public.partners;
       public         heap r       postgres    false            �            1259    49205    partners_id_seq    SEQUENCE     �   CREATE SEQUENCE public.partners_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.partners_id_seq;
       public               postgres    false    229            e           0    0    partners_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.partners_id_seq OWNED BY public.partners.id;
          public               postgres    false    228            �            1259    34393    users    TABLE     b  CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying,
    email character varying,
    hashed_password character varying,
    is_admin boolean,
    role character varying(50) DEFAULT 'user'::character varying,
    avatar_url character varying(255),
    bio text,
    created_at timestamp without time zone DEFAULT now()
);
    DROP TABLE public.users;
       public         heap r       postgres    false            �            1259    34392    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public               postgres    false    215            f           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public               postgres    false    214            �           2604    34418    blog_posts id    DEFAULT     n   ALTER TABLE ONLY public.blog_posts ALTER COLUMN id SET DEFAULT nextval('public.blog_posts_id_seq'::regclass);
 <   ALTER TABLE public.blog_posts ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    219    218    219            �           2604    34408    books id    DEFAULT     d   ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.books_id_seq'::regclass);
 7   ALTER TABLE public.books ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    216    217    217            �           2604    49158    categories id    DEFAULT     n   ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);
 <   ALTER TABLE public.categories ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    226    225    226            �           2604    40994    comments id    DEFAULT     j   ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);
 :   ALTER TABLE public.comments ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    223    224    224            �           2604    40964    media id    DEFAULT     d   ALTER TABLE ONLY public.media ALTER COLUMN id SET DEFAULT nextval('public.media_id_seq'::regclass);
 7   ALTER TABLE public.media ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    221    220    221            �           2604    49209    partners id    DEFAULT     j   ALTER TABLE ONLY public.partners ALTER COLUMN id SET DEFAULT nextval('public.partners_id_seq'::regclass);
 :   ALTER TABLE public.partners ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    228    229    229            �           2604    34396    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    215    214    215            R          0    40985    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public               postgres    false    222   &Y       W          0    49176    blog_post_categories 
   TABLE DATA           I   COPY public.blog_post_categories (blog_post_id, category_id) FROM stdin;
    public               postgres    false    227   CY       O          0    34415 
   blog_posts 
   TABLE DATA           d   COPY public.blog_posts (id, title, content, created_at, updated_at, user_id, image_url) FROM stdin;
    public               postgres    false    219   hY       M          0    34405    books 
   TABLE DATA           j   COPY public.books (id, title, author, description, file_url, created_at, updated_at, user_id) FROM stdin;
    public               postgres    false    217   ?[       V          0    49155 
   categories 
   TABLE DATA           .   COPY public.categories (id, name) FROM stdin;
    public               postgres    false    226   '\       T          0    40991    comments 
   TABLE DATA           M   COPY public.comments (id, content, created_at, user_id, blog_id) FROM stdin;
    public               postgres    false    224   ^\       Q          0    40961    media 
   TABLE DATA           c   COPY public.media (id, name, file_url, media_type, description, blog_post_id, user_id) FROM stdin;
    public               postgres    false    221   �]       Y          0    49206    partners 
   TABLE DATA           h   COPY public.partners (id, name, description, logo_url, website_url, created_at, updated_at) FROM stdin;
    public               postgres    false    229   �^       K          0    34393    users 
   TABLE DATA           r   COPY public.users (id, username, email, hashed_password, is_admin, role, avatar_url, bio, created_at) FROM stdin;
    public               postgres    false    215   7_       g           0    0    blog_posts_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.blog_posts_id_seq', 7, true);
          public               postgres    false    218            h           0    0    books_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.books_id_seq', 6, true);
          public               postgres    false    216            i           0    0    categories_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.categories_id_seq', 2, true);
          public               postgres    false    225            j           0    0    comments_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.comments_id_seq', 9, true);
          public               postgres    false    223            k           0    0    media_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.media_id_seq', 1, true);
          public               postgres    false    220            l           0    0    partners_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.partners_id_seq', 8, true);
          public               postgres    false    228            m           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 6, true);
          public               postgres    false    214            �           2606    40989 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public                 postgres    false    222            �           2606    49180 .   blog_post_categories blog_post_categories_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.blog_post_categories
    ADD CONSTRAINT blog_post_categories_pkey PRIMARY KEY (blog_post_id, category_id);
 X   ALTER TABLE ONLY public.blog_post_categories DROP CONSTRAINT blog_post_categories_pkey;
       public                 postgres    false    227    227            �           2606    34422    blog_posts blog_posts_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.blog_posts DROP CONSTRAINT blog_posts_pkey;
       public                 postgres    false    219            �           2606    34412    books books_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.books DROP CONSTRAINT books_pkey;
       public                 postgres    false    217            �           2606    49162    categories categories_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.categories DROP CONSTRAINT categories_name_key;
       public                 postgres    false    226            �           2606    49160    categories categories_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.categories DROP CONSTRAINT categories_pkey;
       public                 postgres    false    226            �           2606    40998    comments comments_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.comments DROP CONSTRAINT comments_pkey;
       public                 postgres    false    224            �           2606    40968    media media_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.media
    ADD CONSTRAINT media_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.media DROP CONSTRAINT media_pkey;
       public                 postgres    false    221            �           2606    49215    partners partners_name_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.partners
    ADD CONSTRAINT partners_name_key UNIQUE (name);
 D   ALTER TABLE ONLY public.partners DROP CONSTRAINT partners_name_key;
       public                 postgres    false    229            �           2606    49213    partners partners_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.partners
    ADD CONSTRAINT partners_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.partners DROP CONSTRAINT partners_pkey;
       public                 postgres    false    229            �           2606    34400    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    215            �           1259    34428    ix_blog_posts_id    INDEX     E   CREATE INDEX ix_blog_posts_id ON public.blog_posts USING btree (id);
 $   DROP INDEX public.ix_blog_posts_id;
       public                 postgres    false    219            �           1259    34413    ix_books_id    INDEX     ;   CREATE INDEX ix_books_id ON public.books USING btree (id);
    DROP INDEX public.ix_books_id;
       public                 postgres    false    217            �           1259    41009    ix_comments_id    INDEX     A   CREATE INDEX ix_comments_id ON public.comments USING btree (id);
 "   DROP INDEX public.ix_comments_id;
       public                 postgres    false    224            �           1259    40979    ix_media_id    INDEX     ;   CREATE INDEX ix_media_id ON public.media USING btree (id);
    DROP INDEX public.ix_media_id;
       public                 postgres    false    221            �           1259    49216    ix_partners_id    INDEX     A   CREATE INDEX ix_partners_id ON public.partners USING btree (id);
 "   DROP INDEX public.ix_partners_id;
       public                 postgres    false    229            �           1259    34403    ix_users_email    INDEX     H   CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);
 "   DROP INDEX public.ix_users_email;
       public                 postgres    false    215            �           1259    34402    ix_users_id    INDEX     ;   CREATE INDEX ix_users_id ON public.users USING btree (id);
    DROP INDEX public.ix_users_id;
       public                 postgres    false    215            �           1259    34401    ix_users_username    INDEX     N   CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);
 %   DROP INDEX public.ix_users_username;
       public                 postgres    false    215            �           2606    49181 ;   blog_post_categories blog_post_categories_blog_post_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.blog_post_categories
    ADD CONSTRAINT blog_post_categories_blog_post_id_fkey FOREIGN KEY (blog_post_id) REFERENCES public.blog_posts(id) ON DELETE CASCADE;
 e   ALTER TABLE ONLY public.blog_post_categories DROP CONSTRAINT blog_post_categories_blog_post_id_fkey;
       public               postgres    false    219    3231    227            �           2606    49186 :   blog_post_categories blog_post_categories_category_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.blog_post_categories
    ADD CONSTRAINT blog_post_categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE;
 d   ALTER TABLE ONLY public.blog_post_categories DROP CONSTRAINT blog_post_categories_category_id_fkey;
       public               postgres    false    227    3244    226            �           2606    34423 "   blog_posts blog_posts_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 L   ALTER TABLE ONLY public.blog_posts DROP CONSTRAINT blog_posts_user_id_fkey;
       public               postgres    false    3226    219    215            �           2606    49219    books books_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
 B   ALTER TABLE ONLY public.books DROP CONSTRAINT books_user_id_fkey;
       public               postgres    false    3226    217    215            �           2606    41004    comments comments_blog_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_blog_id_fkey FOREIGN KEY (blog_id) REFERENCES public.blog_posts(id);
 H   ALTER TABLE ONLY public.comments DROP CONSTRAINT comments_blog_id_fkey;
       public               postgres    false    219    224    3231            �           2606    40999    comments comments_user_id_fkey    FK CONSTRAINT     }   ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 H   ALTER TABLE ONLY public.comments DROP CONSTRAINT comments_user_id_fkey;
       public               postgres    false    224    3226    215            �           2606    40969    media media_blog_post_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.media
    ADD CONSTRAINT media_blog_post_id_fkey FOREIGN KEY (blog_post_id) REFERENCES public.blog_posts(id);
 G   ALTER TABLE ONLY public.media DROP CONSTRAINT media_blog_post_id_fkey;
       public               postgres    false    3231    219    221            �           2606    40974    media media_user_id_fkey    FK CONSTRAINT     w   ALTER TABLE ONLY public.media
    ADD CONSTRAINT media_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 B   ALTER TABLE ONLY public.media DROP CONSTRAINT media_user_id_fkey;
       public               postgres    false    221    3226    215            R      x������ � �      W      x�3�4�2�4����� ��      O   �  x�}��n�0���)涧%�;pks�Z%{hR�	�0���x�>Q�y�����ā�����{f��F��F�M��\a��=Bc̈́&@�0�ҿ%��bK�����y���3ZbU"���/�;��훟���OG��/�r�M��s�E��4���|U�a��U��tv&gG���|F��L���#�����5�3��bAS*�bU"a�j���}���~
ng�v��v>*�^�-e�a|Jr� D�=�<��A�8���n\�V��f�,K)��>Ճr{���fK����ap<�.�ܠ���80��h�3��"+�.�2����j�d$NH{����洏o�EVy^1:���|Uz�������5���?}����YM�%�$;������Y�KOZtF���m�=�I[��5���}����pV�ʊ��lMb��>�I��9��      M   �   x���1n� �N�����6�*m6)Ҧ�.$AA�Ιr�\,t+Y��HS͗��a��TE���Q�-ũm2�e�DNk�l�3��/D���G1���B�nQ�ፁ<(8@'T�Q{�KT��Gv���X�@��|z:m���G趆�^�7J�ܠw#n���8��Z� ��6�1�Xi�zh6��J�ba+��z���G�tJ;g7"�A	�Ae��*9�]��      V   '   x�3�IM�����O�L�2�tM)MN,�������� ��	?      T   e  x�e�;n�0Ekj�ʕ	��YC\��Fm�T�1��t��,B�HN��{�ɾ�#ؘݸ ��}��8����)Y�9��l�jy'[�� ۡ\�}[�L2Q)�u�������.=�a]�g[D?�\稖���FS��4s`ʐc�`��g�zX1N#��f�O)jrh�t�jA)�j�lX^�����9�����h.�w�k�%��eK�6�C	Ʋ\O+I��u�wGi*.�T�}D�f���$�B"˓���İZ�x�}�K.���p�[�>4�l�=���)�4Mn��3�%~�']Kq���S��Šz.��q3]����P0g���=(���?�7�w^U�8��      Q   �   x�Տ1��0Dk���oV+(#�
!��(i��c���l�l��l��n4���i�w<�o?��nۺۢ���Kov��#��A�`J2r�N"yx���وQ%�qѢ?<�W
"6X�)Zi�.��F�2'��=��S?�K�rq�s���pq�4I��p���Q_'������\ �J�UW�uUU�G9�       Y   �   x��ͱ� @������lj�&u��4TI�6��Gg�s�k�[�m�\�=]c����%-��3�[)�+����$��L�n*ԕ&�P���!�M��V�S;��C�v8�=T&��h!� >J���$8�      K   �   x���=S�0 ��9|
ֆ&B�N�8pk_�uA	\l��^��[Y;��s��wB	5���L��_J��П�x�jZD��ΣI�L�^͒K�udp_eU���v��8�kX�/��Kl-�x��"+��M�$��!��L͹�3|wS����7�n!���cL����p0�z�E����3���,�������<_�է�!�,���k^Nco���)(��ސ
��˜�UH���>
#Z�f���ƏPӴ�zm�     