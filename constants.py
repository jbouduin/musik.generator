
#region command line interface argument related ###############################

def argumentToItem(argument: str) -> str:
    return argument.replace('-', '_')
# end argumentToItem

# TODO make a set of long arguments and short arguments, to make sure that we do not have conflicting values
argumentForce: str = 'force'
argumentGenerateOnly: str = 'generate-only'
argumentOutputDir: str = 'output'
argumentStandardPitch: str = 'standard-pitch'
argumentTarget: str = 'target'
argumentTargetAll: str = 'all'
argumentTargetLilypond: str = 'lilypond'
argumentTargetMusescore: str = 'musescore'
argumentVerbose: str = 'verbose'

#endregion