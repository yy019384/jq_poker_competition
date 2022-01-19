#!/usr/bin/env python3

from pypokerengine.api.game import setup_config, start_poker
from pypokerengine.players import BasePokerPlayer

import argparse
import multiprocessing as mp


def load_sub_classes(directory, base_class):
    import importlib.util
    import os

    abs_dir = os.path.abspath(directory)
    classes = []
    files = filter(lambda f: f.endswith(".py"), os.listdir(abs_dir))

    for f in files:
        spec = importlib.util.spec_from_file_location("", os.path.join(abs_dir, f))
        a_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(a_module)
        for name in dir(a_module):
            obj = getattr(a_module, name)
            if (
                isinstance(obj, type)
                and issubclass(obj, base_class)
                and obj != base_class
            ):
                classes.append(obj)

    return classes


def start_one_game(rounds):
    config = setup_config(max_round=rounds, initial_stack=100, small_blind_amount=5)
    player_constructors = load_sub_classes("./players", BasePokerPlayer)

    names = set([ctor.__name__ for ctor in player_constructors])
    assert len(names) == len(player_constructors), "found duplicated player name!"

    for ctor in player_constructors:
        config.register_player(name=ctor.__name__, algorithm=ctor())

    return start_poker(config, verbose=1)


def get_winner(rounds):
    result = start_one_game(rounds)
    winner_name = ""
    winner_stack = 0
    for player in result["players"]:
        if player["stack"] > winner_stack:
            winner_name = player["name"]
            winner_stack = player["stack"]
    return (winner_name, winner_stack)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run multiple poker games")
    parser.add_argument("-g", "--games", type=int, default=100, help="game count")
    parser.add_argument(
        "-r", "--rounds", type=int, default=10, help="round count in each game"
    )
    parser.add_argument("-c", "--cores", type=int, default=8, help="use how many cores")

    args = parser.parse_args()

    n = args.games
    rounds = args.rounds
    core_num = args.cores

    with mp.Pool(core_num) as pool:
        winners = pool.map(get_winner, [rounds] * n)

        win_counts = {}
        win_stacks = {}
        for (winner, stack) in winners:
            if winner not in win_counts:
                win_counts[winner] = 0
            win_counts[winner] += 1
            if winner not in win_stacks:
                win_stacks[winner] = 0
            win_stacks[winner] += stack

        for name, win_count in win_counts.items():
            print(
                "player {} wins {} out of {}, total stack {}".format(
                    name, win_count, n, win_stacks[name]
                )
            )
