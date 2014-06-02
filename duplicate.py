import re, os, sys, getopt
import distutils.core
import re
import random

def write_PBS_script(num, path, codeline, serial):
    content = """
#!/bin/bash
#PBS -S /bin/bash

#!/bin/sh
# Script for running serial program, diffuse.

#PBS -l walltime=02:00:00
#PBS -l mem=4000mb
#PBS -t 1-{}
#PBS -r n
#PBS -M ziyucwang@gmail.com
#PBS -m bea
#PBS -V
#PBS -l nodes=1:ppn=2

cd $PBS_O_WORKDIR
echo "Current working directory is `pwd`"
echo PBS_ARRAYID=$PBS_ARRAYID
# Run
echo "Starting run: $(date)"
{}
echo "Run complete: $(date)"
""".format(num, codeline)
    
    fname = path + 'job_scripts_{}.pbs'.format(serial)
    f = open(fname, 'w')
    f.write(content)
    f.close()

    return fname


def write_bash_script(num, single_num, path, codeline, serial, name, method):
    outerloop = "#!/bin/bash"

    for i in range(num/single_num):
        indices = [str(k + i*single_num) for k in range(1, single_num+1)]
        indices = ' '.join(indices)

        innerloop = """
    for i in {}; do
        {}
    done

    for job in `jobs -p`
    do
        wait $job || let "FAIL+=1"
    done

    echo $FAIL""".format(indices, codeline)
        outerloop = outerloop + "\n" + innerloop

    outerloop = outerloop + "\n"
    
    fname = path + 'loop_{}_{}_{}.sh'.format(name, method, serial)
    f = open(fname, 'w')
    f.write(outerloop)
    f.close()

    return fname

def getPath(subfolder):
    lpath = re.sub(r'duplicate.pyc?', subfolder, \
        os.path.abspath(__file__))
    return lpath

def prepareSpearmint(name='braninpy', num=20, method=1, max_num=100, \
    noiseless=0, use_grad=0, additionals=None):

    methods = ['GPEIOptChooser', 'GPThompsonOptChooser', \
               'GPPortOptChooser', 'GPEIRobustChooser', \
               'GPPortEntChooser', 'GPPortHedgeChooser']

    origPath = getPath('fcts/{}/'.format(name))


    serial = str(random.randint(1e9, 1e10))
    
    for i in range(num):
        destPath = getPath('{0}/{1}-{2}-{3}/'.format(\
            'copies', name, serial, i+1))
        os.mkdir(destPath)
        distutils.dir_util.copy_tree(origPath, destPath)
        write_additionals(destPath, additionals)

    line = '{}job_scripts/runscript.sh {} {} $PBS_ARRAYID {} {} {} {}'.\
        format(getPath(''), name, serial, methods[method], \
        max_num, noiseless, use_grad)

    fname = write_PBS_script(num, getPath('job_scripts/'), line, serial)


    execute = 'qsub -l walltime=5:00:00,mem=2gb {}'.format(fname)
    print execute

    return serial


def prepareSpearmint_loop(name='braninpy', num=20, single_num=4, method=1, \
    max_num=100, noiseless=0, use_grad=0):

    methods = ['GPEIOptChooser', 'GPThompsonOptChooser', \
               'GPPortOptChooser', 'GPEIRobustChooser']

    origPath = getPath('fcts/{}/'.format(name))


    serial = str(random.randint(1e9, 1e10))
    
    for i in range(num):
        destPath = getPath('{0}/{1}-{2}-{3}/'.format(\
            'copies', name, serial, i+1))
        os.mkdir(destPath)
        distutils.dir_util.copy_tree(origPath, destPath)


    line = '{}job_scripts/runscript.sh {} {} $i {} {} {} {} &'.\
        format(getPath(''), name, serial, methods[method], \
        max_num, noiseless, use_grad)

    fname = write_bash_script(num, single_num, getPath('job_scripts/'), \
        line, serial, name, method)

    print fname

    return serial

def write_additionals(path, additionals):
    import yaml
    with open('{}add.yaml'.format(path), 'w') as yaml_file:
        yaml_file.write(yaml.dump(additionals, default_flow_style=True))



def preparePybo(name='branin', num=20):

    serial = str(random.randint(1e9, 1e10))
    line = 'python {}job_scripts/runSynthetic.py -n {} -s {} -a $PBS_ARRAYID'.\
        format(getPath(''), name, serial)
    fname = write_PBS_script(num, getPath('job_scripts/'), line, serial)
    execute = 'qsub -l walltime=5:00:00,mem=4gb {}'.format(fname)
    print execute

    return serial

def parse_yaml(yaml_file):
    import yaml
    f = open(yaml_file)
    dataMap = yaml.safe_load(f)
    f.close()

    for key in dataMap.keys():
        prepareSpearmint(**dataMap[key])

def main(argv):
    config_file = ''
    usage = 'duplicate.py -f <file>'
    try:
        opts, args = getopt.getopt(argv,"hf:",["file="])
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt in ("-f", "--file"):
            config_file = arg

    if not (config_file == ''):
        parse_yaml(config_file)


if __name__ == '__main__':
    main(sys.argv[1:])


    # prepareSpearmint('rfpy', 20, method=1, max_num=200, \
    #   noiseless=0, use_grad=0)
    #prepareSpearmint_loop('svm_grid', 20, 5, method=1, max_num=100, \
    #    noiseless=0, use_grad=0)
    #prepareSpearmint_loop('braninpy', 20, 5, method=1, max_num=100, \
    #    noiseless=1, use_grad=1)
    #prepareSpearmint_loop('lda_grid', 20, 5, method=1, max_num=50, \
    #    noiseless=0, use_grad=0)

    # prepareSpearmint('hart3py', 20, method=4, max_num=100, \
    #     noiseless=1, use_grad=1)

    # prepareSpearmint('braninpy', 20, method=4, max_num=100, \
    #     noiseless=1, use_grad=1)


    # prepareSpearmint('lda_grid', 20, method=3, max_num=50, \
    #    noiseless=0, use_grad=0)

    # prepareSpearmint('svm_grid', 20, method=3, max_num=100, \
    #    noiseless=0, use_grad=0)

    #prepareSpearmint('logistic_hpolib', 20, method=3, max_num=100, \
    #   noiseless=0, use_grad=1)

    # prepareSpearmint('logistic', 20, method=0, max_num=100, \
    #   noiseless=0, use_grad=1)

    
    # prepareSpearmint('logistic_hpolib', 20, method=3, max_num=100, \
    #   noiseless=0, use_grad=1)
    
    # prepareSpearmint('repeller', 20, method=3, max_num=200, \
    #    noiseless=0, use_grad=1)

    # preparePybo('branin', 20)
    # preparePybo('rfpy', 20)
    # copyFolder('hart3py', 20)
    # copyFolder('hart6py', 20)

    
    
