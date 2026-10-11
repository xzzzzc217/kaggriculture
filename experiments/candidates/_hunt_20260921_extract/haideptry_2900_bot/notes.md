## cell 0

<div style="background: linear-gradient(135deg, #0b2216 0%, #133c24 50%, #1e5635 100%); border-radius: 16px; padding: 30px 32px; color: #ffffff; box-shadow: 0 12px 32px rgba(0,0,0,0.18); margin-bottom: 24px;">
  <div style="display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap;">
    <span style="background: rgba(255,255,255,0.15); padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #c3eed4;">Kaggriculture Meta Forensics</span>
    <span style="background: rgba(234,179,8,0.25); padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; color: #fde047;">2900+ Reflex Engine</span>
    <span style="background: rgba(59,130,246,0.25); padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; color: #93c5fd;">One-Click Submit</span>
    <span style="background: rgba(16,185,129,0.25); padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; color: #6ee7b7;">Zero External Dependencies</span>
  </div>
  <h1 style="font-size: 32px; font-weight: 800; margin: 0 0 12px 0; color: #ffffff; line-height: 1.25;">🌾 Demystifying 2900+ Meta: The Reflex Engine, PnL Audit & Submission Bot</h1>
  <p style="font-size: 15px; color: #d1fae5; margin: 0; line-height: 1.6; max-width: 880px;">
    A forensic breakdown of the late-season breakthroughs that pushed agents past 2850–2945 Elo: moving from brittle static replays to a <b>Route-Reflex dual architecture</b>, sniffing rival market dumps before price crashes, capturing the hidden 5th sheep harvest, and safeguarding against Kaggle's fatal entrypoint trap.
  </p>
</div>

## cell 1

## 1 · The Anatomy of Late-Season 2900+ Meta

In the opening weeks of the competition, the leaderboard was dominated by simple deterministic clones of top replays. By mid-September, however, naive cloning hit an impenetrable wall: against top-tier opponents, single-tape clones suffered **0–28 wipeouts**. When opponents deviated by even a single turn, fixed action streams fractured completely.

The late-season surge to 2900+ Elo emerged from three mechanical breakthroughs and one critical engineering fix:

### 1.1 The Dual Architecture: Route Chassis + Reflex Stack
Instead of building monolithic reinforcement learning policies or fragile rule trees, the modern SOTA architecture cleanly decouples:
1. **The Route Chassis**: A rock-solid 720-turn action schedule handling spatial layout, seed planting, land acquisitions, and hand hiring parallelism ($fib(n-1)$ marginal pricing).
2. **The Reflex Stack**: A fast, reactive layer that reads the public observation on every turn and edits decisions in real time.

### 1.2 Reflex #1: Rival Sale Sniffing & Preemptive Selling (RACE)
Shared market prices collapse rapidly when supply floods the town. Rival sales are public if computed from state deltas:
$$\text{rival\_sold} = \text{inventory}' - \text{inventory} + \text{town\_draw} - \text{own\_sold}$$

The **RACE** reflex monitors this exact signal. When a competitor starts dumping premium goods (Strawberry, Milk, Wool, Melon), the reflex intercepts the route's scheduled sales and pulls them forward by **up to 40 turns**, liquidating inventory at peak prices before the rival collapses the order book.

### 1.3 Reflex #2: The Day-11 Sheep Placement Multiplier
Sheep first produce **6 days** after placement, and then every **3 days** thereafter. The season terminates at the end of **Day 29**.
* **Placed on Day 12**: Produces on days 18, 21, 24, and 27 &rarr; **4 harvests total**.
* **Placed on Day 11**: Produces on days 17, 20, 23, 26, and **29** &rarr; **5 harvests total** (+25% extra high-value wool for just 1 additional day of feed/care).

### 1.4 Animal Economics: CARE Multiplier
While `FEED` merely prevents starvation, `CARE` is the primary profit driver. Each day an animal is both fed and cared for banks one bonus unit:
* Cared Cow: **3 Milk** per production cycle (vs 1 uncared).
* Cared Sheep: **4 Wool** per production cycle (vs 1 uncared).
* Cared Goose: **2 Eggs** per production cycle (vs 1 uncared).

### 1.5 ⚠️ The Fatal Kaggle Loader Trap: `last callable`
Kaggle's simulation runner executes `main.py` and resolves the entrypoint not by looking for a function named `agent`, but by selecting:
```python
[v for v in namespace.values() if callable(v)][-1]
```
If any helper function is defined after `def agent(...)`, Kaggle executes that helper instead of your controller! The agent in this notebook includes a final wrapper ensuring `agent` remains the strictly resolved entrypoint.

## cell 8

## 4 · Strategic Takeaways: The Tomato Gap & The 2-Slot Rule

### 4.1 The Unsolved Frontier: Day-12 Tomatoes
While this public agent beats the vast majority of public bots (~2850–2945 Elo), forensic analysis of private ladder replays shows that private top-10 teams maintain one decisive advantage: **Tomatoes**.
* Top-tier private agents buy ~9 tomato seeds starting around **Day 12** and hold 10+ tomato tiles by Day 20.
* They capture secondary revenue streams while public bots fiercely contest the melon and wheat order books.
* *Experimentation tip*: Extending the route chassis with a non-interfering tomato expansion remains the highest-EV path toward 3000+ Elo.

### 4.2 The 2-Slot Submission Strategy
Remember Kaggle's evaluation dynamics:
1. **Slot 1 (Anchor)**: Keep your best verified version (such as this notebook's output) and allow it to age past 100+ games.
2. **Slot 2 (Challenger)**: Test experimental mutations or parameter sweeps. Never re-submit unchanged code to "re-roll" ratings, as short-term fluctuations ($\Delta < 50$) are purely opponent draw noise.
