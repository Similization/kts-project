create table if not exists public.alembic_version
(
    version_num varchar(32) not null,
    constraint alembic_version_pkc
        primary key (version_num)
);

create table if not exists public.game_data
(
    id       serial,
    question varchar(300) not null,
    answer   varchar(30)  not null,
    primary key (id),
    unique (question)
);

create table if not exists public."user"
(
    id        serial,
    vk_id     integer     not null,
    name      varchar(45) not null,
    last_name varchar(45) not null,
    username  varchar(45) not null,
    primary key (id),
    unique (vk_id)
);

create table if not exists public.admin
(
    id       serial,
    user_id  integer,
    email    varchar(60) not null,
    password varchar(75) not null,
    primary key (id),
    unique (email),
    foreign key (user_id) references public."user"(id)
        on delete set null
);

create table if not exists public.game
(
    id                    serial,
    game_data_id          integer     not null,
    created_at            timestamp,
    finished_at           timestamp,
    chat_id               varchar(15) not null,
    chat_message_id       integer,
    guessed_word          varchar(30) not null,
    required_player_count smallint    not null,
    previous_player_id    integer,
    primary key (id),
    foreign key (game_data_id) references public.game_data(id)
        on delete set null
);

create table if not exists public.player
(
    id        serial,
    user_id   integer not null,
    game_id   integer not null,
    score     integer not null,
    is_winner boolean not null,
    in_game   boolean,
    primary key (id),
    foreign key (game_id) references public.game(id)
        on delete cascade,
    foreign key (user_id) references public."user"(id)
        on delete cascade
);
