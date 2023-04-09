from typing import List

from kts_backend.game.dataclasses import GameFull, Game, PlayerFull, GameData
from kts_backend.store import Store
from kts_backend.store.game.game import PoleChuDesGame
from kts_backend.store.vk_api.dataclasses import Update, UpdateObject
from kts_backend.user.dataclasses import User


class TestHandleUpdates:
    async def test_no_messages(self, store: Store):
        await store.bots_manager.handle_updates(updates=[])
        assert store.vk_api.send_message.called is False

    async def test_unexpected_messages(self, store: Store):
        await store.bots_manager.handle_updates(
            updates=[
                Update(
                    type="message_new",
                    update_object=UpdateObject(
                        id=0,
                        user_id=239360732,
                        message_id=675,
                        peer_id="2000000003",
                        body="abracadabra",
                    ),
                )
            ]
        )
        user: User | None = await store.user.get_one_user_by_vk_id(
            vk_id=239360732
        )
        assert user is None
        game: Game | None = await store.game.get_last_game(chat_id="2000000003")
        assert game is None
        assert store.vk_api.send_message.called is True

    async def test_create_game_messages(
        self, store: Store, game_data_1: GameData
    ):
        await store.bots_manager.handle_updates(
            updates=[
                Update(
                    type="message_new",
                    update_object=UpdateObject(
                        id=0,
                        user_id=239360732,
                        message_id=675,
                        peer_id="2000000003",
                        body="Создай игру для: [id123|@reducter], "
                        "[id456|@stop_27], [id789|@cheatcrap]",
                    ),
                )
            ]
        )
        game_list: List[
            GameFull
        ] | None = await store.game.get_unfinished_game_list()
        assert game_list is not None
        assert len(game_list) == 1

        game: GameFull = game_list[0]
        assert isinstance(game, GameFull)

        player_list: List[PlayerFull] = game.player_list
        player_user_vk_id_list = []
        for player in player_list:
            player_user_vk_id_list.append(player.user.vk_id)
        assert player_user_vk_id_list == [123, 456, 789]

        assert store.vk_api.send_message.called is True

    async def test_wrong_username_messages(
        self, store: Store, game_data_1: GameData
    ):
        await store.bots_manager.handle_updates(
            updates=[
                Update(
                    type="message_new",
                    update_object=UpdateObject(
                        id=0,
                        user_id=239360732,
                        message_id=675,
                        peer_id="2000000003",
                        body="Создай игру для: [id123|@johndoe], "
                        "[id456|@johndoe1], [id789|@johndoe2]",
                    ),
                )
            ]
        )
        user: User | None = await store.user.get_one_user_by_vk_id(
            vk_id=239360732
        )
        assert user is None

        user_list = await store.user.get_user_list_by_vk_id_list(
            vk_id_list=[123, 456, 789]
        )
        assert len(user_list) == 0

        game: Game | None = await store.game.get_last_game(chat_id="2000000003")
        assert game is None

        assert store.vk_api.send_message.called is True


class TestStart:
    async def test_finished_game_start(self, cli, store: Store, game_4: Game):
        bot_manager = store.bots_manager
        await bot_manager.start()
        assert len(bot_manager.game_list) == 0

    async def test_unfinished_game_start(self, cli, store: Store, game_3: Game):
        bot_manager = store.bots_manager
        await bot_manager.start()
        assert len(bot_manager.game_list) == 1
        game = bot_manager.game_list[0]
        assert isinstance(game, PoleChuDesGame)
        assert (
            await bot_manager.get_game_by_chat_id(chat_id=game_3.chat_id)
            == game
        )
