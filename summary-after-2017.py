from scipy.stats import describe

print('All faculty:')

ncites     = [1081,  3118, 13305, 744, 1723, 20541, 25835, 834, 182, 956, 223, 39, 1160, 4547, 15, 2461, 994, 270, 1150, 2562, 3651, 2516, 7306, 564, 4254, 1469, 961, 1777, 6074, 3964, 387, 4201, 887, 6965, 8127, 5893, 3792, 3218, 11027, 5077, 1678, 772, 6747]
hindices   = [  17,    22,    53,   15,    21,    73,  59,  17,   5,  17,  8,    3,   15, 33,    2,  22,  15,    9,   21,   25,   24,   24,  31,   14,   23,  21,   18,   24,   35,  23,    8,  34,   17,   43,   35,   27,   34,    19,   45,   37,  22,   17, 26 ]
i10indices = [  38,    31,   120,   19,    42,   192, 113,  26,   5,  31,  7,    2,   20, 95,    1,  50,  24,    7,   31,   52,   42,   55,  49,   22,   45,  35,   30,   44,   81,  65,    8,  62,   37,   99,   61,   55,   73,    31,  160,   93,  30,   24, 55 ]

dn = describe(ncites, 0, 1)
print('ncites count = %d' % dn.nobs)
print('ncites sum  = %d' % sum(ncites))

dh = describe(hindices, 0, 1)
print('h count = %d' % dh.nobs)
print('h mean  = %.2f' % dh.mean)

di = describe(i10indices, 0, 1)
print('i10 count = %d' % di.nobs)
print('i10 mean  = %.2f' % di.mean)

print('\nCurrent tenure-track faculty only:')

ncites     = [ 3118, 13305, 744, 956, 1160, 4547, 2461, 1150, 2562, 3651, 564, 1469, 961, 1777, 887, 8127, 5893, 3792, 11027, 1678, 772, 6747 ]
hindices   = [22, 53, 15, 17, 15, 33, 22, 21, 25, 24, 14, 21, 18, 24, 17, 35, 27, 34, 45, 22, 17, 26 ]
i10indices = [ 31, 120, 19, 31, 20, 95, 50, 31, 52, 42, 22, 35, 30, 44, 37, 61, 55, 73, 160, 30, 24, 55 ]

dn = describe(ncites, 0, 1)
print('ncites count = %d' % dn.nobs)
print('ncites sum  = %d' % sum(ncites))

dh = describe(hindices, 0, 1)
print('h count = %d' % dh.nobs)
print('h mean  = %.2f' % dh.mean)

di = describe(i10indices, 0, 1)
print('i10 count = %d' % di.nobs)
print('i10 mean  = %.2f' % di.mean)

