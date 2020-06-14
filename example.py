import simulator
import os
import json
import math


isolation_day = 2
confine_day = 2
quarantine_day = 2

def compute_score(I, Q):
    theta_i = 1000.0
    theta_q = 100000.0
    q_w = 1.0

    return math.exp(I*1.0/theta_i) + q_w * math.exp(Q*1.0/theta_q)

lambda_h = 1.0
lambda_i = 0.5
lambda_q = 0.3
lambda_c = 0.2


I = 0
Q = 0
infected_set = set()
treated_set = set()
period = 840

engine = simulator.Engine(thread_num=1, write_mode="append", specified_run_name="test")

engine.reset()
for i in range(period):


    I = len(infected_set)
    if i%14 == 0:
        #Compute current score
        for user_id in range(10000):
            infection_state = engine.get_individual_infection_state(user_id)
            if infection_state  == 3 or infection_state == 4:
                infected_set.add(user_id)

                visited_history = engine.get_individual_visited_history(user_id)

                residental_acq = engine.get_individual_residential_acq(user_id)
                working_acq = engine.get_individual_working_acq(user_id)

                #isolate the acq
                for acq_id in residental_acq:
                    if engine.get_individual_intervention_state(acq_id) == 1:
                        engine.set_individual_isolate_days({acq_id: isolation_day})
                for acq_id in working_acq:
                    if engine.get_individual_intervention_state(acq_id) == 1:
                        engine.set_individual_isolate_days({acq_id: isolation_day})


            if (infection_state == 3 or infection_state == 4):
                if engine.get_individual_intervention_state(user_id) < 5:
                    #hospitalize user
                    treated_set.add(user_id)
                    engine.set_individual_to_treat({user_id: True})


        print(len(infected_set), "*******************************")
        Q += lambda_h * engine.get_hospitalize_count()
        Q += lambda_i * engine.get_isolate_count()
        Q += lambda_q * engine.get_quarantine_count()
        Q += lambda_c * engine.get_confine_count()
    score = compute_score(I, Q)
    print("Score = ", score)
    print("+++++++++++++++++++++++++++")
    engine.next_step()
    engine.get_current_time()
    
    


    # engine.get_individual_visited_history(1)
    # engine.get_individual_infection_state(1)
    # engine.get_individual_visited_history(1)
    # engine.get_area_infected_cnt(1)

    # engine.set_individual_confine_days({1: 5}) # {individualID: day}
    # engine.set_individual_quarantine_days({2: 5}) # {individualID: day}
    # engine.set_individual_isolate_days({3: 5}) # {individualID: day}
    # engine.set_individual_to_treat({4: True}) # {individualID: day}

del engine


