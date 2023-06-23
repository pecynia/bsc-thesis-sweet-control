import numpy as np
import scipy.stats as stats

# Gamma distribution, has a lower peak, but holds on for a bit longer
def gamma(units, alpha=2, rate=0.87):
    '''
    Returns an array of size 500, which represents the activity for 8.33 hours.
    params: alpha, rate
    '''
    x = np.linspace(0, 10, 500) - 12.28/60
    gamma = stats.gamma.pdf(x, alpha, scale=1/rate) 

    for i in range(len(gamma)):
        gamma[i] *= units
    
    return np.array(gamma)    # array of size 500 (8.33 hours)

# Lognormal distribution, has a higher peak, but drops off faster
def lognorm(units, mu=0.75, sigma=0.75):
    '''
    Returns an array of size 500, which represents the activity for 8.33 hours.
    params: mu, sigma
    '''
    x = np.linspace(0, 5, 500) - 12.28/60        
    lognorm = stats.lognorm.pdf(x, mu, scale=sigma)
    
    for i in range(len(lognorm)):
        lognorm[i] *= units/1.99
    
    return np.array(lognorm)  # array of size 500 (8.33 hours)
