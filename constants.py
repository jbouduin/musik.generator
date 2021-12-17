
#region command line interface argument related ###############################

def argumentToItem(argument: str) -> str:
    return argument.replace('-', '_')
# end argumentToItem


argumentForce: str = 'force'
argumentGenerateOnly: str = 'generate-only'
argumentOutputDir: str = 'output'
argumentTarget: str = 'target'
argumentTargetAll: str = 'all'
argumentTargetLilypond: str = 'lilypond'
argumentTargetMusescore: str = 'musescore'
argumentVerbose: str = 'verbose'

#endregion