from simulator import Simulator

def main():
    sim = Simulator(
        mass = 1,
        energy = 2,
        angular_momentum = 15,
        starting_distance = 30,
        starting_angle = 3.14,
        starting_speed = 0
    )
    
    sim.simulate()
    sim.animate()


if __name__ == '__main__':
    main()