import random
import io
import math
import matplotlib.pyplot as plt
from samila import GenerativeImage
from samila import Projection


class graph_generator:
    """
    This class contains various methods to generate different kind of art through various mathematical ways
    """

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

    def generate_from_samila(self) -> io:
        """
        This method generates random art using the library samila
        """
        
        # Method 1 to generate a random uniform destribution
        def f1(x, y):
            result = random.uniform(-2, 3) * x**2  - math.sin(y**2) + abs(y-x)
            return result

        # Method 2 to generate a random uniform destribution
        def f2(x, y):
            result = random.uniform(-3, 1) * y**3 - math.cos(x**2) + 2*x
            return result

        g = GenerativeImage(f1, f2)

        projection = Projection.RECTILINEAR if random.random() > 0.3 else Projection.POLAR

        if projection == Projection.POLAR:
            start = -1.2
            step = random.randrange(40, 100, 1) / 10000
            stop = 0
        else:
            start=random.randrange(-4, 0, 1)
            step=random.randrange(90, 200, 1) / 10000
            stop=random.randrange(0, 5, 1)

        g.generate() if random.random() > 0.8 else g.generate(start=start*math.pi, step=step, stop=stop)

        g.size = [self.width, self.height]
        g.plot(color="white", bgcolor="black", projection=projection, spot_size=0.5)

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='jpg')
        # self.g.save_image(img_buf)

        return img_buf