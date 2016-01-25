import argparse
import os
import glob
import re
import subprocess

def main(arg):
    project = os.path.split(os.path.realpath(arg.source))[1]
    move_from_path = "{}/*/results/".format(arg.source)
    pathway = glob.glob(move_from_path)
    pattern = re.compile(r"^(?:\\.|[^/\\])*/((?:\\.|[^/\\])*)/")
    samples = []
    for path in pathway:
        try:
            samples.append(pattern.match(path).groups()[0])
        except IndexError:
            pass
    
    
    for sample in samples:
        dest = "/proj/{}/INBOX/{}/QC_analysis/{}".format(arg.uppnexid,project,sample)
        cmd = ["rsync", "-auhv", "{}/{}/results".format(arg.source, sample), dest]
        subprocess.call(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type = str,
            help= "Path to QC analysis folder")
    parser.add_argument("--uppnexid", required=True, type = str,
            help =("Destination Uppnex id"))
    projectID = parser.parse_args()
    main(projectID)


