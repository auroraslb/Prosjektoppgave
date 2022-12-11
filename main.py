import numpy as np
import matplotlib.pyplot as plt
import ESP_simulator as ESP
import APRBS as APRBS
import Plot_Simulator as plot

Ts = 1/10
simtime = 10
### Initial values: [70 bar = 70e5 Pa, 30 bar = 30e5 Pa, 36 m3/h = 0.01 m3/s]
x0 = np.array([70e5,30e5,0.01],dtype = np.float64)

# constant input w z = 100% and f = 53 Hz
u_const = np.array([1,53],dtype = np.float64)

# u switching from z = 50% and f = 50 Hz to z = 100% and f = 50 Hz after 5 min
z_before = np.ones(int(simtime/(2*Ts)))*0.5
z_after = np.ones(int(simtime/(2*Ts)))
z_switch = np.transpose(np.append(z_before,z_after))
f_switch = np.transpose(np.ones(int(simtime/Ts))*50)
u_switch = np.vstack((z_switch,f_switch))

# z = 60%, while f increases by 2 Hz from 50 Hz every 10 minutes
# Simtime of 50
simtime_f_incr = 50
z_f_incr = np.transpose(np.ones(int(simtime_f_incr/Ts))*0.6)
f_0_10 = np.ones(int(simtime_f_incr/(5*Ts)))*50
f_10_20 = np.ones(int(simtime_f_incr/(5*Ts)))*52
f_0_20 = np.append(f_0_10,f_10_20)
f_20_30 = np.ones(int(simtime_f_incr/(5*Ts)))*54
f_0_30 = np.append(f_0_20,f_20_30)
f_30_40 = np.ones(int(simtime_f_incr/(5*Ts)))*56
f_0_40 = np.append(f_0_30,f_30_40)
f_40_50 = np.ones(int(simtime_f_incr/(5*Ts)))*58
f_f_incr = np.transpose(np.append(f_0_40,f_40_50))
u_f_incr = np.vstack((z_f_incr,f_f_incr))

# z random between 50% and 100%, f = 50%
z_rand = np.transpose(APRBS.create_APRBS(1, 0, int(simtime/Ts), 10))
f_rand = np.transpose(np.ones(int(simtime/Ts))*50)
u_rand = np.vstack((z_rand,f_rand))


#ESP = ESP.simulator(x0, u_const, Ts, int(simtime/Ts), True)
#ESP = ESP.simulator(x0, u_switch, Ts, int(simtime/Ts), False)
#ESP = ESP.simulator(x0, u_rand, Ts, int(simtime/Ts), False)
ESP = ESP.simulator(x0, u_f_incr, Ts, int(simtime_f_incr/Ts), False)
output = ESP.episode()

fig = plt.figure()
#plot.plot_sim(output,u_const,simtime,Ts,fig)
#plot.plot_sim(output,u_switch,simtime,Ts,fig)
#plot.plot_sim(output,u_rand,simtime,Ts,fig)
plot.plot_sim(output,u_f_incr,simtime_f_incr,Ts,fig)
