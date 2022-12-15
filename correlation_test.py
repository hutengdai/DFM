from platform import machine
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, kendalltau
from statannot import add_stat_annotation
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.special import softmax
from plotnine import *
import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent=4)
pprint.sorted = lambda x, key=None: x


def visual_judgefile(humanjudgefile,bilinear_judgement):

	data = pd.read_csv(
		humanjudgefile,
		sep=",",
		header=0,
		encoding="utf-8")

	machine_data = pd.read_csv(
		bilinear_judgement,
		sep=",",
		# header=0,
		names=["onset","score"],
		encoding="utf-8")

	# fig_human = (ggplot(data, aes('attestedness', 'likert_rating')) 
	# + geom_violin(data))
	# dir(fig)
	# fig_human.save('daland.png', dpi=300)

	data["machine_judgement"] = machine_data["score"]
	# newdata = data

	data = data.sort_values("likert_rating", ascending = False)
	data['rank'] = range(0, len(data))

	newdata = data[data["machine_judgement"] > -25]
	print(newdata)
	# breakpoint()
	pearsoncorr, _ = pearsonr(newdata['likert_rating'], newdata['machine_judgement'])
	print('Pearsons correlation: %.3f' % pearsoncorr)
	# 
	spearmancorr, _ = spearmanr(newdata['likert_rating'], newdata['machine_judgement'])
	print('Spearman correlation: %.3f' % spearmancorr)
	kendalltaucorr, _ = kendalltau(newdata['likert_rating'], newdata['machine_judgement'])
	print('Kentall correlation: %.3f' % kendalltaucorr)

	# fig = ggplot.scatterplot(data=data, x="machine_judgement", y="likert_rating")
	a = (ggplot(newdata, aes(x='machine_judgement', y='rank', color='attestedness', label = 'ortho')) + 
	geom_text())

	print(a)
	plt.savefig('correlation.png', dpi=300)

	# dir(fig)
	# + stat_smooth(method='lm')
	# + facet_wrap('~gear')
	# plt.show()
	
if __name__ == '__main__':
	# JudgementFile = 'data\\TurkishJudgement-MaxEnt-MaxOE1.txt'
	# JudgementFile = 'data\\TurkishJudgement-categorical.txt'
	# JudgementFile = 'data\\TurkishJudgement-probabilistic-100ep005lr.txt'
	# JudgementFile = 'data\\TurkishJudgementFile-tolerance.txt'
	# visual_judgefile_maxent(JudgementFile)


	humanJudgement = "data\\Daland_etal_2011__AverageScores.csv"
	pmi_judgement = "result\\induced_pmi_class_10_27.txt"
	ppmi_judgement = "result\\induced_ppmi_class_10_27.txt"
	binary_judgement = "result\\binary_feature_10_27.txt"
	ternary_judgement = "result\\ternary_feature_10_27.txt"

	nelson_judgement = "data\\Nelson_model_onset_judgement.txt"
	visual_judgefile(humanJudgement,ternary_judgement)

# bilinear:
# Pearsons correlation: -0.798
# Spearman correlation: -0.842
# Kentall correlation: -0.651

# Nelson (<-25):
# Pearsons correlation: 0.742
# Spearman correlation: 0.780
# Kentall correlation: 0.621

# Nelson (>-25):
# Pearsons correlation: 0.742
# Spearman correlation: 0.780
# Kentall correlation: 0.621




