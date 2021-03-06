import numpy as n
import matplotlib.pyplot as p
from scipy.optimize import curve_fit

# Fitting to an exponential model
def exponential(x, a, b):
    return a*n.exp(b*x)

# Fitting to a logistic curve
def logistic(x, a, b, c):
    return a/(1+n.exp(-b*(x-c)))

# Current cases
cases = n.array([126, 166, 196, 210, 256, 285, 294, 327, 366, 402, 456, 495, 536, 576, 609, 656, 710, 779, 865, 985, 1070, 1173, 1322, 1450, 1560, 1699, 1794, 1939]) # Source: The Egyptian Minstry of Health official statements
day = n.arange(0, len(cases), 1)

# Expectations a week later
z = []
for i in range(len(cases)-1):
    z.append(cases[i+1]/cases[i])
mult = n.array(z)
av = n.average(mult) # This value is fed to daily-new-cases.py

u = [cases[len(cases)-1]]
for i in range(7):
    u.append(u[i]*av)
case_model = n.array(u)
day_model = n.arange(len(cases)-1, len(cases)+7, 1)

# Expectations a week earlier
past_expectations = n.array([1144, 930, 709, 902, 910, 809, 867, 948, 1008, 1139, 1071, 1265, 1324, 1357, 1435, 1532, 1669, 1850, 2124, 2285, 2492, 2819, 3077, 3278, 3550, 3699, 3971]) # Data are input from the Google Sheets analysis
day_past_exp = n.arange(9, len(past_expectations)+9, 1)

# Curve fitting
fit_parameters1, covariances = curve_fit(exponential, day, cases) # Fitting current cases
fit_parameters2, covariances = curve_fit(exponential, day_past_exp, past_expectations) # Fitting cases expected a week earlier
# fit_parameters3, covariances = curve_fit(logistic, day, cases) # Fitting current cases

# R-squared calculation
correlation_matrix1 = n.corrcoef(day, exponential(day, *fit_parameters1))
correlation_matrix2 = n.corrcoef(day_past_exp, exponential(day_past_exp, *fit_parameters2))
# correlation_matrix3 = n.corrcoef(day, logistic(day, *fit_parameters3))

correlation_xy1 = correlation_matrix1[0, 1]
correlation_xy2 = correlation_matrix2[0, 1]
# correlation_xy3 = correlation_matrix3[0, 1]

r_sq1 = correlation_xy1**2
r_sq2 = correlation_xy2**2
# r_sq3 = correlation_xy3**2


a = p.subplot() # Was called because it has the ability to delete top and right frameline from the plot

# Constructing lists to be used for the plot legend
FP1 = list(fit_parameters1)
FP2 = list(fit_parameters2)
# FP3 = list(fit_parameters3)

FP1.append(r_sq1)
FP2.append(r_sq2)
# FP3.append(r_sq3)

# Plotting current cases
a.plot(day, cases, "Dr")
a.plot(day, exponential(day, *fit_parameters1), "--b", label = "Current Model: %.1f $e^{%.2f}$ ($R^{2}$ = %.4f)" % tuple(FP1))
# a.plot(day, logistic(day, *fit_parameters3), "--b", label = "Current Model: %.2f/(1 + $e^{-%.2f (x - %.2f)}$) ($R^{2}$ = %.4f)" % tuple(FP3))


# Plotting cases expected a week later
a.plot(day_model, case_model, ":b", label = "Average Multiplication Factor = %.2f" %av)

# Plotting cases expected a week earlier
a.plot(day_past_exp, past_expectations, "Dg")
a.plot(day_past_exp, exponential(day_past_exp, *fit_parameters2), "--r", label = "Expected Cases a Week Earlier: %.1f $e^{%.2f}$ ($R^{2}$ = %.4f)" % tuple(FP2))


p.legend()
p.xlabel("Days Since 15 March")
p.ylabel("Confirmed Cases")
p.title("COVID-19 in Egypt")
p.grid("off")

# Writing the number of cases above points

p.annotate(past_expectations[len(past_expectations)-1], (day_past_exp[len(day_past_exp)-1], past_expectations[len(past_expectations)-1]), textcoords = "offset points", xytext = (0, 10), ha = "center")

# Deleting the top and right framelines
a.spines['right'].set_visible(False)
a.spines['top'].set_visible(False)

# Forcing the x-axis to integers
p.xticks(range(0, len(cases)+8, 5))

p.show()

# Values to be fed into daily-new-cases.py
exponent = FP1[1]
