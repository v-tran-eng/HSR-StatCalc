import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator


def effect_P(base_eff, eff_hr, eff_res, debuff_res=0):
    '''
    Calculates probability of status infliction for a given set of coeff
    '''

    probability = base_eff*(1+eff_hr)*(1-eff_res)*(1-debuff_res)

    return probability


def P_simple(base_eff, eff_res, debuff_res=0, hr_start=0, hr_stop=1.5):
    '''
    Calculates probability for all hitrate values specified
    Caps P values to 100%
    '''

    # define hitrate array
    hitrate_array = np.linspace(hr_start, hr_stop)

    # calculate
    P_array = effect_P(base_eff, hitrate_array, eff_res, debuff_res)

    # cap probabilities at 100%
    P_array_capped = np.where(P_array < 1, P_array, 1)

    return P_array_capped, hitrate_array


def singlePlot(base_eff, eff_res, **P_kwargs):
    '''
    Uses P_simple to plot probability vs EHR for some given parameters
    '''

    temp_Parray, hr_array = P_simple(base_eff, eff_res, **P_kwargs)
    scaled_Parray = temp_Parray*100
    scaled_hr_array = hr_array*100


    fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)

    ax.plot(scaled_hr_array, scaled_Parray)
    ax.set_xlabel('Hitrate (%)')
    ax.set_ylabel('Probability (%)')
    ax.set_title('Probability vs Hitrate (Base EHR = ' + str(base_eff) +
                 ', Enemy ER = ' + str(eff_res) + ')')
    plt.show()

    # print(temp_Parray)
    return True


def P_all(base_eff=0.3, min_eff_res=0, max_eff_res=0.4):
    '''
    Calculates P for all hitrate and eff_res values
    Base effect hit rate is held constant
    '''

    # set constants
    min_hr = 0
    max_hr = 1.5
    steps = 50

    # get an array of all possible input values
    hr_array = np.linspace(min_hr, max_hr, num=steps)
    eff_res_array = np.linspace(min_eff_res, max_eff_res, num=steps)

    # define meshgrid to calculate over all eff_res/hitrate combinations
    HR_mesharray, ER_mesharray = np.meshgrid(hr_array, eff_res_array)

    # use probability function above
    all_P_array = effect_P(base_eff, HR_mesharray, ER_mesharray)

    # cap at 100% probability
    P_capped = np.where(all_P_array < 1, all_P_array, 1)

    return P_capped, HR_mesharray, ER_mesharray


def P_plot_all(base_eff, min_eff_res=0, max_eff_res=0.4):
    '''
    Uses the P_all function and plots with plt
    '''

    all_data = P_all(base_eff, min_eff_res, max_eff_res)

    # extract data
    all_P_array = all_data[0]
    HR_mesharray = all_data[1]
    ER_mesharray = all_data[2]

    # plot
    fig, ax = plt.subplots(figsize=(10, 7), subplot_kw={'projection': '3d'})

    surf = ax.plot_surface(HR_mesharray, ER_mesharray, all_P_array,
                           cmap=cm.coolwarm, linewidth=0,
                           antialiased=False)
    ax.zaxis.set_major_formatter('{x:.02f}')
    # ax.plot_wireframe(HR_mesharray, ER_mesharray, all_P_array,
                      # rstride=5, cstride=5)

    ax.set_title('Probability vs Bonus Hitrate, Enemy Effect Res ' +
                '(Base Effect Hitrate = ' + str(base_eff) + ')')
    ax.set_xlabel('Hitrate')
    ax.set_ylabel('Enemy Effect Res')
    ax.set_zlabel('Probability')
    fig.colorbar(surf)

    ax.view_init(elev=25, azim=-160)

    plt.show()
