# A lilypond and musescore file generator

## Short history
As I needed a lot of Images and mp3 files for my [Anki](https://apps.ankiweb.net/) deck I started searching for apps that could generate them.

### Prerequisites:
* the images are cropped to what is to be displayed
* the images have a transparent background (usefull in dark-mode)
* the mp3 files use a standard pitch of 443Hz

### Result of my search
I ended up with [lilypond](https://lilypond.org) for generating images like this:
![image](./sample_output/kurzer-tonleiter-in-a-dur.cropped.png).

Lilypond can also export midi-files, but those are not supported by Anki and lilypond uses the 440Hz standard pitch. Further research ended at [MuseScore](https://musescore.org), which offers a graphical interface and is capable of generating mp3-files out of your score, using whatever standard pitch you want to use.
The mp3 file corresponding to the image above can be found [here](./sample_output/kurzer-tonleiter-in-a-dur.cropped.mp3).

As creating the sources for both programs would take me ages, I decided to build some small tool that does the basic work for me. And here it is.
I used python, although I do not have a lot of experience with it.

### Caveat
As I started learning to play the violin, the generated files are restricted to the ambitus of the violin (1st position)

# The generator
## Requirements
* Python (I currently use 3.8.5).
* No special libraries are required.

## Run
* clone the repository
* rename config.template.json to config.json (this is the default used if you do not provide any parameter)
* run `generate.py`

```sh
usage: generate.py [-h] [--config CONFIG] [--generate-only] [--output OUTPUT] [--force] [--verbose] {all,musescore,lilypond}

Generate and process lilypond and musescore files.

positional arguments:
  {all,musescore,lilypond}
                        Type of files to generate

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        The name of the configuration file
  --generate-only, -g   Do not process generated files
  --output OUTPUT, -o OUTPUT
                        The output directory
  --force, -f           Force creation of the output directory if it does not exist
  --verbose, -v         Verbose
```


## Todo's
- :white_check_mark: add CLI parameter outputdir to config.json and merge CLI args with config
- :white_check_mark: output subdir's should go into config.json + CLI args
- :white_check_mark: add a parameter for the standardpitch, default = 443
- :white_check_mark: add a parameter to skip files that already exist
- :white_check_mark: delete .pdf and .cropped.pdf lilypond generates as intermediate steps
- :white_check_mark: parameterized (default: false) delete of ly and mscx files after processing them
- :white_check_mark: add selection noten, tonleiter, intervalle
- :white_check_mark: Split helper into a musical helper and a text helper
- :white_check_mark: get name of template file from config
- :white_check_mark: get template file name from config

