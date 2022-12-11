import casadi as ca
import numpy as np

class simulator():
    def __init__(self, x0, u, Ts, samples, constant_input = True):
        self.x = x0
        self.u = u
        self.Ts = Ts
        self.samples = samples
        self.const_input = constant_input
        self.output = np.empty([x0.shape[0], self.samples])

        # Symbolic variables
        self.x_sim = ca.MX.sym('x', x0.shape[0])
        self.u_sim = ca.MX.sym('u', u.shape[0])

        ### ESP state function ###
        # Well
        g = 9.81                #Gravitational acceleration constant    [m/s2]
        Cc = 2*10**(-5)         #Choke valve constant                   [*]
        A1 = 0.008107           #Cross-section area of pipe below ESP   [m2]
        A2 = 0.008107           #Cross-section area of pipe above ESP   [m2]
        D1 = 0.1016             #Pipe diameter below ESP                [m]
        D2 = 0.1016             #Pipe diameter above ESP                [m]
        hw = 1000               #Total vertical distance in well        [m]
        L1 = 500                #Length from reservoir to ESP           [m]
        L2 = 1200               #Length from ESP to choke               [m]
        V1 = 4.054              #Pipe volume below ESP                  [m3]
        V2 = 9.729              #Pipe volume above ESP                  [m3]

        # ESP data
        f0 = 60                 #ESP characteristics reference freq.    [Hz]

        # Parameters from fluid analysis and well tests
        beta = 1.5*10**9        #Bulk modulus below ESP                 [Pa]
        M = 1.992*10**8         #Fluid inertia parameter                [kg/m4]
        rho = 950               #Density of produced fluid              [kg/m3]
        Pr = 1.26*10**7         #Reservoir pressure                     [Pa]

        # Parameters assumed to be constant
        PI = 2.32*10**(-9)      #Well productivity index                [m3/s/Pa]
        mu = 0.025              #Viscosity of produced fluid            [Pa*s]
        Pm = 20e5               #Manifold pressure                      [Pa]

        # Increase readability of variables 
        # x = [Pbh, Pwh, q]
        Pbh = self.x_sim[0]
        Pwh = self.x_sim[1]
        q = np.fmax(self.x_sim[2],1e-9) # Avoid numerical instability due to low values
        # u = [z, f]
        z = self.u_sim[0]
        f = self.u_sim[1]

        ### Algebraic equations
        # Flow 
        qr = PI*(Pr-Pbh)
        qc = Cc*np.sqrt(Pwh-Pm)*z

        # Friction
        F1 = 0.158*((rho*L1*q**2)/(D1*A1**2))*(mu/(rho*D1*q))**(1/4)
        F2 = 0.158*((rho*L2*q**2)/(D2*A2**2))*(mu/(rho*D2*q))**(1/4)
        Dpf = F1 + F2

        # ESP
        CH = 1 - 0.03*mu
        Cq = 1 - 2.6266*mu + 6.0032*mu**2 - 6.8104*mu**3 + 2.7944*mu**4
        q0 = (q/Cq)*(f0/f)
        H0 = 9.5970e2 + (7.4959e3)*q0 - (1.2454e6)*(q0**2)

        H = CH*H0*(f/f0)**2
        Dpp = rho*g*H

        ### ODEs
        Pbh_dot = beta/V1*(qr-q)
        Pwh_dot = beta/V2*(q-qc)
        q_dot = 1/M*(Pbh-Pwh-rho*g*hw-Dpf+Dpp)

        dx = ca.MX(3,1)
        dx[0] = Pbh_dot
        dx[1] = Pwh_dot
        dx[2] = q_dot
        
        self.ode = {'x': self.x_sim, 'p': self.u_sim, 'ode': dx}
        opts = {'t0': 0.0, 'tf':self.Ts}
        self.F = ca.integrator('F', 'cvodes', self.ode, opts)

    def step(self, u):
        res = self.F(x0=self.x,p=u)
        self.x = res['xf']
        if self.x[2] < 1e-9: # Avoid numerical instability due to low values
            self.x[2] = 1e-9
        return np.array(self.x).flatten()
    
    def episode(self):
        for i in range(0,self.samples):
            if self.const_input:
                y = self.step(self.u)
            else:
                y = self.step(self.u[:,i])
            self.output[:,i] = y
        return self.output
