import matplotlib.pyplot as plt
import numpy as np

def plot_sim(output, u, simtime, Ts, figure):

    plt.subplot(511)
    plt.title("Responses")
    plt.plot(np.arange(int(simtime/Ts))*Ts,output[0,:]/1e5)
    plt.ylabel("$p_{bh}$ [bar]")
    plt.grid()

    plt.subplot(512)
    plt.plot(np.arange(int(simtime/Ts))*Ts,output[1,:]/1e5)
    plt.ylabel("$p_{wh}$ [bar]")
    plt.grid()

    plt.subplot(513)
    plt.plot(np.arange(int(simtime/Ts))*Ts,output[2,:]*3600)
    plt.ylabel("$q$ [$m^3/h$]")
    plt.grid()

    plt.subplot(514)
    plt.title("Inputs")
    try:
        plt.plot(np.arange(int(simtime/Ts))*Ts,u[0,:]*100, color='r')
    except:
        plt.hlines(y=u[0]*100, xmin=0, xmax=simtime, color='r')
    plt.ylabel("$z$ [%]")
    plt.grid()

    plt.subplot(515)
    try:
        plt.plot(np.arange(int(simtime/Ts))*Ts,u[1,:], color='r')
    except:
        plt.hlines(y=u[1], xmin=0, xmax=simtime, color='r')
    plt.ylabel("$f$ [Hz]")
    plt.xlabel('Time [min]')
    plt.grid()

    plt.show()
