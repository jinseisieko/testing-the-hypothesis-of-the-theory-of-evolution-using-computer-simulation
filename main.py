import cellular_automaton as ca

ca.MainCycle(
    (200, 100),
    borders=False,
    update_frequency=20,
    forced_render=False,
    render_frequency=20,
).run()
