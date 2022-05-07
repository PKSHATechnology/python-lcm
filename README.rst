################################
LCM: Linear time Closed itemset Miner
################################

TODO

- Refactoring lcm and publish on github.  Now, lcm install method is too old.
- Use Cython to call lcm.  Maybe Cython is most useful to call a module implemented by c language.
- version control and publish to PyPI


********************************
Install
********************************

Install LCM ver. 5.3, and set PATH to run `lcm`.
ref. http://research.nii.ac.jp/~uno/codes-j.htm

Install as module ::

	pip install git+ssh://git@github.com/YuseiYokoyama/python-lcm.git
	#pip install git+ssh://git@github.com/YuseiYokoyama/python-lcm.git@master
	#pip install git+ssh://git@github.com/YuseiYokoyama/python-lcm.git@v0.1.0

Uninstall ::

	pip uninstall lcm


********************************
Related
********************************

fp grouth is also frequent itemset mining algorithm.

- provided a python implemented module in mlxtend.
  https://github.com/rasbt/mlxtend/blob/2362d9f53cb715a88cda63a8a7e69793afd64cbd/mlxtend/frequent_patterns/fpgrowth.py
- also output not closed pattern

So, LCM is faster.

