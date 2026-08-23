from kaggle_environments import make

from main import agent


def test_agent_finishes_from_both_seats() -> None:
    for seat in (0, 1):
        players = [agent, "pass"] if seat == 0 else ["pass", agent]
        env = make(
            "kaggriculture",
            configuration={"episodeSteps": 48, "seed": 20260821},
            debug=True,
        )
        env.run(players)
        assert [state.status for state in env.steps[-1]] == ["DONE", "DONE"]

