import cellular_automaton as ca

mc = ca.MainCycle(
    (70, 70),
    borders=False,
    update_frequency=20,
    forced_render=False,
    render_frequency=20,
)

mc.run()
