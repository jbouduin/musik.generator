
#region command line interface argument related ###############################

def argumentToItem(argument: str) -> str:
    return argument.replace('-', '_')
# end argumentToItem


argumentForce: str = 'force'                   # -f
argumentGenerateOnly: str = 'generate-only'    # -g
argumentOutputDir: str = 'output'              # -o
argumentStandardPitch: str = 'standard-pitch'  # -s
argumentVerbose: str = 'verbose'               # -v
argumentTarget: str = 'target'                 # positional
argumentTargetAll: str = 'all'
argumentTargetLilypond: str = 'lilypond'
argumentTargetMusescore: str = 'musescore'

# endregion
