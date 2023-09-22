import numpy as np
import pygame
import random

class Simulator:
    def __init__(self, mass: float,
                 energy: float,
                 angular_momentum: float,
                 starting_distance: float,
                 starting_angle: float,
                 starting_speed: float,
                 dtau: float = 1 / 100,
                 black_hole_radius: float = 5) -> None:
        """Class that simulates a body being thrown into a black hole

        Args:
            mass (float): mass of the object
            energy (float): mechanical energy of the object
            angular_momentum (float): angular momentum of the object
            starting_distance (float): starting distance between the object and the black hole
            starting_angle (float): starting angle between the object and the black hole, expressed in radiants
            starting_speed (float): starting speed of the object (angolo ???)
            dtau (float, optional): time step for the simulation. Defaults to 1/100.
            black_hole_radius (float, optional): radius of the black hole. Defaults to 10.
        """
                
        self.MASS = mass
        self.ENERGY = energy
        self.ANGULAR_MOMENTUM = angular_momentum
        
        self.DTAU = dtau
        self.BLACK_HOLE_RADIUS = black_hole_radius
        
        self.distances = [starting_distance]
        self.angles = [starting_angle]
        self.speeds = [starting_speed]
        self.times = [0]
        self.light_speed = 1
        
    def initialize_drawing_variables(self) -> None:
        """Initializes a bunch of stuff as instance variables because, quite frankly, I could not be bothered to make specific functions for everything
        """
        self.display_x, self.display_y = self.display_size = self.display_size
        self.h_display_x, self.h_display_y = self.display_x // 2, self.display_y // 2
        
        self.stars_number = round(self.display_x * self.display_y * self.star_density)  # Number of stars
        self.black_hole_display_size = self.BLACK_HOLE_RADIUS * self.scale    # Black hole size in pixels
        
        if self.do_daddy_pig:
            self.daddy_pig = pygame.image.load('black_hole.jpg')   # Loads daddy pig (hilarious)
            self.daddy_pig = pygame.transform.scale(self.daddy_pig, 2*[self.black_hole_display_size])   # Scales daddy pig (hilarious)
            pygame.mixer.init()
            pygame.mixer.music.load('music.mp3')
        
        if self.do_animation:
            self.stars_per_frame = round(self.stars_number / (2 * self.fps))
        else:
            self.stars_per_frame = self.stars_number
            
        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(self.display_size)
        self.clock = pygame.time.Clock()
        font = pygame.font.Font('freesansbold.ttf', 32)
        
        self.start_text = font.render('CLICK TO START', True, 'white')
        self.text_rect = self.start_text.get_rect()
        self.text_rect.center = (self.h_display_x, self.h_display_y)

        self.xs = self.h_display_x + self.distances * np.cos(self.angles) * self.scale
        self.ys = self.h_display_y - self.distances * np.sin(self.angles) * self.scale
        
        self.simulation_steps_index = 0
        self.stars_index = 0
        self.simulation_steps_per_frame = round(self.time_scale / (self.fps * self.DTAU)) # Number of DTAU timesteps per frame
        self.state = 'click_to_start'
        self.clicked = False
        
        
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


    def show(self,
             display_size: tuple[int, int] = None,
             fps: float = None,
             scale: float = 10,
             time_scale: float = 1,
             star_density: float = 1 / 1000,
             star_dimension_range: tuple[int, int] = (1,3),
             do_animation: bool = True,
             do_daddy_pig: bool = False) -> None:
        """Shows the result of the simulation via matplotlib (run Simulator.simulate() first)
        
        Args:
            display_size (tuple[int, int], optional): size of the display, if None it will fit the starting distance. Defaults to None.
            self.fps (float, optional): frames per second, if None then 1 / DTAU. Defaults to None.
            scale (float, optional): self.screen scaling in pixels / meters. Defaults to 10.
            self.time_scale (float, optional): how fast the time goes in the animation. Defaults to 1.
            star_density (float, optional): stars / square pixels. Defaults to 1 / 1000.
            star_dimension_range (tuple[int, int], optional): range of possible stars dimensions. Defaults to (1, 3).
            do_animation (bool, optional): if True, stars and black hole appear with an animation. Defaults to True.
            do_daddy_pig (bool, optional): find out :). Defaults to False.
        """
        # Inits args and stuff
        if display_size is None:
            display_size = (self.distances[0] * scale * 2.4, self.distances[0] * scale * 2.4)

        if fps is None:
            fps = 1 / self.DTAU

        self.display_size = display_size
        self.fps = fps
        self.scale = scale
        self.time_scale = time_scale        
        self.star_density = star_density
        self.star_dimension_range = star_dimension_range
        self.do_animation = do_animation
        self.do_daddy_pig = do_daddy_pig
        
        self.initialize_drawing_variables()
        
        # Game Loop
        running = True
        while running:
            # Resets the click
            if self.clicked:
                self.clicked = False
            
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
            
            # State checks
            match self.state:
                case 'click_to_start':
                    self.click_to_start()
                        
                case 'drawing_stars':
                    self.draw_stars()
                        
                case 'drawing_black_hole':
                    self.draw_black_hole()
                        
                case 'drawing_simulation':
                    self.draw_simulation()
            
            # Locks FPS
            self.clock.tick(self.fps)
            # Updates the caption
            pygame.display.set_caption(f'self.fps: {self.clock.get_fps():.0f}/{self.fps:.0f}, Time x{round(self.time_scale, 2)}')      

                    
        # If not running (e.g. closed the window) tell pygame to stop doing its thing
        pygame.quit()


    def click_to_start(self) -> None:
        """Called when drawing the click to start panel
        """
        self.screen.fill('darkblue')
        self.screen.blit(self.start_text, self.text_rect)
        pygame.display.flip()
        
        if self.clicked:
            self.screen.fill('darkblue')
            pygame.display.flip()
            self.state = 'drawing_stars'
            
    
    def draw_stars(self) -> None:
        """Called when drawing the stars
        """
        for _ in range(self.stars_per_frame):
            if not self.stars_index < self.stars_number:
                self.stars_index = 0
                self.state = 'drawing_black_hole'
                break
            
            pos = (random.randint(0, self.display_x), random.randint(0, self.display_y))
            pygame.draw.circle(self.screen, 'white', pos, random.randint(*self.star_dimension_range))
            
            self.stars_index += 1
        
        pygame.display.flip()
    
    
    def draw_black_hole(self) -> None:
        """Called when drawing the black hole
        """
        pygame.draw.circle(self.screen, 'black', (self.h_display_x, self.h_display_y), self.black_hole_display_size)
        
        # Shows & plays daddy pig (hilarious)
        if self.do_daddy_pig:
            daddy_pig_pos = ((self.display_x - self.black_hole_display_size) // 2, (self.display_y - self.black_hole_display_size) // 2)
            self.screen.blit(self.daddy_pig, daddy_pig_pos)
            pygame.mixer.music.play(-1)
            
        pygame.display.flip()
        
        self.state = 'drawing_simulation'
    
    
    def draw_simulation(self) -> None:
        """Called when drawing the simulation
        """
        for _ in range(self.simulation_steps_per_frame):
            p = (self.xs[round(self.simulation_steps_index)],
                self.ys[round(self.simulation_steps_index)])
            
            pygame.draw.circle(self.screen, 'orange', p, 2)  
            pygame.display.flip()
            
            self.simulation_steps_index += 1
        
            if not self.simulation_steps_index < len(self.distances):
                self.running_animation = False
                self.simulation_steps_index = 0
                self.state = 'click_to_start'
                pygame.mixer.music.fadeout(1500)
                pygame.time.wait(1500)
                break
    
    
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