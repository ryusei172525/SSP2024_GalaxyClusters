'''
This program contains various surface mass density profiles of model clusters and
filaments.

Many of the cluster profiles come from Keiichi Umetsu's review article.
See Table 1 on p. 8, equations 31, 32 on p.10 and discussions on p. 21 
for putting together expression of nfw_Sigma, nfw_sigmabar and sigma_cr 

The filament profile comes from the Colberg et al. 2005 paper.
'''
from __future__ import division
import sys
import numpy
import cosmo

# CONSTANTS
kginMsun = 1.98892*10**30 #kg in a solar mass
minMpc = 3.08568025*10**22 # m in a Megaparsec

# NFW profile
def nfw_den(del_c,r_s,r,z,h=0.7,Om=0.3,Ol=0.7,Or=0):
    '''
    NFW density at radius r [kg/m^3]. Note that this function accepts a single number
    or list for r.
    
    del_c = characteristic overdensity of the CDM halo
    r_s = scale radius of the halo
    r = radius of interest [same units as r_s]
    z = halo redshift
    '''
    rho_crit = cosmo.rhoCrit(z,h,Om,Ol,Or)
    
    return rho_crit * del_c / (r/r_s*(1.+r/r_s)**2)

def nfw_Sigma(del_c,r_s,r,z,h=0.7,Om=0.3,Ol=0.7,Or=0):
    '''
    NFW surface mass density at radius theta [kg/m^2]. Note that this function
    accepts a single number or list for r.
    
    del_c = characteristic overdensity of the CDM halo
    r_s = scale radius of the halo (Mpc)
    r = radius of interest (Mpc)
    z = halo redshift
    
    compare expressions in Umetsu 2010 table 1 and equations in discussion on
    p.21 to get this expression 
    '''
    rho_crit = cosmo.rhoCrit(z,h,Om,Ol,Or)
    #convert r to an array so that the function will work for ints and arrays
    r = r*numpy.ones(numpy.shape(r))    
    x = r/r_s
    if numpy.sum(r_s==0)!=0:
        print('profiles.nfw_Sigma: r_s = 0 leads to infinity, exiting')
        sys.exit()
    mask_lt = x<1
    mask_eq = x==1
    mask_gt = x>1
    f = numpy.zeros(numpy.shape(x))
    #if x<1
    if numpy.sum(mask_lt) !=0:
        f[mask_lt] = 1/(1.-x[mask_lt]**2)*\
                (-1+2/numpy.sqrt(1-x[mask_lt]**2)*\
                 numpy.arctanh(numpy.sqrt((1-x[mask_lt])/(1.+x[mask_lt]))))
    #elif x==1
    if numpy.sum(mask_eq) !=0:
        f[mask_eq] = 1/3.
    #elif x > 1
    if numpy.sum(mask_gt) !=0:
        f[mask_gt] = 1/(x[mask_gt]**2-1.)*\
                    (1-2/numpy.sqrt(x[mask_gt]**2-1)*\
                     numpy.arctan(numpy.sqrt((x[mask_gt]-1)/(x[mask_gt]+1.))))
    #if only single value of r was input then make the f array into a float
    if numpy.size(f) == 1:
        f = f[0]
    return 2*del_c*rho_crit*r_s*f*minMpc

def nfw_Sigmabar(del_c,r_s,r,z,h=0.7,Om=0.3,Ol=0.7,Or=0):
    '''
    NFW average surface mass density within radius r [kg/m^2]. Note that this
    function accepts a single number or list for r.
    
    del_c = characteristic overdensity of the CDM halo
    r_s = scale radius of the halo [Mpc]
    r = radius of interest [Mpc]
    z = halo redshift
    
    compare expressions in Umetsu 2010 table 1 and equations in discussion on
    p.21 to get this expression
    '''
    rho_crit = cosmo.rhoCrit(z,h,Om,Ol,Or)
    #convert r to an array so that the function will work for ints and arrays
    r = r*numpy.ones(numpy.shape(r))
    x = r/r_s
    if numpy.sum(x==0)!=0 or r_s==0:
        print('profiles.nfw_Sigmabar: r or r_s = 0 leads to infinity, exiting')
        sys.exit()
    mask_lt = x<1
    mask_eq = x==1
    mask_gt = x>1
    g = numpy.zeros(numpy.shape(x))
    #if x<1
    if numpy.sum(mask_lt) !=0:
        g[mask_lt] = numpy.log(x[mask_lt]/2.)+\
                2/numpy.sqrt(1-x[mask_lt]**2)*\
                numpy.arctanh(numpy.sqrt((1-x[mask_lt])/(1+x[mask_lt])))
    #elif x==1
    if numpy.sum(mask_eq) !=0:
        g[mask_eq] = numpy.log(x[mask_eq]/2.) + 1
    #elif x > 1:
    if numpy.sum(mask_gt) !=0:
        g[mask_gt] = numpy.log(x[mask_gt]/2.)+\
                    2/numpy.sqrt(x[mask_gt]**2-1)*\
                   numpy.arctan(numpy.sqrt((x[mask_gt]-1)/(x[mask_gt]+1.)))
    #if only single value of r was input then make the g array into a float
    if numpy.size(g) == 1:
        g = g[0]
    return 4*del_c*rho_crit*r_s*g/x**2*minMpc

def nfwparam(M_200,z,h_scale=0.7,Om=0.3,Ol=0.7,Or=0.0):
    '''
    Inputs:
    M_200 = [array of floats; units=1e14 M_sun]

    Outputs:
    del_c, r_s = characteristic overdensity of the CDM halo, scale radius of 
    the halo (Mpc)
    Assumes Duffy et al. 2008 M_200 vs. c relationship.
    '''
    #calculate the concentration parameter based on Duffy et al. 2008
    #for full samples profile
    A200 = 5.71
    B200 = -0.084
    C200 = -0.47
    rho_cr = cosmo.rhoCrit(z,h_scale,Om,Ol,Or)/kginMsun*minMpc**3
    #calculate the r_200 radius
    r_200 = (M_200*1e14*3/(4*numpy.pi*200*rho_cr))**(1/3.)
    #the h_scale is multiplied because the scaling relationship uses 
    # 2e-2 h_scale^{-1}  using 1e14 Msun as unit 
    c = A200/(1+z)**numpy.abs(C200)*(M_200*h_scale/2e-2)**(B200)
    del_c = 200/3.*c**3/(numpy.log(1+c)-c/(1+c))
    r_s = r_200/c
    return del_c, r_s

def nfwparam_extended(M_200,z,h_scale=0.7,Om=0.3,Ol=0.7,Or=0.0):
    '''
    This is the same as nfwparam except that it offers extended output.
    Inputs:
    M_200 = [array of floats; units=e14 M_sun]
    Outputs:
    del_c, r_s = characteristic overdensity of the CDM halo, scale radius of 
    the halo (Mpc)
    r_200 (Mpc)
    c = concentration
    rho_s (M_sun/Mpc^3)
    
    Assumes Duffy et al. 2008 M_200 vs. c relationship.
    '''
    #calculate the concentration parameter based on Duffy et al. 2008
    #for full samples profile
    A200 = 5.71
    B200 = -0.084
    C200 = -0.47
    rho_cr = cosmo.rhoCrit(z,h_scale,Om,Ol,Or)/kginMsun*minMpc**3
    #calculate the r_200 radius
    r_200 = (M_200*1e14*3/(4*numpy.pi*200*rho_cr))**(1/3.)
    c = A200/(1+z)**numpy.abs(C200)*(M_200*h_scale/2e-2)**(B200)
    #c = 5.71/(1+z)**0.47*(M_200*h_scale/2e12)**(-0.084)
    del_c = 200/3.*c**3/(numpy.log(1+c)-c/(1+c))
    r_s = r_200/c
    rho_s = del_c*rho_cr
    return del_c, r_s, r_200, c, rho_s

def nfwM200(conc, z, A200=5.71, B200=-0.084, C200=-0.47, h_scale=0.7):
    '''
    Author: Karen Y. Ng
    This function gives the M200 based on c200 by making use of the mass-
    concentration scaling relationship given by Duffy et. al. 2008
    input:
    conc = concentration parameter
    A200, B200 , C200 = suitable parameters from Table 1 of Duffy et. al. 2008
    z = redshift
    output:
    the M200 with units of solar mass  
    '''
    M_pivot = (2.0e12/h_scale)  #have to be in terms of solar mass
    #output is also in solar mass 
    #when comparing to literature sometimes have to multiply by h_scale
    #depending on the unit
    return M_pivot*(conc/A200/((1.0+z)**C200))**(1.0/B200) 

# Filament Profile

#def filament_den():
#    '''
#    This returns the density of the filament for the input cylindrical radius.
#    '''

def nfwkappa(del_c,r_s,r,zl,zs,h=0.7,Om=0.3,Ol=0.7,Or=0):
    '''
    Computes the convergence for a nfw profile
    input:
    del_c = characteristic density
    r_s = scale radius 
    r = distance from center of lens
    zl = lens redshift
    zs = source redshift
    '''
    sigma = nfw_Sigma(del_c, r_s, r, zl)
    sigma_cr = cosmo.lensgeo(zl,zs)['sigcr']
    return sigma/sigma_cr 


def del_conc(c):
    '''
    calculates characteristic overdensity based on given concentration
    input:
    c = concentration parameter 
    output:
    characteristic overdensity
    '''
    return 200/3.*c**3/(numpy.log(1+c)-c/(1+c))

def filament_mu(mu_0,r_s,r,z,h=0.7,Om=0.3,Ol=0.7,Or=0):
    '''
    Returns the radial projected linear mass density of the filament at cylindrical radius (i.e.
    to get the surface mass density of the filament divide mu by the length of the filament).
    Currently this assumes that the axis of the filament is perpendicular to the line of
    sight.
    
    mu_0 = central surface mass density
    r_s = scale radius of the filament (~1.5-2 Mpc)
    r = cylindrical radius (Mpc)
    '''

    #Note that I think this form should actually include the critical density

    return mu_0 * r_s / (numpy.sqrt(1.+(r/r_s)**2))

def filament_mubar(mu_0,r_s,r,z,h=0.7,Om=0.3,Ol=0.7,Or=0):
    '''
    Returns the radial projected average linear mass density of the filament within cylindrical radius r
    (i.e. to get the average mass density of the filament divide mu by the length of the filament).
    Currently this assumes that the axis of the filament is perpendicular to the line of sight.

    mu_0 = central surface mass density
    r_s = scale radius of the filament (~1.5-2 Mpc)
    r = cylindrical radius (Mpc)
    '''

    #Note that I think this form should actually include the critical density    

    return mu_0 * r_s**2 * numpy.log(r/r_s+numpy.sqrt(1.+(r/r_s)**2)) / (2.*r)
