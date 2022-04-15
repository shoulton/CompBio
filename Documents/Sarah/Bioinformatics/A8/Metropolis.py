import argparse
import numpy as np
import scipy
from scipy import stats
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-o",required=True, type=str, help="Name of the output file")
args = parser.parse_args()

np.random.seed(3)

def ifelse(size, yes, no):
    y = []
    test = scipy.stats.uniform.rvs(size=size)
    for i in range(len(test)):
        if test[i] < 0.2:
            y.append(yes[i])
        else:
            y.append(no[i])
    return y


#generate data
N = 100
n = np.asarray(scipy.stats.poisson.rvs(50, size=N))
y1 = scipy.stats.binom.rvs(n, 0.6, size=N)
y2 = scipy.stats.binom.rvs(n, 0.1, size=N)
y = np.asarray(ifelse(N, y1, y2))

#===================================

def logpost(theta):
    lamb = float(theta[0])
    p1 = float(theta[1])
    p2 = float(theta[2])
    if ( lamb >= 1 or p1 > 1 or p2 >= 1 or lamb <= 0 or p1 <= 0 or p2 < 0 or p1 < p2):
        return (-999999)

    one = lamb*p1**y
    two = (1-p1)**(n-y)
    three = (1-lamb)*p2**y
    four = (1-p2)**(n-y)
    log = np.log(one * two + three * four)
    return sum(log)

#===================================

def proposal(theta):
    rand = scipy.stats.norm.rvs(size=3)
    mult = np.multiply(rand, (0.01, 0.01, 0.01))
    new = theta + mult
    return new

#===================================

NREP = 3000
## starting values
lamb = 0.2
p1 = 0.6
p2 = 0.3
mchain = np.empty((NREP, 3))
mchain[:] = np.nan

#===================================
theta = mchain[0]

mchain[0] = theta = [lamb, p1, p2]
acc = 0
for i in range(1, NREP):
    thetaCandidate = proposal(theta)
    alpha = logpost(thetaCandidate) - logpost(theta)
    ran = scipy.stats.uniform.rvs(size=1)
    if ran <= np.exp(alpha):
        acc = acc + 1
        theta = thetaCandidate
    mchain[i] = theta

#===================================

accept_ratio = acc/NREP
print("Acceptance Ratio: " + str(accept_ratio))
y_axis = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
x_axis = [0, 500, 1500, 2500]
figure, axis = plt.subplots(1,3, figsize=(15, 7))
axis[0].plot(mchain[100:, 0])
axis[0].set_title("Lambda")
axis[0].set_xlabel("Index")
axis[0].set_ylabel("mchain[100:, 0]")
axis[0].set_yticks(y_axis)
axis[0].set_xticks(x_axis)
axis[1].plot(mchain[100:, 1])
axis[1].set_title("P1")
axis[1].set_xlabel("Index")
axis[1].set_ylabel("mchain[100:, 1]")
axis[1].set_yticks(y_axis)
axis[1].set_xticks(x_axis)
axis[2].plot(mchain[100:, 2])
axis[2].set_title("P2")
axis[2].set_xlabel("Index")
axis[2].set_ylabel("mchain[100:, 2]")
axis[2].set_yticks(y_axis)
axis[2].set_xticks(x_axis)
figure.tight_layout(pad=3.0)
plt.savefig(args.o)

print('Lambda Mean:', round(np.mean(mchain[100:NREP,0]), 3))
print('p1 Mean:', round(np.mean(mchain[100:NREP,1]), 3))
print('p2 Mean:', round(np.mean(mchain[100:NREP,2]), 3))