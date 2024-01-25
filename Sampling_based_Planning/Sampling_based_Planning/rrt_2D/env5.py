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
            [660, 0, 40, 1468],
            [1348, 580, 40, 1468]

        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        obs_rectangle = [
            [40, 40, 150, 1968],
            [40, 40, 620, 150],
            [510, 40, 150, 1428],
            [700, 40, 150, 1428],
            [510, 1468, 340, 150],
            [700, 40, 1308, 150],
            [1858, 40, 150, 1968],
            [1388, 1858, 620, 150],
            [1388, 580, 150, 1428],
            [1198, 580, 150, 1428],
            [1198, 430, 340, 150],
            [40, 1858, 1308, 150]


        ]
        return obs_rectangle

    @staticmethod
    def obs_circle():
        obs_cir = [

        ]

        return obs_cir