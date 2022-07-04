delta = 30
alpha = [[0,110,48,94] ,[110,0,118,48], [48,118,0,110], [94,48,110,0]]
ai = ['A','C','G','T']

def getAlpha(x, y):
    return alpha[ai.index(x)][ai.index(y)]

def bottom_up(X,Y):
    m = len(X) + 1
    n = len(Y) + 1
    
    dp = [[0 for _ in range(n)] for _ in range(m)]
    
    for i in range(m):
        for j in range(n):
            
            if i == 0 and j == 0:
                continue
                
            if i == 0:
                dp[i][j] = delta * j
                continue
                
            if j == 0:
                dp[i][j] = delta * i
                continue
                
            dp[i][j] = min(getAlpha(X[i-1],Y[j-1]) + dp[i-1][j-1], delta + dp[i-1][j], delta + dp[i][j-1])
    
    return dp, dp[-1][-1]

def top_down(dp,X,Y):
    result_1 = ''
    result_2 = ''
    
    # m = len(X) + 1
    # n = len(Y) + 1

    i = len(X)
    j = len(Y)

    while True:

        if i ==0 and j == 0:
            break

        if i == 0:
            result_1 += '_'
            result_2 += Y[j-1]
            j -= 1
            continue

        if j == 0:
            result_1 += X[i-1]
            result_2 += '_'
            i -= 1
            continue

        diagonal = getAlpha(X[i-1],Y[j-1]) + dp[i-1][j-1]
        left = delta + dp[i][j-1]
        top = delta + dp[i-1][j]

        min_value = min(diagonal, left, top)
        
        if min_value == diagonal:
            result_1 += X[i-1]
            result_2 += Y[j-1]
            i -= 1
            j -= 1
        
        elif min_value == left:
            result_1 += '_'
            result_2 += Y[j-1]
            j-=1
        
        elif min_value == top:
            result_1 += X[i-1]
            result_2 += '_'
            i-= 1
        
    return result_1[::-1], result_2[::-1]


def NeedlemanWunsch(X, Y):
    
    dp, alignCost = bottom_up(X,Y)
    alignment_1, alignment_2 = top_down(dp,X,Y)
    print(alignCost)
    return alignment_1, alignment_2

print(NeedlemanWunsch(input(),input()))