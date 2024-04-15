from brian2 import *
from js_utils import *

# Constant parameters
# chain
N = 500
WIDTH = 50
INHIBIT_SIZE = 105  # 500/4.8
GROUPS = int(N / WIDTH)

# equation
VT = -55 * mV
VR = -70 * mV
TAUM = 10 * ms
TAUPSP = 0.325 * ms
EQS = '''
dv/dt = (-(v-VR)+x)*(1./TAUM) : volt
dx/dt = (-x+y)*(1./TAUPSP) : volt
dy/dt = -y*(1./TAUPSP)+25.27*mV/ms+
        (8*mV/ms**0.5)*xi : volt
'''

# simulation
DURATION = 180 * ms
SIMULATIONS_NUM = 500


class SynfireChain:
    def __init__(self, w, w_inter, w_ex, w_inhibit, p_ab, p_ac, p_bbin, p_ccin, r_bin, r_cin):
        self.w = w
        self.w_inter = w_inter
        self.w_ex = w_ex
        self.w_inhibit = w_inhibit
        self.p_ab = p_ab
        self.p_ac = p_ac
        self.p_bbin = p_bbin
        self.p_ccin = p_ccin
        self.r_bin = r_bin
        self.r_cin = r_cin
        self.results = []

    def run_simulation(self, json_name):
        w = self.w
        w_inter = self.w_inter
        w_ex = self.w_ex
        w_inhibit = self.w_inhibit

        if not os.path.exists(f"{RES_DIR_NAME}/{json_name}"):
            os.makedirs(f"{RES_DIR_NAME}/{json_name}")

        for s in range(SIMULATIONS_NUM):
            start_scope()

            # create chains
            # A
            A = NeuronGroup(N, EQS, threshold='v > VT', reset='v = VR', refractory=2 * ms, method='euler')
            A.v = 'VR + rand() * (VT - VR)'
            S = Synapses(A, A, on_pre='v += w', delay=5 * ms)
            S.connect(condition="(j >= i + WIDTH - i%WIDTH) and j < (i + 2 * WIDTH - i%WIDTH)", skip_if_invalid=True)

            # B
            B = NeuronGroup(N, EQS, threshold='v > VT', reset='v = VR', refractory=2 * ms, method='euler')
            B.v = 'VR + rand() * (VT - VR)'
            S1 = Synapses(B, B, on_pre='v += w', delay=5 * ms)
            S1.connect(condition="(j >= i + WIDTH - i%WIDTH) and j < (i + 2 * WIDTH - i%WIDTH)", skip_if_invalid=True)

            # C
            C = NeuronGroup(N, EQS, threshold='v > VT', reset='v = VR', refractory=2 * ms, method='euler')
            C.v = 'VR + rand() * (VT - VR)'
            S2 = Synapses(C, C, on_pre='v += w', delay=5 * ms)
            S2.connect(condition="(j >= i + WIDTH - i%WIDTH) and j < (i + 2 * WIDTH - i%WIDTH)", skip_if_invalid=True)

            # B_in - B->B_in->C
            B_in = NeuronGroup(INHIBIT_SIZE, EQS, threshold='v > VT', reset='v = VR', refractory=2 * ms, method='euler')
            B_in.v = 'VR + rand() * (VT - VR)'

            # C_in - C->C_in->B
            C_in = NeuronGroup(INHIBIT_SIZE, EQS, threshold='v > VT', reset='v = VR', refractory=2 * ms, method='euler')
            C_in.v = 'VR + rand() * (VT - VR)'

            # Inter synapses
            AB = Synapses(A, B, on_pre='v += w_inter', delay=5 * ms)
            AB.connect(i=list(range(N - WIDTH, N)), j=list(range(WIDTH)), p=self.p_ab)

            AC = Synapses(A, C, on_pre='v += w_inter', delay=5 * ms)
            AC.connect(i=list(range(N - WIDTH, N)), j=list(range(WIDTH)), p=self.p_ac)

            # Excitatory synapses (enable more than 1 group forming inhibitory connections)
            BB_in = Synapses(B, B_in, on_pre='v += w_ex', delay=5 * ms)
            BB_in.connect(condition="i<WIDTH", p=self.p_bbin)

            CC_in = Synapses(C, C_in, on_pre='v += w_ex', delay=5 * ms)
            CC_in.connect(condition="i<WIDTH", p=self.p_ccin)

            # Inhibatory synapses
            B_inC = Synapses(B_in, C, on_pre='v -= w_inhibit', delay=5 * ms)
            B_inC.connect(condition="i<INHIBIT_SIZE",
                          p=min((w_ex * WIDTH) / ((w_inhibit * INHIBIT_SIZE) * self.r_bin), 1))

            C_inB = Synapses(C_in, B, on_pre='v -= w_inhibit', delay=5 * ms)
            C_inB.connect(condition="i<INHIBIT_SIZE",
                          p=min((w_ex * WIDTH) / ((w_inhibit * INHIBIT_SIZE) * self.r_cin), 1))

            # Inputs
            inputs = SpikeGeneratorGroup(WIDTH, np.arange(WIDTH),
                                         np.absolute(np.random.randn(WIDTH)) * 0.1 * ms + 20 * ms)
            S_inputs = Synapses(inputs, A[:WIDTH], on_pre='v += w')
            S_inputs.connect()

            # Monitors
            M = SpikeMonitor(A)
            Mb = SpikeMonitor(B)
            Mc = SpikeMonitor(C)
            MBin = SpikeMonitor(B_in)
            MCin = SpikeMonitor(C_in)

            # Run the simulation
            run(DURATION)

            # Plots
            plt.figure()
            plt.plot(M.t / ms, 1.0 * M.i / WIDTH, '.k', color='C0', label='A')
            plt.plot(Mb.t / ms, 1.0 * Mb.i / WIDTH + GROUPS, '.k', color='C1', label='B')
            plt.plot(Mc.t / ms, 1.0 * Mc.i / WIDTH + 2 * GROUPS, '.k', color='C2', label='C')
            plt.plot(MBin.t / ms, 1.0 * MBin.i / WIDTH + 3 * GROUPS, '.k', color='C3', label='B_inhibit')
            plt.plot(MCin.t / ms, 1.0 * MCin.i / WIDTH + 4 * GROUPS, '.k', color='C4', label='C_inhibit')
            plt.plot([0, DURATION / ms], np.arange(GROUPS * 5).repeat(2).reshape(-1, 2).T, 'k-')
            plt.legend(loc='upper left')
            xlabel('Time (ms)')
            ylabel('Group Number')
            plt.title(f'{json_name}_plot_{s}')
            savefig(os.path.join(f"{RES_DIR_NAME}/{json_name}", f'fig{s}.svg'), format='svg', bbox_inches='tight')
            plt.close()
            self.results.append([M.t, Mb.t, Mc.t, MBin.t, MCin.t])
        return

    def create_pie_plot(self, json_name):
        # Spikes count
        results_len = np.array([[len(i) for i in lst] for lst in self.results])

        # calculates results
        a_mean = np.mean(results_len[:, 0])
        did_fire = results_len > (a_mean * 0.55)
        rel_sim = did_fire[:, 0]
        no_fire = ~did_fire[:, 1] & ~did_fire[:, 2]
        b_win = did_fire[:, 1] & ~did_fire[:, 2]
        c_win = ~did_fire[:, 1] & did_fire[:, 2]
        both_fire = did_fire[:, 1] & did_fire[:, 2]
        plt.figure()
        results = {NO_FIRE: no_fire[rel_sim].mean(), B_WIN: b_win[rel_sim].mean(), C_WIN: c_win[rel_sim].mean(),
                   BOTH_FIRE: both_fire[rel_sim].mean()}

        # saves results (4 values for each pair of (p_ab, p_ac)
        data = {"r_bin": self.r_bin, "r_cin": self.r_cin, "vals": results}
        create_json(os.path.join(f"{RES_DIR_NAME}", f"results_{json_name}.json"), data)

        # creates pie plot
        plt.pie(results.values(), labels=[NO_FIRE, B_WIN, C_WIN, BOTH_FIRE])
        plt.savefig(os.path.join(f"{RES_DIR_NAME}/{json_name}", "pie_fig.svg"), format='svg', bbox_inches='tight')
        plt.close()
        return


def main_func_per_json_file(json_name):
    params = load_json(json_name)
    json_name = json_name.replace(".json", "")
    print(json_name)
    print(params)
    chain = SynfireChain(**{k: v * mV if k.startswith("w") else v for k, v in params.items()})
    chain.run_simulation(json_name)
    chain.create_pie_plot(json_name)


if __name__ == "__main__":
    # for f in jsons_dir: (submit different job in the cluster for each json file)
    if len(sys.argv) != 2:
        print("Usage: python3 synfire_chain.py <json_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    main_func_per_json_file(json_file)





