# Impact of tuning on Ensemble learners

## Description
The project compares the performance (F1-score and Accuracy) of ensemble learners with that of individual learners.


Start by downloading all the datasets required by the project by executing the `getDataset.sh` script. The list of datasets used in this project are:
* IVY
* JEDIT
* LUCENE
* VELOCITY
* XALAN
* XERCES


After all the datasets are successfully downloaded, run:<br>
`python3 run.py <dataset> <f1|accuracy>`
<br><br>

Alternatively, `multi_run.sh` can be executed which deploys multiple jobs of `run.py` (in parallel) each working on a single dataset.

---

## Algorithm flow
1. Fetches 4 versions of the data namely i) `train`, ii) `tune`, iii) `test`, iv) `merged`. Function of the individual versions are explained in the report. 

2. SMOTE is applied on `train` and `merged`. None of the test datasets are SMOTEd. SMOTE is performed by `preprocess()` in `preprocess.py`. It uses SMOTE from `imblearn` package.

3. All the learners are tuned using Differential Evolution from `DiffentialEvolutionTuner()` in `DE.py`.

4. The output of the learners are written to the file `../results/<goal>/<dataset>_results.csv`. For example, if `run.py` was called for Lucene dataset and Accuracy as the goal, the file would be named `../results/f1/lucene_results.csv`. The contents of the file are in the following format:<br>

Learner | Best parameters (computed by the tuner) | Untuned Score | Tuned Score
--- | --- | --- | ---

5. Applying the "Best Parameters" obtained from the tuner, the learners will perform a 5x5 Cross validation on the dataset. Their results are stored in `../results/<goal>/<dataset>.kout`

6. Scott-Knott Test will be run on the `*.kout` file to obtain the ranks which will be used as weights by the ensemble learner.

7. With the weights computed and the learners, `VotingClassifier` is created whose parameters are the union of all the parameters of all the constituent learners.

8. Best Parameters and the corresponding scores of the ensemble are written to `../results/<goal>/<dataset>_results.csv`.

9. A new ensemble is created by applying the best params to individual learners and the corresponding scores are captured and appended to the file `../results/<goal>/<dataset>_results.csv`.

