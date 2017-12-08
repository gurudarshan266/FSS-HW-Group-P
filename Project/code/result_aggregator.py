import glob
import computation_config as cc
if __name__ == '__main__':
    goal = 'accuracy'
    results_base_dir = "../results/%s/"%goal

    tuned_scores = {}
    untuned_scores = {}

    for dataset in cc.datasets:
        file = "%s%s_results.csv" % (results_base_dir, dataset)

        with open(file,"r") as f:
            tuned_scores[dataset] = []
            untuned_scores[dataset] = []

            print("Scanning %s"%dataset)
            lines = f.readlines()
            lines = [ l.strip() for l in lines]

            for line in lines:
                if 'Tuning Times' in line or len(line)==0:
                    break
                elif line.startswith('Learner'):
                    continue
                tuned_score = line.split("|")[-1]
                tuned_scores[dataset].append(float(tuned_score))

                untuned_score = line.split("|")[-2]
                untuned_scores[dataset].append(float(untuned_score))




    print (cc.learners)
    for dataset in cc.datasets:
        print(dataset)
        print(untuned_scores[dataset])
        print (tuned_scores[dataset])
        print()
    # print (untuned_scores)