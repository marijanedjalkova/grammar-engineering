from Grammar import *
import sys, getopt

cfg_str ="""\

	# Grammar

	S -> Statement
	S -> Question 
	S -> SBAR 
	SBAR -> WhP Statement Statement  

	Statement -> NP[NUM=?n, PER=?p] VP[NUM=?n, PER=?p, SUBCAT=nil] 

	Question -> WhP SQ 
	WhP -> WhNP | WhADVP
	WhNP -> WP | WDT Nominal 
	WhADVP -> WRB 
	SQ -> Auxiliary[NUM=?n, PER=?p] NP[NUM=?n, PER=?p] VP[NUM=pl, SUBCAT=nil]

	NP[NUM=pl] -> NP CC NP
	NP[NUM=?n, PER=?p] -> DT[NUM=?n] Nominal[NUM=?n] | Nominal[NUM=?n] | ProperNoun[NUM=?n, PER=?p] | Pronoun[NUM=?n, PER=?p] | AP NP[NUM=?n] | NP[NUM=?n] PP
	GERUND -> V[TENSE=prespart, SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg] | V[TENSE=prespart, SUBCAT=nil]

	VP[NUM=?n, PER=?p, TENSE=?t, SUBCAT=?rest] -> VP[NUM=?n, PER=?p, TENSE=?t, SUBCAT=nil] CC VP[NUM=?n, PER=?p, SUBCAT=nil] 
	VP[NUM=?n, PER=?p, TENSE=?t, SUBCAT=?rest] -> VP[NUM=?n, PER=?p, TENSE=?t, SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg]
	VP[NUM=?n, PER=?p, TENSE=pres, SUBCAT=?args] -> V[NUM=?n, PER=?p, TENSE=pres, SUBCAT=?args]  
	VP[NUM=?n, PER=?p, TENSE=past, SUBCAT=?args] -> V[NUM=?n, PER=?p, TENSE=past, SUBCAT=?args] 
	VP[NUM=?n, PER=?p, TENSE=prespart, SUBCAT=?args] -> BE[NUM=?n, PER=?p] V[TENSE=prespart, SUBCAT=?args] 

	VP[NUM=?n, PER=?p, TENSE=?t, SUBCAT=nil] -> RB VP[NUM=?n, PER=?p, TENSE=?t, SUBCAT=?args]
	VP[NUM=?n, PER=?p, TENSE=pres, SUBCAT=nil] -> MD VP[NUM=pl, TENSE=presperf, PER=?p, SUBCAT=nil] | MD VP[NUM=pl, TENSE=pres, PER=?p, SUBCAT=nil]
	VP[NUM=?n, TENSE=presperf, SUBCAT=?args] -> HV[NUM=?n, PER=?p, TENSE=pres] V[TENSE=pastpart, SUBCAT=?args]

	AP -> RB JJ | JJ
	Nominal[NUM=?n] -> Nominal[NUM=?n] Noun[NUM=?n] | Noun[NUM=?n] 
	PP -> IN NP

	ARG[CAT=np] -> NP
	ARG[CAT=vp] -> VP
	ARG[CAT=pp] -> PP
	ARG[CAT=ap] -> AP
	ARG[CAT=st] -> Statement
	ARG[CAT=gd] -> GERUND

	# Words

	V[NUM=sg, TENSE=pres, PER=3, SUBCAT=nil] -> 'barks' | 'laughs' | 'eats'
	V[NUM=sg, TENSE=pres, PER=3, SUBCAT=[HEAD=np, TAIL=[HEAD=pp, TAIL=nil]]] -> 'puts' 
	V[NUM=sg, TENSE=pres, PER=3, SUBCAT=[HEAD=np, TAIL=nil]] -> 'eats' | 'drinks' | 'likes' | 'has'
	V[NUM=sg, TENSE=pres, PER=3, SUBCAT=[HEAD=gd, TAIL=nil]] -> 'likes'
	V[NUM=sg, TENSE=pres, PER=3, SUBCAT=[HEAD=np, TAIL=nil]] -> 'feeds'
	V[NUM=sg, TENSE=pres, PER=3, SUBCAT=[HEAD=np, TAIL=[HEAD=np, TAIL=nil]]] -> 'feeds' | 'does'
	V[NUM=sg, TENSE=pres, PER=3, SUBCAT=[HEAD=st, TAIL=nil]] -> 'thinks' | 'says'

	V[NUM=pl, TENSE=pres, SUBCAT=nil] -> 'bark' | 'laugh' | 'eat'
	V[NUM=pl, TENSE=pres, SUBCAT=[HEAD=np, TAIL=[HEAD=pp, TAIL=nil]]] -> 'put' 
	V[NUM=pl, TENSE=pres, SUBCAT=[HEAD=np, TAIL=nil]] -> 'eat' | 'drink' | 'like' | 'have'
	V[NUM=pl, TENSE=pres, SUBCAT=[HEAD=gd, TAIL=nil]] -> 'like'
	V[NUM=pl, TENSE=pres, SUBCAT=[HEAD=np, TAIL=nil]] -> 'feed'
	V[NUM=pl, TENSE=pres, SUBCAT=[HEAD=np, TAIL=[HEAD=np, TAIL=nil]]] -> 'feed' | 'do'
	V[NUM=pl, TENSE=pres, SUBCAT=[HEAD=st, TAIL=nil]] -> 'think' | 'say'

	V[TENSE=past, SUBCAT=nil] -> 'barked' | 'laughed' | 'ate'
	V[TENSE=past, SUBCAT=[HEAD=np, TAIL=[HEAD=pp, TAIL=nil]]] -> 'put' 
	V[TENSE=past, SUBCAT=[HEAD=np, TAIL=nil]] -> 'ate' | 'drank' | 'liked' | 'had'
	V[TENSE=past, SUBCAT=[HEAD=gd, TAIL=nil]] -> 'liked'
	V[TENSE=past, SUBCAT=[HEAD=np, TAIL=nil]] -> 'fed'
	V[TENSE=past, SUBCAT=[HEAD=np, TAIL=[HEAD=np, TAIL=nil]]] -> 'fed' | 'did'
	V[TENSE=past, SUBCAT=[HEAD=st, TAIL=nil]] -> 'thought' | 'said'

	V[TENSE=pastpart, SUBCAT=nil] -> 'barked' | 'laughed' | 'eaten'
	V[TENSE=pastpart, SUBCAT=[HEAD=np, TAIL=[HEAD=pp, TAIL=nil]]] -> 'put' 
	V[TENSE=pastpart, SUBCAT=[HEAD=np, TAIL=nil]] -> 'eaten' | 'drunk' | 'liked' | 'had'
	V[TENSE=pastpart, SUBCAT=[HEAD=gd, TAIL=nil]] -> 'liked'
	V[TENSE=pastpart, SUBCAT=[HEAD=np, TAIL=nil]] -> 'fed'
	V[TENSE=pastpart, SUBCAT=[HEAD=np, TAIL=[HEAD=np, TAIL=nil]]] -> 'fed' | 'done'
	V[TENSE=pastpart, SUBCAT=[HEAD=st, TAIL=nil]] -> 'thought' | 'said'

	V[TENSE=prespart, SUBCAT=nil] -> 'barking' | 'laughing' | 'eating'
	V[TENSE=prespart, SUBCAT=[HEAD=np, TAIL=[HEAD=pp, TAIL=nil]]] -> 'putting' 
	V[TENSE=prespart, SUBCAT=[HEAD=np, TAIL=nil]] -> 'eating' | 'drinking' | 'liking' | 'having'
	V[TENSE=prespart, SUBCAT=[HEAD=np, TAIL=nil]] -> 'feeding'
	V[TENSE=prespart, SUBCAT=[HEAD=np, TAIL=[HEAD=np, TAIL=nil]]] -> 'feeding' | 'doing'
	V[TENSE=prespart, SUBCAT=[HEAD=st, TAIL=nil]] -> 'thinking' | 'saying'

	HV[NUM=sg, PER=3] -> 'has' 
	HV[NUM=pl] -> 'have'

	BE[NUM=sg, PER=1] -> 'am'
	BE[NUM=sg, PER=3] -> 'is'
	BE[NUM=pl] -> 'are'

 	Auxiliary[NUM=sg, PER=3] -> 'does'
 	Auxiliary[NUM=pl] -> 'do' | 'did'
 	ProperNoun[NUM=sg, PER=3] -> 'Gromit' | 'Wallace'
 	Pronoun[PER=1] -> 'I' | 'we'
 	Pronoun[PER=2] -> 'you'
 	Pronoun[NUM=sg, PER=3] -> 'he' | 'she' | 'it'
 	Pronoun[PER=3, NUM=pl] -> 'they' 
	Noun[NUM=sg] -> 'cheese' | 'water' | 'kitchen' | 'dinner'
	DT[NUM=sg] -> 'a' | 'an' 
	DT -> 'the' | 'my'
	IN -> 'in' | 'on' | 'at' | 'after' | 'when'
	JJ -> 'tasty' | 'soft' 
	CC -> 'and' | 'but' | 'or'
	RB -> 'seldom' | 'often'
	WRB -> 'when'
	WP -> 'what' 
	WDT -> 'what'
	MD -> 'should' | 'could' | 'may' | 'might'
	"""

valid = """\
Gromit barks
Gromit barked
Wallace and Gromit eat cheese
Wallace and Gromit ate cheese
Wallace feeds Gromit
Wallace seldom feeds Gromit cheese
Wallace thinks Gromit eats cheese and drinks water
Wallace often eats tasty soft cheese in the kitchen after dinner
when Gromit barks Wallace feeds Gromit
when does Wallace eat cheese
Wallace likes eating cheese
Wallace likes eating
Wallace should have fed Gromit cheese
what does Gromit eat 
what cheese does Gromit eat 
what cheese does Wallace think Gromit eats
I like you
you could have eaten the cheese
I think you think he thinks they think they like cheese
when I laugh you should feed Gromit
he has put water on the cheese
he thinks he has put cheese in the kitchen
he said he put the cheese in the kitchen
he said he thought they said they put cheese in the kitchen
"""

invalid = """\
Gromit and Wallace barks
Gromit likes doing
I likes you
Gromit bark
Gromit barking
Gromit eaten
when do Gromit eat cheese
Gromit barks the kitchen
Wallace should has feed Gromit cheese
Wallace should has fed Gromit cheese
Wallace should have feed Gromit cheese
I like
when I laugh
"""

def process_args(argv, argsdict):
	""" Processes args given in command line. """
	print argsdict
	try:
		opts, args = getopt.getopt(argv, "p:r:i:d",["toPrintValid=", "toPrintRepetitionsValid=", "toPrintInvalid=", "toPrintRepetitionsInvalid="])
	except getopt.GetoptError:
		print 'Could not get arguments'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-p', '--toPrintValid'):
			argsdict['toPrintValid'] = True
		elif opt in ('-r', '--toPrintRepetitionsValid'):
			argsdict['toPrintRepetitionsValid'] = True
		elif opt in ('-i', '--toPrintInvalid'):
			argsdict['toPrintInvalid'] = True
		elif opt in ('-d', '--toPrintRepetitionsInvalid'):
			argsdict['toPrintRepetitionsInvalid'] = True 
		else:
			continue
	return dict(argsdict)


def main(argv):
	print """\
	##############################################
	#                 Begin                      #
	##############################################
	"""
	args = {'toPrintValid': False, 'toPrintRepetitionsValid': False,
	'toPrintInvalid': False, 'toPrintRepetitionsInvalid': False}
	args = process_args(argv, args)
	print args
	g = Grammar(cfg_str)
	print "======= Valid sentences: ======"
	g.parse_and_print(valid, args['toPrintValid'], args['toPrintRepetitionsValid'])
	print "======= Invalid sentences: ======"
	g.parse_and_print(invalid, args['toPrintInvalid'], args['toPrintRepetitionsInvalid'])

if __name__ == '__main__':
	main(sys.argv[1:])