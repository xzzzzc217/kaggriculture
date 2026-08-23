# fert_wheat_v2

Tracked copy: experiments/candidates/fert_wheat_v2/. Runtime copy also at artifacts/variants/fert_wheat_v2/ (gitignored). Not a promotion. Root `main.py` is unchanged h2.

- Base: h2 V36 tape + knobs (clone_horizon, msb, mr, market window untouched)
- Single structural add: class-conditional 4th-land + shed-access path onto SE
- After Q4 unlock, up to two non-farmer workers walk from shed-access onto SE,
  build the 2x2 at (5,5)/(6,5)/(5,6)/(6,6), and PLACE extra sheep
- Overrides are MOVE/PASS only so CARE/FEED/WATER stay on the tape
- Kaggle file loader uses `get_last_callable`; `fert_wheat_v2_kaggle_agent` is the last inserted callable

G5 recorded-seat replay-callback (not opposite seat):

| Stream | h2 | fert_wheat_v1 | fert_wheat_v2 |
| --- | --- | --- | --- |
| Subin An 97399969 | 65997-73104 (-7107) | 64794-77568 (-12774) | 53801-115039 (-61238) |
| James Y 95677563 | 85208-93759 (-8551) | 93448-105319 (-11871) | 71118-140511 (-69393) |

Q4: 4 pastures built; 3-4 sheep placed then escaped. Final SE animals: 0.

Failed the slice pass bar and wrecked the V36 morning tape. Stopped. No knob search.
