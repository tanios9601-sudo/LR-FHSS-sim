# -*- coding: utf-8 -*-
"""
Simulation LR-FHSS avec distribution mixte de headers
"""
from lrfhss.lrfhss_core import *
from lrfhss.acrda import BaseACRDA
from lrfhss.settings import Settings
import simpy
import numpy as np


def run_sim_mixed(base='acrda', number_nodes=50000//8, seed=0,
                  simulation_time=3600, payload_size=10,
                  code='1/3', obw=35, p=0.5):
    """
    Lance une simulation avec p*100% des noeuds à 2 headers
    et (1-p)*100% à 3 headers.
    """
    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()

    n2 = int(p * number_nodes)
    n3 = number_nodes - n2

    # Settings pour le groupe 2 headers
    s2 = Settings(
        number_nodes    = n2,
        simulation_time = simulation_time,
        payload_size    = payload_size,
        headers         = 2,
        code            = code,
        obw             = obw,
        base            = base
    )

    # Settings pour le groupe 3 headers
    s3 = Settings(
        number_nodes    = n3,
        simulation_time = simulation_time,
        payload_size    = payload_size,
        headers         = 3,
        code            = code,
        obw             = obw,
        base            = base
    )

    # Créer la gateway
    if base == 'acrda':
        avg_toa = (s2.time_on_air + s3.time_on_air) / 2
        bs = BaseACRDA(obw, s2.window_size, s2.window_step, avg_toa, s2.threshold)
        env.process(bs.sic_window(env))
    else:
        bs = Base(obw, s2.threshold)

    nodes = []

    # Groupe 1 : p% avec 2 headers
    for i in range(n2):
        node = Node(
            s2.obw, s2.headers, s2.payloads,
            s2.header_duration, s2.payload_duration,
            s2.transceiver_wait, s2.traffic_generator
        )
        bs.add_node(node.id)
        nodes.append(node)
        env.process(node.transmit(env, bs))

    # Groupe 2 : (1-p)% avec 3 headers
    for i in range(n3):
        node = Node(
            s3.obw, s3.headers, s3.payloads,
            s3.header_duration, s3.payload_duration,
            s3.transceiver_wait, s3.traffic_generator
        )
        bs.add_node(node.id)
        nodes.append(node)
        env.process(node.transmit(env, bs))

    env.run(until=simulation_time)

    success     = sum(bs.packets_received.values())
    transmitted = sum(n.transmitted for n in nodes)

    return success / transmitted if transmitted > 0 else 1.0


if __name__ == "__main__":

    NUMBER_NODES    = 150000 // 8
    SIMULATION_TIME = 3600
    CODE            = '1/3'

    # =========================================================
    # Modifiez p ici : proportion de noeuds avec 2 headers
    # p=0.0  → 100% headers=3
    # p=0.5  → 50% headers=2, 50% headers=3 (optimal article)
    # p=1.0  → 100% headers=2
    # =========================================================
    P = 0.25

    print(f"N={NUMBER_NODES} | code={CODE} | sim_time={SIMULATION_TIME} sec")
    print(f"Distribution : p2={P:.2f} × 2 headers + p3={1-P:.2f} × 3 headers")
    print("-" * 55)

    for base in ['core', 'acrda']:
        result = run_sim_mixed(
            base            = base,
            number_nodes    = NUMBER_NODES,
            simulation_time = SIMULATION_TIME,
            code            = CODE,
            p               = P
        )
        print(f"base={base:<5} | p2={P:.2f} p3={1-P:.2f} | Prob succès = {result:.6f}")