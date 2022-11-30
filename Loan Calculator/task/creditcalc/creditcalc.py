import math
import argparse


# GLOBAL SETTINGS
parser = argparse.ArgumentParser(prog='creditcalc.py',
                                 description='calculate loan repayments for annualised and differentiated repayments')
parser.add_argument('--type', action='store', choices=['annuity', 'diff'], required=True,
                    help='set the type of calculation required. Must be "annuity" or "diff"')
parser.add_argument('--payment', action='store', type=float,
                    help='monthly payment amount. Not valid with --type=diff')
parser.add_argument('--principal', action='store', type=float,
                    help='value of loan required. \
                    May be calculated if given interest, annuity payment, and \
                    number of monthly repayment')
parser.add_argument('--periods', action='store', type=int,
                    help="the number of months needed to repay the loan. \
                    It's calculated based on the interest, annuity payment, and principal.")
parser.add_argument('--interest', action='store', type=float, required=False,
                    help="Required yearly interest rate as a percentage value without '%' sign")
args = parser.parse_args()
params_ok = True


def annuity(args_dict):
    if not params_ok:
        return
    if args_dict['m'] is None:
        ans = 'n'
        prin = args_dict['prin']
        pmt = args_dict['pmt']
        rate = args_dict['rate']
    elif args_dict['pmt'] is None:
        ans = 'a'
        prin = args_dict['prin']
        m = args_dict['m']
        rate = args_dict['rate']
    elif args_dict['prin'] is None:
        ans = 'p'
        m = args_dict['m']
        pmt = args_dict['pmt']
        rate = args_dict['rate']
    if ans == 'n':
        i = rate / 1200.00    # monthly rate as a fraction
        m = math.ceil(math.log((pmt / (pmt - (i * prin))), (1 + i)))
        yrs = m // 12
        mth = m % 12
        plural_m = plural_y = 's'
        if mth == 1:
            plural_m = ''
        if yrs == 1:
            plural_y = ''
        if yrs == 0:
            print(f'It will take {mth} month{plural_m} to repay this loan!')
        elif mth == 0:
            print(f'It will take {yrs} year{plural_y} to repay this loan!')
        else:
            print(f'It will take {yrs} year{plural_y} and {mth} month{plural_m} to repay this loan!')
    elif ans == 'a':
        i = rate / 1200.00    # monthly rate as a fraction
        pmt = math.ceil(prin * (i * ((1 + i) ** m)) / (((1 + i) ** m) - 1))
        print('Your monthly payment = {}!'.format(pmt))
    elif ans == 'p':
        i = rate / 1200.00    # monthly rate as a fraction
        prin = round((pmt / ((i * ((1 + i) ** m)) / (((1 + i) ** m) - 1))), 2)
        print('Your loan principal = {}!'.format(prin))
    print('Overpayment =', math.ceil((pmt * m) - prin))


def differentiate(args_dict):
    if not params_ok:
        return
    m = args_dict['m']
    # pmt = args_dict['pmt']
    prin = args_dict['prin']
    rate = args_dict['rate']
    i = rate / 1200.00    # monthly rate as a fraction
    total_pmt = 0.0
    for j in range(1,m+1):
        d = math.ceil((prin / m) + (i * (prin - ((prin * (j - 1)) / m))))
        total_pmt += d
        print(f"Month {j}: payment is {d}")
    print('Overpayment =', math.ceil(total_pmt - prin))


def args_count(arg_namespace):
    ct = 0
    for x in vars(arg_namespace).values():
        if x is not None:
            ct += 1
    return ct


# MAIN starts here...
if args.interest is None:
    params_ok = False
if args.type == 'diff' and args.payment is not None:
    params_ok = False
if args_count(args) < 4:
    params_ok = False
params_d = {'prin': args.principal, 'pmt': args.payment, 'm': args.periods, 'rate': args.interest}
if args.type == 'annuity':
    annuity(params_d)
elif args.type == 'diff':
    differentiate(params_d)
else:
    params_ok = False
if not params_ok:
    print("Incorrect parameters")
