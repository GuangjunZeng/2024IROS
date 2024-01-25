"""
Environment for rrt_2D
@author: huiming zhou
"""


class Env:
    def __init__(self):
        self.x_range = (0, 2048)
        self.y_range = (0, 2048)
        self.obs_boundary = self.obs_boundary()
        self.obs_circle = self.obs_circle()
        self.obs_rectangle = self.obs_rectangle()

    @staticmethod
    def obs_boundary():
        obs_boundary = [
            [0, 0, 40, 2048],
            [0, 0, 2048, 40],
            [2008, 0, 40, 2048],
            [0, 2008, 2048, 40],
        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        obs_rectangle = [
            [500, 0, 40, 1148],
            [1508, 900, 40, 1148],
            [540, 300, 750, 40],
            [758, 1708, 750, 40]

        ]
        return obs_rectangle

    @staticmethod
    def obs_circle():
        obs_cir = [

        ]

        return obs_cir