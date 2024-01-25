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
            [0, 0, 190, 2048],
            [0, 0, 2048, 190],
            [1858, 0, 190, 2048],
            [0, 1858, 2048, 190]
        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        obs_rectangle = [
            [350, 0, 340, 1298],
            [540, 190, 900, 300],
            [608, 1558, 900, 340],
            [1358, 750, 340, 1298]

        ]
        return obs_rectangle

    @staticmethod
    def obs_circle():
        obs_cir = [

        ]

        return obs_cir