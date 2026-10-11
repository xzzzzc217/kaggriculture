_E334_REPORT=dict(changed=0,removed=0,errors=0)
_E334_BASE=_y_agent_shopherd

def _e334_compact(obs,action):
    market=action.get('market') or []
    if int(obs['step'])<144 or len(market)<2:return action
    segments=[];i=0
    while i<len(market):
        if len(market[i])>=3 and market[i][0]=='SELL' and market[i][1] in _E334_ITEMS:
            j=i+1
            while j<len(market) and len(market[j])>=3 and market[j][0]=='SELL' and market[j][1] in _E334_ITEMS:j+=1
            if j-i>=2:segments.append((i,j))
            i=j
        else:i+=1
    if not segments:return action
    _,private=_r127_fields(obs,action);remaining=dict(private['shed']);new=[list(o) for o in market];removed=0
    for start,end in segments:
        quantities={};order=[]
        for o in market[start:end]:
            p=o[1]
            if p not in quantities:order.append(p);quantities[p]=0
            quantities[p]+=max(0,int(o[2]))
        kept=[]
        for p in order:
            q=min(quantities[p],max(0,int(remaining.get(p,0))))
            if q:kept.append(['SELL',p,q]);remaining[p]-=q
        # Empty order slots are explicitly skipped by the pinned engine parser.
        # Keep external order indices unchanged; do not pull BUY/HIRE forward.
        replacement=kept+[[] for _ in range(end-start-len(kept))]
        if replacement!=market[start:end]:removed+=end-start-len(kept);new[start:end]=replacement
    if new==market:return action
    _E334_REPORT['changed']+=1;_E334_REPORT['removed']+=removed
    return dict(action,market=new)

def _e334_agent(observation,configuration=None):
    if int(observation.get('step',0))==0:
        for k in _E334_REPORT:_E334_REPORT[k]=0
    action=_E334_BASE(observation,configuration)
    try:return _e334_compact(observation,action)
    except Exception:
        _E334_REPORT['errors']+=1;return action

# EXP335: empty buyable-product sales are holes too, when no purchases exist.
_E335_ORIGINAL_COMPACT=_e334_compact

def _e334_compact(obs,action):
    market=action.get('market') or []
    if int(obs['step'])<144 or len(market)<2:return action
    if not all(len(o)>=3 and o[0]=='SELL' for o in market):return _E335_ORIGINAL_COMPACT(obs,action)
    _,private=_r127_fields(obs,action);remaining=dict(private['shed']);effective=[]
    for o in market:
        item=o[1];q=min(max(0,int(o[2])),max(0,int(remaining.get(item,0))))
        remaining[item]=max(0,int(remaining.get(item,0))-q)
        effective.append(['SELL',item,q] if q else [])
    new=[list(o) for o in effective];i=0;removed=0
    while i<len(effective):
        if effective[i] and effective[i][1] not in _E334_ITEMS:i+=1;continue
        j=i+1
        while j<len(effective) and (not effective[j] or effective[j][1] in _E334_ITEMS):j+=1
        order=[];qty={}
        for o in effective[i:j]:
            if not o:continue
            if o[1] not in qty:order.append(o[1]);qty[o[1]]=0
            qty[o[1]]+=o[2]
        kept=[['SELL',item,qty[item]] for item in order]
        new[i:j]=kept+[[] for _ in range(j-i-len(kept))];removed+=j-i-len(kept);i=j
    if new==market:return action
    _E334_REPORT['changed']+=1;_E334_REPORT['removed']+=removed
    return dict(action,market=new)

def _e335_agent(observation,configuration=None):
    return _e334_agent(observation,configuration)




# ---------------------------------------------------------------------------
# v11 entry normalisation: Kaggle's loader takes the last callable in the module
# namespace.  Rebind it to a fresh `agent` so the packaged name matches the rest
# of the v9 releases (and so validate.py's name check passes).
# ---------------------------------------------------------------------------
_V11_ENTRY = [v for v in list(globals().values()) if callable(v)][-1]


def agent(observation, configuration=None):
    return _V11_ENTRY(observation, configuration)


agent.telemetry = getattr(_V11_ENTRY, 'telemetry', {})
agent = globals().pop('agent')


# ---------------------------------------------------------------------------
# v13 V219SKIP (review suggestion #1): V219 hires a tomato crew every day from
# day 19, but tomatoes planted on day 18 only produce at the refreshes ending
# days 25-28.  Before that, watering only keeps them alive, and a plant
# survives one dry day (it dies after two consecutive dry refreshes).  On the
# chosen skip days, when every committed tomato was watered yesterday
# (consecutive_unwatered == 0), no crew is hired and nobody waters them today;
# the next day's crew waters them again.
# ---------------------------------------------------------------------------
V13V_SKIP_DAYS = (19, 21, 23)
_V13V_REPORT = dict(v_skipped=0, v_blocked=0, v_errors=0)
_V13V_ORIG_REQUEST = _v219_request


def _v219_request(obs, action, state, native):
    try:
        day = int(obs["step"]) // 24
        if day in V13V_SKIP_DAYS and state.get("committed") and state.get("requested_day") != day:
            farm = obs["farms"][int(obs["player"])]
            tomatoes = 0
            safe = True
            for x, y in state.get("targets", []):
                tile = farm["tiles"][y][x]
                if isinstance(tile, dict) and tile.get("crop") == "TOMATO":
                    tomatoes += 1
                    if int(tile.get("consecutive_unwatered", 1)) != 0:
                        safe = False
            if tomatoes and safe:
                state["requested_day"] = day
                _V13V_REPORT["v_skipped"] += 1
                return action
            if tomatoes:
                _V13V_REPORT["v_blocked"] += 1
    except Exception:
        _V13V_REPORT["v_errors"] += 1
    return _V13V_ORIG_REQUEST(obs, action, state, native)


_V13V_PARENT = agent


def agent(observation, configuration=None):
    if int(observation["step"]) == 0:
        for k in _V13V_REPORT:
            _V13V_REPORT[k] = 0
    return _V13V_PARENT(observation, configuration)


agent.telemetry = _V13V_REPORT
agent = globals().pop("agent")


# Bounded alternative productive openings. Dmitrii Gluzdov, 2026, Apache-2.0.
# The upstream The 2945 Farm source and its notices are preserved above.
_ALT_MODE = 'HybridOpening'
_ALT_RAW = copy.deepcopy(_IMPL.chassis.routes[0][:96])
_ALT_CT = dict(CT_TABLE)
_ALT_STATE = {}
_ALT_REPORT = {}

def _alt_install(mode):
    global CT_TABLE
    tape=_IMPL.chassis.routes[0]
    tape[:96]=copy.deepcopy(_ALT_RAW)
    CT_TABLE=dict(_ALT_CT)
    if mode=='Original': return
    if mode=='HybridOpening':
        tape[0]['market']=list(tape[0]['market'])+[['BUY_SEED','WHEAT',1]]
    else:
        CT_TABLE={}
        tape[0]['market']=[['BUY_PRODUCT','WHEAT',5],['BUY_SEED','WHEAT',1]]
        tape[1]['market']=[o for o in tape[1]['market'] if not (len(o)>=3 and o[0] in ('BUY_PRODUCT','SELL') and o[1]=='WHEAT')]
    # Day-zero idle hand 1 walks from (5,4) to the future (2,4) pasture.
    for step,command in {2:['WEST'],3:['WEST'],4:['WEST'],5:['PLANT','WHEAT'],6:['WATER']}.items():
        assert tape[step]['hands'][1]==['PASS']
        tape[step]['hands'][1]=command
    # On day one, water instead of building the not-yet-needed pasture.
    assert tape[29]['hands'][2]==['BUILD_PASTURE']
    tape[29]['hands'][2]=['WATER']
    # Day-two idle hand 0: water, harvest, restore pasture, deliver.
    commands=[['WEST'],['WEST'],['WEST'],['WATER'],['HARVEST'],['BUILD_PASTURE'],['EAST'],['EAST'],['DROP']]
    for step,command in zip(range(49,58),commands):
        assert tape[step]['hands'][0]==['PASS']
        tape[step]['hands'][0]=command
    if mode=='TomatoInsteadOfCow':
        tape[0]['market'].append(['BUY_SEED','TOMATO',1])
        cow=next(o for o in tape[1]['market'] if o[:2]==['BUY_ANIMAL','COW'])
        assert cow[2]==2; cow[2]=1
        # The first carrier still owns the bought cow; the other cow's site
        # becomes one tomato plant, with its worker route left in place.
        assert tape[2]['hands'][4][:2]==['PICKUP','COW']
        assert tape[3]['hands'][4]==['BUILD_PASTURE']
        assert tape[4]['hands'][4][:2]==['PLACE','COW']
        tape[2]['hands'][4]=['PASS']
        tape[3]['hands'][4]=['PASS']
        tape[4]['hands'][4]=['PLANT','TOMATO']
        tape[5]['hands'][4]=['WATER']
    assert max(len(a.get('market',[])) for a in tape[:96])<=10

def _alt_sell_extra(action,item,n):
    if n<=0:return action
    orders=[list(o) for o in action.get('market',[])]
    sell=next((o for o in orders if len(o)>=3 and o[:2]==['SELL',item]),None)
    if sell is not None:sell[2]+=n
    elif len(orders)<10:orders.append(['SELL',item,n])
    else:return action
    return dict(action,market=orders)

_ALT_PARENT=agent
def agent(observation,configuration=None):
    seat,step=int(observation['player']),int(observation['step'])
    state=_ALT_STATE.get(seat)
    if state is None or step<=state['step']:
        mode=_ALT_MODE
        if mode=='Mixed':
            # Private RNG: no mutation of the engine or opponent's random state.
            # Seed is used only for reproducible opening selection, never prediction.
            import random as _opening_random
            seed=(configuration or {}).get('seed',0)
            bit=_opening_random.Random('productive-opening:'+str(seed)+':'+str(seat)).getrandbits(1)
            mode='EarlyCycle' if bit else 'Original'
        _alt_install(mode)
        state=_ALT_STATE[seat]={'step':-1,'mode':mode}
        _ALT_REPORT.clear()
        _ALT_REPORT.update(selected_opening=mode,temporary_crop_seen=0,temporary_crop_harvested=0,
                           restored_pasture_seen=0,delivered_extra_wheat=0,tomato_seen=0,
                           tomato_water_requests=0,tomato_harvest_requests=0,tomato_units_harvest_requested=0,
                           extension_errors=0)
    action=_ALT_PARENT(observation,configuration)
    try:
        mode=state['mode']
        if mode!='Original':
            farm=observation['farms'][seat];private=observation['private']
            site=farm['tiles'][4][2]
            if step==6:_ALT_REPORT['temporary_crop_seen']=int(isinstance(site,dict) and site.get('crop')=='WHEAT')
            if step==54:
                _ALT_REPORT['temporary_crop_harvested']=int(private['inventories'][1].get('WHEAT',0))
            if step==55:_ALT_REPORT['restored_pasture_seen']=int(isinstance(site,dict) and site.get('kind')=='PASTURE')
            if step==57 and len(farm['hands'])>=1:
                if tuple(farm['hands'][0])==(4,4) and action.get('hands',[[]])[0]==['DROP']:
                    n=int(private['inventories'][1].get('WHEAT',0))
                    action=_alt_sell_extra(action,'WHEAT',n)
                    _ALT_REPORT['delivered_extra_wheat']=n
            if mode=='TomatoInsteadOfCow':
                tomato=farm['tiles'][4][4]
                if isinstance(tomato,dict) and tomato.get('crop')=='TOMATO' and tomato.get('planted_day')==0:
                    _ALT_REPORT['tomato_seen']=1
                    units=[list(action.get('farmer') or ['PASS'])]+[list(c) for c in action.get('hands',[])]
                    positions=[tuple(farm['farmer'])]+[tuple(p) for p in farm['hands']]
                    watered=bool(tomato.get('watered_today'));yield_left=int(tomato.get('yield_units',0))
                    for actor,pos in enumerate(positions):
                        if pos!=(4,4) or actor>=len(units):continue
                        if units[actor][0] not in ('FEED','CARE','COLLECT_FERTILIZER','HARVEST','WATER','PASS'):continue
                        if not watered:
                            units[actor]=['WATER'];watered=True
                            _ALT_REPORT['tomato_water_requests']+=1
                        elif yield_left>0:
                            units[actor]=['HARVEST']
                            _ALT_REPORT['tomato_harvest_requests']+=1
                            _ALT_REPORT['tomato_units_harvest_requested']+=yield_left
                            yield_left=0
                        else:units[actor]=['PASS']
                    action=dict(action,farmer=units[0],hands=units[1:])
                # Tomatoes are cash produce, never a feed or route input. Sell
                # only observed shed stock beyond any parent's existing sale.
                stock=int(private['shed'].get('TOMATO',0))
                scheduled=sum(int(o[2]) for o in action.get('market',[]) if len(o)>=3 and o[:2]==['SELL','TOMATO'])
                action=_alt_sell_extra(action,'TOMATO',max(0,stock-scheduled))
    except Exception:
        _ALT_REPORT['extension_errors']+=1
    state['step']=step
    return action
agent.telemetry=_ALT_REPORT
agent=globals().pop('agent')


# Shared I1: extend the temporary wheat crop by one growth refresh.
_ASTRA_I1_PARENT = agent
_ASTRA_I1_INSTALL = _alt_install
_ASTRA_I1_REPORT = dict(installed=0, harvested_units=0, delivered_units=0,
                        pasture_restored=0, sale_units=0, errors=0)
_ASTRA_I1_STATE = {}


def _alt_install(mode):
    _ASTRA_I1_INSTALL(mode)
    if mode != 'HybridOpening':
        return
    tape = _IMPL.chassis.routes[0]
    try:
        expected = [['HARVEST'], ['BUILD_PASTURE'], ['EAST'], ['EAST'], ['DROP']]
        assert [tape[s]['hands'][0] for s in range(53, 58)] == expected
        assert all(tape[s]['hands'][0] == ['PASS'] for s in range(84, 92))
        # Build all replacements before mutating the runtime route.
        replacement = {s: copy.deepcopy(tape[s]) for s in list(range(53, 58)) + list(range(84, 92))}
        for s in range(53, 58):
            replacement[s]['hands'][0] = ['PASS']
        commands = [['EAST'], ['EAST'], ['WATER'], ['HARVEST'],
                    ['BUILD_PASTURE'], ['EAST'], ['EAST'], ['DROP']]
        for s, command in zip(range(84, 92), commands):
            replacement[s]['hands'][0] = command
        for s, action in replacement.items():
            tape[s] = action
        _ASTRA_I1_REPORT['installed'] += 1
    except Exception:
        _ASTRA_I1_REPORT['errors'] += 1


def agent(observation, configuration=None):
    step = int(observation['step'])
    seat = int(observation['player'])
    if step == 0:
        for key in _ASTRA_I1_REPORT:
            _ASTRA_I1_REPORT[key] = 0
        _ASTRA_I1_STATE.clear()
    action = _ASTRA_I1_PARENT(observation, configuration)
    try:
        if _ALT_STATE[seat]['mode'] != 'HybridOpening' or not _ASTRA_I1_REPORT['installed']:
            return action
        state = _ASTRA_I1_STATE.setdefault(seat, {})
        private = observation['private']
        farm = observation['farms'][seat]
        cargo = int(private['inventories'][1].get('WHEAT', 0)) if len(private['inventories']) > 1 else 0
        if step == 87 and action['hands'][0] == ['HARVEST']:
            state['preharvest'] = cargo
        if step == 88 and 'preharvest' in state:
            _ASTRA_I1_REPORT['harvested_units'] = max(0, cargo - state['preharvest'])
        if step == 89:
            tile = farm['tiles'][4][2]
            _ASTRA_I1_REPORT['pasture_restored'] = int(isinstance(tile, dict) and tile.get('kind') == 'PASTURE')
        if step == 92 and 'predicted_delivery' in state:
            _ASTRA_I1_REPORT['delivered_units'] = min(state['predicted_delivery'], max(0, state['predrop'] - cargo))
        if step != 91 or action['hands'][0] != ['DROP'] or tuple(farm['hands'][0]) != (4, 4):
            return action
        _, projected = _r127_fields(observation, action)
        delivered = max(0, cargo - int(projected['inventories'][1].get('WHEAT', 0)))
        state['predrop'] = cargo
        state['predicted_delivery'] = delivered
        scheduled = sum(max(0, int(o[2])) for o in action.get('market', [])
                        if len(o) >= 3 and o[:2] == ['SELL', 'WHEAT'])
        extra = min(delivered, max(0, int(projected['shed'].get('WHEAT', 0)) - scheduled))
        if not extra:
            return action
        changed = _alt_sell_extra(action, 'WHEAT', extra)
        if changed is not action:
            _ASTRA_I1_REPORT['sale_units'] += extra
        return changed
    except Exception:
        _ASTRA_I1_REPORT['errors'] += 1
        return action


agent.telemetry = _ASTRA_I1_REPORT
agent = globals().pop('agent')
kaggle_submission_agent = agent

