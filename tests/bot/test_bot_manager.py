from typing import List

from kts_backend.game.dataclasses import GameFull, Game, PlayerFull, GameData
from kts_backend.store import Store
from kts_backend.store.game.game import PoleChuDesGame
from kts_backend.store.vk_api.dataclasses import Update, UpdateObject
from kts_backend.user.dataclasses import User


class TestHandleUpdates:
    async def test_no_messages(self, store):
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

    async def test_create_game_messages(self, server, game_data_1: GameData):
        await server.store.bots_manager.handle_updates(
            updates=[
                Update(
                    type="message_new",
                    update_object=UpdateObject(
                        id=0,
                        user_id=239360732,
                        message_id=675,
                        peer_id="2000000003",
                        body="Создай игру для: [id239360732|@reducter], [id222246414|@stop_27], [id185237409|@cheatcrap]",
                    ),
                )
            ]
        )
        game_list: List[
            GameFull
        ] | None = await server.store.game.get_unfinished_game_list()
        assert game_list is not None
        assert len(game_list) == 1
        game: GameFull = game_list[0]
        player_list: List[PlayerFull] = game.player_list
        player_user_vk_id_list = []
        for player in player_list:
            assert player.game.id == game.id
            player_user_vk_id_list.append(player.user.vk_id)
        assert player_user_vk_id_list == ["239360732", "222246414", "185237409"]

        assert server.store.vk_api.send_message.called is True

    # async def test_unfinished_game_start(self, store: Store, game_2: Game):
    #     bot_manager = store.bots_manager
    #     assert len(bot_manager.game_list) == 1
    #     assert isinstance(bot_manager.game_list[0], GameFull)
    #
    # async def test_finished_game_start(self, store: Store, game_3: Game):
    #     bot_manager = store.bots_manager
    #     assert len(bot_manager.game_list) == 0
    #
    # async def test_get_game_by_chat_id(self, store: Store, game_3: Game):
    #     bot_manager = store.bots_manager
    #     full_game = store.game.get_full_game(game_id=game_3.id)
    #     pole_game = await PoleChuDesGame(app=store.bots_manager.app).init_from(game=full_game)
    #     assert await bot_manager.get_game_by_chat_id("2") == pole_game
