from math import sqrt
from casadi import *

### Declearation of constants ###
# Well
g = 9.81                #Gravitational acceleration constant    [m/s2]
C_c =2*pow(10,-5)       #Choke valve constant                   [*]
A_1 = 0.008107          #Cross-section area of pipe below ESP   [m2]
A_2 = 0.008107          #Cross-section area of pipe above ESP   [m2]
D_1 = 0.1016            #Pipe diameter below ESP                [m]
D_2 = 0.1016            #Pipe diameter above ESP                [m]
h_1 = 200               #Height from reservoir to ESP           [m]
h_w = 1000              #Total vertical distance in well        [m]
L_1 = 500               #Length from reservoir to ESP           [m]
L_2 = 1200              #Length from ESP to choke               [m]
V_1 = 4.054             #Pipe volume below ESP                  [m3]
V_2 = 9.729             #Pipe volume above ESP                  [m3]

# ESP data
f_0 = 60                #ESP characteristics reference freq.    [Hz]
I_np = 65               #ESP motor nameplate current            [A]
P_np = 1.625*pow(10, 5) #ESP motor nameplate power              [W]

# Parameters from fluid analysis and well tests
beta_1 = 1.5*pow(10,9)  #Bulk modulus below ESP                 [Pa]
beta_2 = 1.5*pow(10,9)  #Bulk modulus below ESP                 [Pa]
M = 1.992*pow(10,8)     #Fluid inertia parameter                [kg/m4]
rho = 950               #Density of produced fluid              [kg/m3]
P_r = 1.26*pow(10, 7)   #Reservoir pressure                     [Pa]

# Parameters assumed to be constant
PI = 2.32*pow(10,-9)    #Well productivity index                [m3/s/Pa]
mu = 0.025              #Viscosity of produced fluid            [Pa*s]
P_m = 20                #Manifold pressure                      [Pa]

# Inputs
z = 100 #%
f = 53 #Hz

dae = DaeBuilder()
# Input expressions
p_bh = dae.add_x('p_bh')
p_wh = dae.add_x('p_wh')
q = dae.add_x('q')

q_r = dae.add_z('q_r')
q_c = dae.add_z('q_c')
Dp_f = dae.add_z('Dp_f')
Dp_p = dae.add_z('Dp_p')

#Output expressions
p_bh_dot = beta_1/V_1*(q_r-q)
p_wh_dot = beta_2/V_2*(q-q_c)
q_dot = 1/M*(p_bh-p_wh-rho*g*h_w-Dp_f+Dp_p)
dae.add_ode('p_bh_dot', p_bh_dot)
dae.add_ode('p_wh_dot', p_wh_dot)
dae.add_ode('q_dot', q_dot)

F_1 = 0.158*((rho*L_1*pow(q,2))/(D_1*pow(A_1,2)))*pow(mu/(rho*D_1*q),1/4)
F_2 = 0.158*((rho*L_2*pow(q,2))/(D_2*pow(A_2,2)))*pow(mu/(rho*D_2*q),1/4)

C_H = 1-0.03*mu
C_q = 1 - 2.6266*mu + 6.0032*pow(mu,2) - 6.8104*pow(mu,3) + 2.7944*pow(mu,4)
q_0 = q/C_q*(f_0/f)
H_0 = 9.5670*pow(10,2) + 7.4959*pow(10,3)*q_0 - 1.2454*pow(10,6)*pow(q_0, 2)
H = C_H*H_0*pow(f_0/f,2)

dae.add_alg('q_r', PI*(P_r-p_bh))
dae.add_alg('q_c', C_c*sqrt(p_wh-P_m)*z)
dae.add_alg('Dpf_n', F_1 + F_2)   
dae.add_alg('Dpp_n', rho*g*H)

#Initial conditions
dae.set_start('p_bh', 70)
dae.set_start('p_wh', 30)
dae.set_start('q', 36)

ode = vertcat(*dae.ode)
alg = vertcat(*dae.alg)
x = vertcat(*dae.x)
z = vertcat(*dae.z)

dae_dict = {'x': x, 
            'z': z, 
            'ode': ode, 
            'alg': alg}

#I = integrator('I', 'idas', dae)
dt = 10e-3
opts = {"tf": dt}
I = integrator("I", "cvodes", dae_dict, opts)
print(I)

#print(ode)
#dae.disp(True)

#f = dae.create('f', ['x', 'z'], ['ode', 'alg'])
#print(f)
