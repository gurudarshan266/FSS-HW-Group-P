import glob
import computation_config as cc
if __name__ == '__main__':
    goal = 'f1'
    results_base_dir = "../results/%s/"%goal

    rf_scores = []
    ensemble_scores = []

    for dataset in cc.datasets:
        file = "%s%s_results.csv"%(results_base_dir,dataset)
        with open(file,"r") as f:
            print("Scanning %s"%dataset)
            lines = f.readlines()
            lines = [ l.strip() for l in lines]

            for line in lines:
                if line.startswith('rf'):
                    score = line.split("|")[-1]
                    rf_scores.append(float(score))
                elif line.startswith('tuned_ensemble' ):
                    score = line.split("|")[-1]
                    ensemble_scores.append(float(score))
                elif 'Tuning Times' in line:
                    break

    print (cc.datasets)
    print (rf_scores)
    print (ensemble_scores)
