-- truncate game_data cascade;
truncate game cascade;
truncate "user" cascade;
truncate admin cascade;
truncate player cascade;

-- alter sequence game_data_id_seq restart with 1;
alter sequence game_id_seq restart with 1;
alter sequence user_id_seq restart with 1;
alter sequence admin_id_seq restart with 1;
alter sequence player_id_seq restart with 1;

insert into "game_data" (id, question, answer)
values (1, 'Как в 19 веке в окрестностях Твери называли удачливого грибника или ягодника?', 'Набирошник'),
       (2, 'Какая страна не имеет столицы?', 'Науру'),
       (3, 'Какое животное может переварить стальной гвоздь?', 'Крокодил'),
       (4, 'В Швеции существует налог на собак, от которого многие пытаются уклониться. В налоговой инспекции в Стокгольме придумали забавный способ борьбы с неплательщиками: сотрудница службы Эльфрида Карлсон ходит по домам и делает это.', 'Гавкает'),
       (5, 'Польский ученый-математик Гуго Дионисий Штейнгауз, прославившийся также своими афоризмами, говорил: «Комплимент женщине должен быть правдивее, чем…»', 'Правдв'),
       (6, 'По традиции в Китае муж может в одностороннем порядке объявить о расторжении брака по семейным обстоятельствам. Назовите одну из причин для этого.', 'Болтливость'),
       (7, 'Первый подобный музей появился в Париже до 1975 года. Экскурсии по нему проводились на лодке. Сейчас туристы осматривают его экспонаты со специальных решеток и пандусов. О каком музее идет речь?', 'Канализация'),
       (8, 'В 1931 году Аркадий Райкин сам придумал и произнес со сцены некое слово. Оно стремительно вошло в обиход — так стали называть несуразную легкую сумку.', 'Авоська'),
       (9, 'Пельмени издавна заготавливают в форме ушек. Что символизируют такие пельмени?', 'Послушание'),
       (10, 'Если скорость ветра тропического шторма превышает 60 км/ч, ему присваивают личное имя. Во времена Второй мировой войны американские синоптики начали давать ураганам имена кого?', 'Теща'),
       (11, 'В словаре Владимира Ивановича Даля встречается старинное название барометра. В честь какой птицы он так назван?', 'Буревестник'),
       (12, 'Чтобы отпугнуть врагов, гуси могут грозно шипеть и больно щипаться. В Шотландии решили использовать эту особенность птиц и создали отряд гусей, который стал охранять завод. Какой?', 'Алкогольный'),
       (13, 'Английский писатель Киплинг говорил: «Женская интуиция намного точнее, чем мужская…»', 'Уверенность'),
       (14, 'Какого слова нет в языке народов Арктики?', 'Война'),
       (15, 'Соседи по улице знали Дмитрия Ивановича Менделеева как замечательного мастера по изготовлению чего?', 'Чемодан'),
       (16, 'Чтобы сделать комплимент женщине в Индии, нужно сравнить ее с коровой и слоном. Причем с коровой она должна быть схожа глазами, а со слоном — этим.', 'Походка'),
       (17, 'В XIV–XVI веках его носили мужчины. С XVII века его стали носить женщины. Названий было много: шторник, пестряк, клинник, наколоточник и др. До нас дошло лишь одно название. Какое?', 'Сарафан'),
       (18, 'Во время второй мировой войны этот предмет являлся символом единства у Норвежцев. В честь него даже построили памятник', 'Скрепка'),
       (19, 'Так в старину называли сторожа городских ворот', 'Вратарь'),
       (20, 'Как называется железная дорога с канатной тягой, устраиваемая на крутых подъемах', 'Фуникулер'),
       (21, 'Какое животное дало название распространенному в Древнем Риме способу боевого построения?', 'Черепаха'),
       (22, 'В метро этого города для того, чтобы играть в переходах, нужно еще получить специальную лицензию', 'Торонто'),
       (23, 'У этих животных, считающихся в некоторых странах деликатесом, зубы расположены на языке', 'Улитка'),
       (24, 'В Чили находится самое крупное сооружение подобного типа. Его длина – 1 километр.', 'Бассейн'),
       (25, 'Какое существо может задержать дыхание на 6 суток?', 'Скорпион')
;

insert into game (id, game_data_id, created_at, finished_at, chat_id, chat_message_id,
                  guessed_word, required_player_count, previous_player_id)
values (1, 1, now(), null, 1, 1, '', 3, 2)
;

insert into "user" (id, vk_id, name, last_name, username)
values (1, 239360732, 'Даниил', 'Бахланов', '@reductor'),
       (2, 239360735, 'Иван', 'Темный', ''),
       (3, 239360737, 'Антон', 'Жигуль', '')
;

insert into "admin" (id, user_id, email, password)
values (1, 1, 'borbri228@gmail.com', 'pass228')
;

insert into "player" (id, user_id, game_id, score, is_winner, in_game)
values (1, 1, 1, 100, FALSE, TRUE),
       (2, 2, 1, 50, FALSE, TRUE),
       (3, 3, 200, 1, FALSE, FALSE)
;