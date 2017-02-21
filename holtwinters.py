def MAPE(actual, estimate):
        
    if len(actual) != len(estimate):
        print("ERROR: Lists not the same length.")
        return []
        
    pcterrors = []
    
    for i in range(len(estimate)):
        pcterrors.append(abs(estimate[i]-actual[i])/actual[i])
    
    return sum(pcterrors)/len(pcterrors)

def holtwinters(ts, *args):
    '''Holt-Winters exp. smoothing method to forecast the next
       three points in a time series.  The second two arguments are 
       smoothing coefficients, alpha and beta.  If no coefficients are given,
       both are assumed to be 0.5.
       '''
       
    if len(args) >= 1:
        alpha = args[0]
       
    else:
        alpha = .5
        findcoeff = True
    
    if len(args) >= 2:
        beta = args[1]
    else:
        beta = .5
            
    if len(ts) < 3:
        print("ERROR: At least three points are required for TS forecast.")
        return 0
    
    est = []    #estimated value (level)
    trend = []  #estimated trend
    
    '''For first value, assume trend and level are both 0.'''
    est.append(0)
    trend.append(0)
    
    '''For second value, assume trend still 0 and level same as first          
        actual value'''
    est.append(ts[0])
    trend.append(0)
    
    '''Now roll on for the rest of the values'''
    for i in range(len(ts)-2):
        trend.append(beta*(ts[i+1]-ts[i])+(1-beta)*trend[i+1])
        est.append(alpha*ts[i+1]+(1-alpha)*est[i+1]+trend[i+2])
        
    
    '''now back-cast for the first three values that we fudged'''
    est.reverse()
    trend.reverse()
    ts.reverse()
    
    for i in range(len(ts)-3, len(ts)):
        trend[i] = beta*(ts[i-1]-ts[i-2])+(1-beta)*(trend[i-1])
        est[i] = alpha*ts[i-1]+(1-alpha)*est[i-1]+trend[i]
    
       
    est.reverse()
    trend.reverse()
    ts.reverse()
    
    '''and do one last forward pass to smooth everything out'''
    for i in range(2, len(ts)):
        trend[i] = beta*(ts[i-1]-ts[i-2])+(1-beta)*(trend[i-1])
        est[i]= alpha*ts[i-1]+(1-alpha)*est[i-1]+trend[i]
        
    
    '''Holt-Winters method is only good for about 3 periods out'''
    next3 = [alpha*ts[-1]+(1-alpha)*(est[-1])+beta*(ts[-1]-ts[-2])+(1-beta)*trend[-1]]
    next3.append(next3[0]+trend[-1])
    next3.append(next3[1]+trend[-1])
    
    return next3, MAPE(ts,est)