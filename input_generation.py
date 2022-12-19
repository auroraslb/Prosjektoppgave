import numpy as np
import APRBS as APRBS


def create_constant_input(z, f):
    return np.array([z,f],dtype = np.float64)


#------------------------------- CHANGING Z VALUES -----------------------------------------
def create_step_up_z(z_lower, z_higher, f, simtime, Ts):
    z_lower_values = np.ones(int(simtime/(2*Ts)))*z_lower
    z_higher_values = np.ones(int(simtime/(2*Ts)))*z_higher

    z_combined = np.transpose(np.append(z_lower_values,z_higher_values))

    f_out = np.transpose(np.ones(int(simtime/Ts))*f)
    return np.vstack((z_combined,f_out))


def create_step_down_z(z_lower, z_higher, f, simtime, Ts):
    z_lower_values = np.ones(int(simtime/(2*Ts)))*z_lower
    z_higher_values = np.ones(int(simtime/(2*Ts)))*z_higher

    z_combined = np.transpose(np.append(z_higher_values,z_lower_values))

    f_out = np.transpose(np.ones(int(simtime/Ts))*f)
    return np.vstack((z_combined,f_out))


def create_step_updown_z(z_lower, z_higher, f, simtime, Ts):
    z_lower_values = np.ones(int(simtime/(3*Ts)))*z_lower
    z_higher_values = np.ones(int(simtime/(3*Ts)))*z_higher
    z_lower2_values = np.ones(int(simtime/Ts)-len(z_lower_values)-len(z_higher_values))*z_lower

    z_combined = np.transpose(np.append(z_lower_values,np.append(z_higher_values,z_lower2_values)))

    f_out = np.transpose(np.ones(int(simtime/Ts))*f)
    return np.vstack((z_combined,f_out))


def create_stepping_z(z_start, z_step, f, simtime, Ts):
    z_0_10 = np.ones(int(simtime/(5*Ts)))*z_start
    z_10_20 = np.ones(int(simtime/(5*Ts)))*(z_start + z_step)
    z_20_30 = np.ones(int(simtime/(5*Ts)))*(z_start + 2*z_step)
    z_30_40 = np.ones(int(simtime/(5*Ts)))*(z_start + 3*z_step)
    z_40_50 = np.ones(int(simtime/(5*Ts)))*(z_start + 4*z_step)
    z_combined = np.transpose(np.append(z_0_10,np.append(z_10_20,np.append(z_20_30,np.append(z_30_40,z_40_50)))))

    f_out = np.transpose(np.ones(int(simtime/Ts))*f)
    return np.vstack((z_combined,f_out))


def create_random_z(z_min, z_max, f, simtime, Ts, hold):
    z_rand = np.transpose(APRBS.create_APRBS(z_max, z_min, int(simtime/Ts), hold))
    f_out = np.transpose(np.ones(int(simtime/Ts))*f)
    return np.vstack((z_rand,f_out))


#------------------------------- CHANGING F VALUES -----------------------------------------
def create_step_up_f(z, f_lower, f_higher, simtime, Ts):
    f_lower_values = np.ones(int(simtime/(2*Ts)))*f_lower
    f_higher_values = np.ones(int(simtime/(2*Ts)))*f_higher

    f_combined = np.transpose(np.append(f_lower_values,f_higher_values))

    z_out = np.transpose(np.ones(int(simtime/Ts))*z)
    return np.vstack((z_out,f_combined))


def create_step_down_f(z, f_lower, f_higher, simtime, Ts):
    f_lower_values = np.ones(int(simtime/(2*Ts)))*f_lower
    f_higher_values = np.ones(int(simtime/(2*Ts)))*f_higher

    f_combined = np.transpose(np.append(f_higher_values,f_lower_values))

    z_out = np.transpose(np.ones(int(simtime/Ts))*z)
    return np.vstack((z_out,f_combined))


def create_step_updown_f(z, f_lower, f_higher, simtime, Ts):
    f_lower_values = np.ones(int(simtime/(3*Ts)))*f_lower
    f_higher_values = np.ones(int(simtime/(3*Ts)))*f_higher
    f_lower2_values = np.ones(int(simtime/Ts)-len(f_lower_values)-len(f_higher_values))*f_lower

    f_combined = np.transpose(np.append(f_lower_values,np.append(f_higher_values,f_lower2_values)))

    z_out = np.transpose(np.ones(int(simtime/Ts))*z)
    return np.vstack((z_out,f_combined))


def create_stepping_f(z, f_start, f_step, simtime, Ts):
    f_0_10 = np.ones(int(simtime/(5*Ts)))*f_start
    f_10_20 = np.ones(int(simtime/(5*Ts)))*(f_start + f_step)
    f_20_30 = np.ones(int(simtime/(5*Ts)))*(f_start + 2*f_step)
    f_30_40 = np.ones(int(simtime/(5*Ts)))*(f_start + 3*f_step)
    f_40_50 = np.ones(int(simtime/(5*Ts)))*(f_start + 4*f_step)
    f_combined = np.transpose(np.append(f_0_10,np.append(f_10_20,np.append(f_20_30,np.append(f_30_40,f_40_50)))))

    z_out = np.transpose(np.ones(int(simtime/Ts))*z)
    return np.vstack((z_out,f_combined))


def create_random_f(z, f_min, f_max, simtime, Ts, hold):
    f_rand = np.transpose(APRBS.create_APRBS(f_max, f_min, int(simtime/Ts), hold))
    z_out = np.transpose(np.ones(int(simtime/Ts))*z)
    return np.vstack((z_out,f_rand))
