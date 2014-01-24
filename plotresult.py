import pylab as pl
import numpy as np
import seaborn as sns
import pandas as pd


def lineplot(title, results):
	fig = pl.figure()

	minval = np.inf; maxval = -np.inf
	for key in results.keys():
		result = results[key][0]
		mean = np.mean(result, axis=0)
		std = np.sqrt(np.var(result, axis=0))
		minvali = np.min(mean-std); maxvali = np.max(mean+std);
		if minvali < minval:
			minval = minvali
		if maxvali > maxval:
			maxval = maxvali

		x_indices = np.arange(mean.shape[0])+1

		a = sns.tsplot(result, err_style="boot_traces", \
			n_boot=result.shape[0], label=key, color=results[key][1])
		# pl.fill_between(x_indices, mean-std, mean+std, \
		# 	facecolor=results[key][1], alpha=0.2)
		# a = pl.plot(x_indices, mean, color=results[key][1], \
		# 	linestyle='-', linewidth=4.0, label=key)

	pl.legend(borderaxespad=0.2)
	pl.ylabel('Log Distance to optimal', fontsize=20)
	pl.xlabel('No. of Fct. Evaluations ($t$)', fontsize=20)
	# pl.axis([1, 100, minval-0.1, maxval+0.1])

	pl.title(title, fontsize=20)

	pl.savefig('{}.pdf'.format(title), bbox_inches='tight', dpi=200)
	fig.clf()

def seaborn_plot():
	

	def sine_wave(n_x, obs_err_sd=1.5, tp_err_sd=.3):
	    x = np.linspace(0, (n_x - 1) / 2, n_x)
	    y = np.sin(x) + np.random.normal(0, obs_err_sd) + np.random.normal(0, tp_err_sd, n_x)
	    return y

	sines = np.array([sine_wave(31) for _ in range(20)])
	sns.tsplot(sines);

	pl.show()



if __name__ == '__main__':
	resultBrEI = np.load('./results/result-braninpy-7859558362.npy')[:, :100]
	resultBrT = np.load('./results/out-branin-8683685435.npy')[:, :100]

	results = {'EI-MCMC':(resultBrEI, 'blue'), \
			   'Thompson-MCMC':(resultBrT, 'green')}
	title = 'Branin'
	lineplot(title, results)

	resultBrEI = np.load('./results/result-hart3py-7277509593.npy')[:, :100]
	resultBrT = np.load('./results/out-hart3-2626550518.npy')[:, :100]

	results = {'EI-MCMC':(resultBrEI, 'blue'), \
			   'Thompson-MCMC':(resultBrT, 'green')}
	title = 'Hartmann 3'
	lineplot(title, results)


	# seaborn_plot()
