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
            [500, 0, 40, 1148],
            [1508, 900, 40, 1148],
            [540, 300, 750, 40],
            [758, 1708, 750, 40]
        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        obs_rectangle = [
            [40, 40, 150, 1968],
            [40, 40, 460, 150],
            [350, 40, 150, 1108],
            [350, 1148, 340, 150],
            [540, 340, 150, 808],
            [540, 340, 750, 150],
            [540, 150, 750, 150],
            [1290, 150, 150, 340],
            [540, 40, 150, 260],
            [540, 40, 1468, 150],
            [1858, 40, 150, 1968],
            [40, 1858, 1468, 150],
            [1548, 1858, 460, 150],
            [1548, 900, 150, 1108],
            [1358, 1290, 150, 260],
            [1358, 900, 150, 808],
            [1358, 750, 340, 150],
            [758, 1748, 750, 150],
            [758, 1558, 750, 150],
            [608, 1558, 150, 340]

        ]
        return obs_rectangle

    @staticmethod
    def obs_circle():
        obs_cir = [

        ]

        return obs_cir