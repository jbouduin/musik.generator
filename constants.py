
def argumentToItem(argument: str) -> str:
    return argument.replace('-', '_')
# end argumentToItem

argumentForce: str = 'force'                        # -f
argumentGenerateOnly: str = 'generate-only'         # -g
# TODO argumentKeepIntermediate: str = 'keep-intermediate' # -k
# TODO argumentLanguage: str = 'language'                  # -l
argumentOutputDir: str = 'output'                   # -o
argumentPurge: str = 'purge'                        # -p
argumentRegenerate: str = 'regenerate'              # -r
argumentStandardPitch: str = 'standard-pitch'       # -s
argumentTarget: str = 'target'                      # positional
argumentVerbose: str = 'verbose'                    # -v

# possible values for Target parameter
argumentTargetAll: str = 'all'
argumentTargetLilypond: str = 'lilypond'
argumentTargetMusescore: str = 'musescore'

# possible values ofr Target language
argumentLanguageDe: str = 'de'
argumentLanguageEn: str = 'en'

# result list keys
keyLilipond: str = 'Lilypond'
keyMusescore: str = 'Musescore'
keySkipped: str = 'Skipped'
