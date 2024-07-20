# needs Python >=3.7
from subprocess import run
from re import findall
import argparse
#get data with cdo
#change paths if necessary
parser = argparse.ArgumentParser(description='Evaluate ICON-Output.')
parser.add_argument('folder',type=str, help='path to the ICON-Output')
parser.add_argument('grid',type=int, help='Grid used by ICON')
parser.add_argument('jubeid',type=int, nargs='?',default=0, help='ID of the Jube-step, leave it empty if Jube is not used')
args=parser.parse_args()
outpath=args.folder

if(args.jubeid != 0):
    exps = args.jubeid-int(run(f'''ls -ld {outpath}/0*_execute|wc -l''',shell=True,check=True,capture_output=True).stdout)
    outpath += f'''{exps:06d}_execute/work/'''

print(str(outpath))
output=open('evaluation.out','w')
day=""
grid = args.grid
if grid == 1 or grid == 2 or grid == 5:
    day="20180609T000000Z"
elif grid == 3:
    day="20180402T000000Z"
elif grid == 4:
    day="20210712T020000Z"
    



data = run(f'''ml Stages/2022 Intel ParaStationMPI CDO
#ps
cdo infov {outpath}/*_ps_ml_{day}.grb
echo ";"
#ta
cdo infov {outpath}/*_ta_ml_{day}.grb
echo ";"
#ua
cdo infov {outpath}/*_ua_ml_{day}.grb
echo ";"
#va
cdo infov {outpath}/*_va_ml_{day}*.grb
echo ";"
#wa
cdo infov {outpath}/*_wa_ml_{day}.grb
''',shell=True,text=True,check=True,capture_output=True)
arr = str(data.stdout).split(";")
#boundaries for the tests
mini = [ 36000, 172, -80,-80, -30 ]
names = [ "ps", "ta", "ua", "va", "wa" ]
maxi = [ 1.08e+5, 330, 105, 80, 35 ]
meani = [[ 98500, 98600 ], [ 200 , 300 ], [ -2, 20 ], [ -2, 2 ], [ -0.01, 0.01 ]]
var = 0
ver = True

for dats in arr:
    #find the data in the CDO output
    mins = findall(r": +(-?\d+\..{0,8}) +-?\d",dats)
    maxs = findall(r"[\d|\.] +(-?\d+\..{0,8}) :",dats)
    means = findall(r"[\d|\.] +(-?\d+\..*\d?) +-?\d",dats)
    #verify data with given boundaries
    check = True
    if len(mins) < 1 or len(maxs) < 1 or len(means) < 1:
        check = False
    for dat in mins:
        if not (float(dat) >= mini[var] and float(dat) <= maxi[var]):
            check = False
    for dat in maxs:
        if not (float(dat) >= mini[var] and float(dat) <= maxi[var]):
            check = False
    for dat in means:
        if not (float(dat) >= meani[var][0] and float(dat) <= meani[var][1]):
           check = False
    #output
    output.write(f''' {names[var]}: {check} \n''')
    if not check:
        ver = False
    var += 1
if ver:
    output.write(f'''Verification has run successfully''')
else:
    output.write(f'''Verification has failed ''')



    

