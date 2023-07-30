import eff_res as er


def singlePlotTest(debuff_res=0):

    base_eff = 0.9
    eff_res = 0.4

    er.singlePlot(base_eff, eff_res, debuff_res)

    return True


def all_calc_test():
    data = er.P_all()

    print(data[0])
    print(data[1])
    print(data[2])


def plot_all_test():
    base_eff = 0.8

    er.P_plot_all(base_eff)


def main():
    # singlePlotTest(1)
    plot_all_test()


main()
