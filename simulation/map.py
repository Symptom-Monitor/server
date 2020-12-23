import matplotlib.cm as cm
import numpy as np
from PIL import Image
import imageio
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import uuid
import os

def simulate(x, y, alpha, beta, gamma):
  img = Image.open('./public/population-density.png')
  width = img.size[0]//6
  height = img.size[1]//6
  img = img.resize((width, height)) 
  img = 255 - np.asarray(img)

  S_0 = img[:,:,1]
  I_0 = np.zeros_like(S_0)
  I_0[int(height * y), int(width * x)] = 1

  R_0 = np.zeros_like(S_0)

  T = 900                         # final time
  dt = 1                          # time increment
  N = int(T/dt) + 1               # number of time-steps
  t = np.linspace(0.0, T, N)      # time discretization

  # initialize the array containing the solution for each time-step
  u = np.empty((N, 3, S_0.shape[0], S_0.shape[1]))
  u[0][0] = S_0
  u[0][1] = I_0
  u[0][2] = R_0

  theCM = cm.get_cmap("Reds")
  theCM._init()
  alphas = np.abs(np.linspace(0, 1, theCM.N))
  theCM._lut[:-3,-1] = alphas


  # Compute data
  for n in range(N-1):
      u[n+1] = euler_step(u[n], f, dt, beta, gamma, alpha)

  keyFrames = []
  frames = 60.0 # upper limit on keyframes

  for i in range(0, N-1, int(N/frames)):
    fig = Figure()
    fig.figimage(img, resize=True)
    fig.figimage(u[i][1], vmin=0, cmap=theCM)

    canvas = FigureCanvas(fig)
    canvas.draw()

    rows, cols = canvas.get_width_height()

    keyFrames.append(np.fromstring(canvas.tostring_rgb(), dtype=np.uint8).reshape(cols, rows, 3))

  # Couldn't figure out a way to use BytesIO directly
  p = os.path.join(os.getenv('DATA_DIR'), "generated", uuid.uuid4().hex + ".mp4")

  imageio.mimsave(p, keyFrames, fps=5)

  return p

# Approximate curve
def euler_step(u, f, dt, beta, gamma, alpha):
    return u + dt * f(u, beta, gamma, alpha)

# Compute at point
def f(u, beta, gamma, alpha):
    S = u[0]
    I = u[1]
    R = u[2]

    new = np.array([-beta*(S[1:-1, 1:-1]*I[1:-1, 1:-1]),
                     beta*(S[1:-1, 1:-1]*I[1:-1, 1:-1]) - gamma*I[1:-1, 1:-1] + \
                     alpha*(-4* I[1:-1, 1:-1] + \
                            I[0:-2, 1:-1] + \
                            I[2:, 1:-1] + \
                            I[1:-1, 0:-2] + \
                            I[1:-1, 2:]),
                     gamma*I[1:-1, 1:-1]
                    ])
    
    padding = np.zeros_like(u)
    padding[:,1:-1,1:-1] = new
    padding[0][padding[0] < 0] = 0
    padding[0][padding[0] > 255] = 255
    padding[1][padding[1] < 0] = 0
    padding[1][padding[1] > 255] = 255
    padding[2][padding[2] < 0] = 0
    padding[2][padding[2] > 255] = 255
    
    return padding
