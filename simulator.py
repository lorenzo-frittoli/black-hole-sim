import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Simulator:
    def __init__(self, mass: float, energy: float, angular_momentum: float, starting_distance: float, starting_angle: float, starting_speed: float) -> None:
        self.MASS = mass
        self.ENERGY = energy
        self.ANGULAR_MOMENTUM = angular_momentum
        
        self.DTAU = 1/1000  # Tau derivative step
        self.BLACK_HOLE_RADIUS = 2

        self.distances = [starting_distance]
        self.angles = [starting_angle]
        self.speeds = [starting_speed]
        self.times = [0]
        self.light_speed = 1   #speed of light
        
    
    def get_dr_dtau(self, speed: float) -> float:
        """Gets the derivative of r (distance) with respect to tau (relative time)

        Args:
            speed (float): speed to calculate the derivative at

        Returns:
            float: derivative of r (distance) with respect to tau (relative time)
        """
        return speed

    def get_dv_dtau(self, distance: float) -> float:
        """Gets the derivative of v (speed) with respect to tau (relative time)

        Args:
            distance (float): distance to calculate the derivative at

        Returns:
            float: derivative of v (speed) with respect to tau (relative time)
        """
        return self.ANGULAR_MOMENTUM*2 / distance**3 - self.MASS * self.light_speed**2 / distance**2 - (3 * self.ANGULAR_MOMENTUM**2 * self.MASS) / distance**4
    
    
    def get_dt_dtau(self, distance: float) -> float:
        """Gets the derivative of t (absolute time) with respect to tau (relative time)

        Args:
            distance (float): distance to calculate the derivative at

        Returns:
            float: derivative of t (absolute time) with respect to tau (relative_time)
        """
        return self.ENERGY / (1 - (2 * self.MASS / distance))


    def get_dphi_dtau(self, distance: float) -> float:
        """Gets the derivative of phi (angle) with respect to tau (relative time)

        Args:
            distance (float): distance to calculate the derivative at

        Returns:
            float: derivative of phi (angle) with respect to tau (relative time)
        """
        return self.ANGULAR_MOMENTUM / distance ** 2

   
    def simulate(self) -> None: 
        """Runs the simulation and updates the internal values
        """
        while self.distances[-1] > self.BLACK_HOLE_RADIUS:  # Until the particle crashes into the black hole
            # Derivatives
            dr_dtau = self.get_dr_dtau(self.speeds[-1])
            dv_dtau = self.get_dv_dtau(self.distances[-1])
            dphi_dtau = self.get_dphi_dtau(self.distances[-1])
            dt_dtau = self.get_dt_dtau(self.distances[-1])
            
            # new val = old val + dval/dtau * dtau
            self.speeds.append(self.speeds[-1] + dv_dtau * self.DTAU)
            self.distances.append(self.distances[-1] + dr_dtau * self.DTAU)
            self.angles.append(self.angles[-1] + dphi_dtau * self.DTAU)
            self.times.append(self.times[-1] + dt_dtau * self.DTAU)


    def show(self) -> None:
        """Shows the result of the simulation via matplotlib (run Simulator.simulate() first)
        """
        plt.plot(self.distances * np.cos(self.angles), self.distances * np.sin(self.angles))
        black_hole = plt.Circle((0,0), self.BLACK_HOLE_RADIUS, color='black')
        ax = plt.gca()
        ax.add_patch(black_hole)
        plt.show()
        
        
    # def animate(self) -> None:
    #     """Shows the result of the simulation via matplotlib (run Simulator.simulate() first)
    #     """
    #     xs = self.distances * np.cos(self.angles)
    #     ys = self.distances * np.sin(self.angles)
        
    #     fig, ax = plt.subplots()
    #     black_hole = plt.Circle((0,0), self.BLACK_HOLE_RADIUS, color='black')

    #     def update(n):
    #         ax.cla()
    #         ax.add_patch(black_hole)

    #         ax.plot(xs[:n], ys[:n])

    #         return fig,
        
    #     anim = FuncAnimation(fig = fig, func = update, frames = len(xs)/10, interval = 1, repeat = False)
    #     anim.save("a.gif", fps=10)
    #     plt.show()