from scipy.stats import describe

ncites     = [ 1703, 4186, 12430, 967, 2362, 26303, 36547, 1051, 222, 1367, 265, 10, 1411, 6015, 17, 3880, 1402, 243, 1121, 3989, 5270, 3786, 6298, 814, 6438, 2232, 1482, 2748, 8218, 5837, 137, 1902, 1212, 9977, 10290, 6700, 5005, 4859, 15532, 6327, 1915, 1177, 8475]
hindices   = [ 41, 25, 66, 19, 34, 99, 84, 23, 6, 32, 9, 3, 20, 52, 2, 49, 26, 11, 22, 38, 38, 47, 32, 24, 45, 35, 33, 54, 60, 53, 8, 36, 29, 67, 41, 36, 45, 38, 82, 51, 26, 26, 37]
i10indices = [ 85, 33, 131, 26, 106, 219, 149, 39, 5, 45, 9, 2, 32, 141, 1, 113, 41, 11, 35, 70, 54, 112, 51, 32, 71, 58, 50, 81, 116, 103, 8, 64, 52, 136, 66, 90, 84, 55, 220, 139, 34, 41, 72]

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

ncites     = [ 4186, 12430, 967, 1367, 1411, 6015, 3880, 1121, 3989, 5270, 814, 2232, 1482, 2748, 1212, 10290, 6700, 5005, 15532, 1915, 1177, 8475 ]
hindices   = [25, 66, 19, 32, 20, 52, 49, 22, 38, 38, 24, 35, 33, 54, 29, 41, 36, 45, 82, 26, 26, 37 ]
i10indices = [ 33, 131, 26, 45, 32, 141, 113, 35, 70, 54, 32, 58, 50, 81, 52, 66, 90, 84, 220, 34, 41, 72 ]

dn = describe(ncites, 0, 1)
print('ncites count = %d' % dn.nobs)
print('ncites sum  = %d' % sum(ncites))

dh = describe(hindices, 0, 1)
print('h count = %d' % dh.nobs)
print('h mean  = %.2f' % dh.mean)

di = describe(i10indices, 0, 1)
print('i10 count = %d' % di.nobs)
print('i10 mean  = %.2f' % di.mean)

