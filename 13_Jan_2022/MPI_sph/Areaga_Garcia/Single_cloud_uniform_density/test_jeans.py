
import numpy as np
import pandas as pd
import pickle
import glob

M_sun = 1.989e33 # gram
grav_const_in_cgs = 6.67259e-8 #  cm3 g-1 s-2
UnitMass_in_g = 50.0 * M_sun       # !!!!!!!!!!!!!!!!!!!!!!!!! CHANGE !!!!!!!!!!!!!!!!!
#rB = 0.8 # pc
#ksi = 3.
R_0 = 0.84 #rB/ksi
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

G = grav_const_in_cgs

Mcld = 50. * M_sun


filz = np.sort(glob.glob('./Outputs/*.pkl'))

j = -1

with open(filz[j], 'rb') as f:
	data = pickle.load(f)


r = data['pos']
h = data['h']

print(r.shape)

print('h = ', np.sort(h))

N = r.shape[0]/2.
m = 1. / N # mass of an SPH particle.

print('N = ', N)

N_ngb = 50.
M_min = N_ngb * m * UnitMass_in_g


#---- Speed of Sound ------
mH = 1.6726e-24 # gram
kB = 1.3807e-16  # cm2 g s-2 K-1
T_0 = 54. # K, see Table_1 in Anathpindika - 2009 - II

# Note that for pure molecular hydrogen mu=2. For molecular gas with ~10% He by mass and trace metals, mu ~ 2.7 is often used.
muu = 2.7
mH2 = muu * mH

c_s = (kB * T_0 / mH2)**0.5

print('Sound speed (cm/s) = ', c_s)
print('Sound speed (m/s) = ', c_s/100.)
print('Sound speed (km/s) = ', c_s/100000.)
print()
#--------------------------

rho = 1.e-15 # g/cm^3

M_Jeans = np.pi**2.5 * c_s**3 / 6. / G**1.5 / rho**0.5

print()
print('M_min (mass resolution in gram) = ', M_min)
print('M_Jeans (in gram) = ', M_Jeans)
print()
print('M_min (mass resolution in solar mass) = ', M_min/M_sun)
print('M_Jeans (in solar mass) = ', M_Jeans/M_sun)










