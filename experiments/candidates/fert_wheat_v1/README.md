# fert_wheat_v1

Tracked copy: experiments/candidates/fert_wheat_v1/. Runtime copy also at artifacts/variants/fert_wheat_v1/ (gitignored). Not a promotion. Root `main.py` is unchanged h2.

- Base: h2 V36 tape + knobs (clone_horizon, msb, mr, market window untouched)
- Single structural add: class-conditional 4th-land + extra-sheep satellite
- Activates after step 241 if the opponent has >=3 quadrants or >=6 sheep
- Field edits are PASS-only (DIG / BUILD_PASTURE / PICKUP / PLACE on SE or shed-access)
- Kaggle file loader uses `get_last_callable`; `fert_wheat_v1_kaggle_agent` is the last inserted callable

G5 recorded-seat replay-callback (not opposite seat):

| Stream | h2 | fert_wheat_v1 |
| --- | --- | --- |
| Subin An 97399969 | 65997-73104 (-7107) | 64794-77568 (-12774) |
| James Y 95677563 | 85208-93759 (-8551) | 93448-105319 (-11871) |

Failed the slice pass bar (must beat both streams). Stopped. No knob search.
