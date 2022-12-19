import numpy as np
import matplotlib.pyplot as plt
import ESP_simulator as ESP
import APRBS as APRBS
import Plot_Simulator as plot
import input_generation as input

Ts = 1/10
simtime = 50
### Initial values: [70 bar = 70e5 Pa, 30 bar = 30e5 Pa, 36 m3/h = 0.01 m3/s]
x0 = np.array([70e5,30e5,0.01],dtype = np.float64)


# constant input w z = 100% and f = 60 Hz
u_const = input.create_constant_input(1,60) 
ESP_const = ESP.simulator(x0, u_const, Ts, int(simtime/Ts), True)
output_const = ESP_const.episode()

fig1 = plt.figure(1)
plot.plot_sim(output_const,u_const,simtime,Ts,fig1)


# u switching from z = 50% and f = 50 Hz to z = 100% and f = 50 Hz after one third of the time, then going back down after 2/3
u_z_updown = input.create_step_updown_z(0.5,1,50,simtime,Ts)
ESP_z_updown = ESP.simulator(x0, u_z_updown, Ts, int(simtime/Ts), False)
output_z_updown = ESP_z_updown.episode()

fig2 = plt.figure(2)
plot.plot_sim(output_z_updown,u_z_updown,simtime,Ts,fig2)


# f switching from f = 60Hz to f = 50 Hz after one third of the time, then going back up after 2/3, with z = 60%
u_f_updown = input.create_step_updown_f(0.6,60,50,simtime,Ts)
ESP_f_updown = ESP.simulator(x0, u_f_updown, Ts, int(simtime/Ts), False)
output_f_updown = ESP_f_updown.episode()

fig3 = plt.figure(3)
plot.plot_sim(output_f_updown,u_f_updown,simtime,Ts,fig3)


# z = 60%, while f increases by 2 Hz from 50 Hz every 10 minutes
u_f_incr = input.create_stepping_f(0.6,50,2,simtime,Ts)
ESP_f_incr = ESP.simulator(x0, u_f_incr, Ts, int(simtime/Ts), False)
output_f_incr = ESP_f_incr.episode()

fig4 = plt.figure(4)
plot.plot_sim(output_f_incr,u_f_incr,simtime,Ts,fig4)


# z random between 50% and 100%, f = 50%
u_z_rand = input.create_random_z(0.5,1,50,simtime,Ts,50)
ESP_z_rand = ESP.simulator(x0, u_z_rand, Ts, int(simtime/Ts), False)
output_z_rand = ESP_z_rand.episode()

fig5 = plt.figure(5)
plot.plot_sim(output_z_rand,u_z_rand,simtime,Ts,fig5)
