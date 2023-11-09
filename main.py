from simulator import Simulator

def main():
    sim = Simulator(
        mass=10,
        energy=1,
        angular_momentum=1,
        starting_distance=30,
        starting_angle=3.14/2,
        starting_speed=10
    )
    
    sim.simulate()
    sim.show(display_size=(800, 800), time_scale=10)


if __name__ == '__main__':
    main()