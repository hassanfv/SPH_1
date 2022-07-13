
# Try to create a sphere with REALLY a uniform density with rho_0 = 'predifined'

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import time
np.random.random(42)
import pickle
from libsx import *
import time

np.random.seed(42)

TA = time.time()


res = []
count = 0

N = 10000

while count < N:

	x = 1. - 2. * np.random.random()
	y = 1. - 2. * np.random.random()
	z = 1. - 2. * np.random.random()

	if (x**2 + y**2 + z**2)**0.5 <= 1.:
		res.append([x, y, z])
		count += 1

print('Total number of particles inside the sphere = ', count)

res = np.array(res)

x = res[:, 0]
y = res[:, 1]
z = res[:, 2]

plt.scatter(res[:, 0], res[:, 1], s = 0.05, color = 'k')
plt.show()

N = res.shape[0]


M_sun = 1.989e33 # gram
grav_const_in_cgs = 6.67259e-8 #  cm3 g-1 s-2
UnitMass_in_g = 2.21 * M_sun       # !!!!!!!!!!!!!!!!!!!!!!!!! CHANGE !!!!!!!!!!!!!!!!!
#rB = 0.8 # pc
#ksi = 3.
R_0 = 0.97 #rB/ksi
UnitRadius_in_cm = R_0 * 3.086e18 # cm (2.0 pc)    #!!!!!!!!!!!!!! CHANGE !!!!!!!!!!!!!!!!!!
UnitDensity_in_cgs = UnitMass_in_g / UnitRadius_in_cm**3
Unit_u_in_cgs = grav_const_in_cgs * UnitMass_in_g / UnitRadius_in_cm
Unit_P_in_cgs = UnitDensity_in_cgs * Unit_u_in_cgs
unitVelocity = (grav_const_in_cgs * UnitMass_in_g / UnitRadius_in_cm)**0.5

unitTime = (UnitRadius_in_cm**3/grav_const_in_cgs/UnitMass_in_g)**0.5
unitTime_in_yr = unitTime / 3600. / 24. / 365.25
unitTime_in_Myr = unitTime / 3600. / 24. / 365.25 / 1.e6

print('unitTime_in_Myr = ', unitTime_in_Myr)
print('unitVelocity = ', unitVelocity)
print('UnitMass_in_g = ', UnitMass_in_g)
print('UnitDensity_in_cgs = ', UnitDensity_in_cgs)

G = grav_const_in_cgs

Mcld = UnitMass_in_g
Rcld = R_0

#---- Speed of Sound ------
mH = 1.6726e-24 # gram
kB = 1.3807e-16  # cm2 g s-2 K-1
T_0 = 54. # K, see Table_1 in Anathpindika - 2009 - II

# Note that for pure molecular hydrogen mu=2. For molecular gas with ~10% He by mass and trace metals, mu ~ 2.7 is often used.
muu = 2.7
mH2 = muu * mH

c_0 = (kB * T_0 / mH2)**0.5

print('Sound speed (cm/s) = ', c_0)
print('Sound speed (m/s) = ', c_0/100.)
print('Sound speed (km/s) = ', c_0/100000.)
print()
#--------------------------


#------- Prepare the IC to output -------

#m = 3. * Mcld / 4./np.pi/Rcld**3/N + np.zeros(N)
m = np.ones(N) / N
print('m = ', np.sort(m))

rho_0 = 1.3024e-21 #g/cm^3
rho_0 = rho_0 / UnitDensity_in_cgs

r_arr = (x*x + y*y + z*z)**0.5

res2 = []

for i in range(N):

	xt = x[i]
	yt = y[i]
	zt = z[i]

	rtmp = (xt*xt +yt*yt + zt*zt)**0.5
	nnt = np.where(r_arr <= rtmp)[0]
	
	# calculating the corresponding theta & phi
	theta = np.arccos(zt/rtmp) # the angle from z-axis
	phi = np.arctan(yt/xt)
	
	if (xt < 0.) & (yt > 0.):
		phi += np.pi
	
	elif (xt < 0.) & (yt < 0.):
		phi += np.pi
	
	elif (xt > 0.) & (yt < 0.):
		phi += 2.*np.pi
	
	M_r_dist = np.sum(m[nnt]) # the mass within a sphere of radius <= rtmp.
	
	r_dist = (3./4./np.pi/rho_0 * M_r_dist)**(1./3.)
	
	# Reconstructing the updated coordinate:
	x_dist = r_dist * np.cos(phi) * np.sin(theta)
	y_dist = r_dist * np.sin(phi) * np.sin(theta)
	z_dist = r_dist * np.cos(theta)

	res2.append([x_dist, y_dist, z_dist])

res2 = np.array(res2)

with open('IC_rho_0.pkl', 'wb') as f:
	pickle.dump(res2, f)

plt.scatter(res2[:, 0], res2[:, 1], s = 0.05, color = 'k')
plt.show()

s()




m = np.ones(N) / N
h = do_smoothingX((res, res)) # We don't save this one as this is the h for only one of the clouds.
rho = getDensity(res, m, h)

print('rho = ', np.sort(rho)*UnitDensity_in_cgs)
#print('mean(rho) = ', np.mean(rho)*UnitDensity_in_cgs)

hB = np.median(h) # the two clouds will be separated by 2*hB

res2 = res.copy()
res2[:, 0] += (2.*1.0 + 2.*hB) # 1.0 is the radius of the cloud !

res12 = np.vstack((res, res2))

Mach = 3.
vel_ref = Mach * c_0 # The speed of each cloud. Note that the clouds are in a collision course so v1 = -v2.

v_cld_1 = np.zeros_like(res)
v_cld_2 = v_cld_1.copy()

v_cld_1[:, 0] = vel_ref
v_cld_2[:, 0] = -vel_ref

vel = np.vstack((v_cld_1, v_cld_2))

xx, yy = res12[:, 0], res12[:, 1]

print()
print(res12.shape)

print('Elapsed time = ', time.time() - TA)

plt.figure(figsize = (14, 6))
plt.scatter(xx, yy, s = 1, color = 'k')
plt.show()

#---- Output to a file ------
h = np.hstack((h, h))
m = np.hstack((m, m))
print('h.shape = ', h.shape)
print('m.shape = ', m.shape)

dictx = {'r': res12, 'v': vel, 'h': h, 'm': m}

with open('Data_Uniform_Initial_rho.pkl', 'wb') as f:
	pickle.dump(dictx, f)
#----------------------------


#------- check density profile -------
r = (x*x + y*y + z*z)**0.5

plt.scatter(r, rho, s = 1, color = 'black')
plt.show()
#-------------------------------------




