# Turntable RPM Analysis

## Overview
This Python script provides an accurate way to analyze the revolutions per minute (RPM) of a turntable using audio recordings. It's designed for audiophiles, turntable manufacturers, and hobbyists interested in measuring and analyzing the performance of their turntables with high precision.

## Features
- **Channel Selection**: Choose between left, right, or mixed audio channels for analysis.
- **Peak Detection**: Automatically detects the highest peaks in the audio signal to determine the time intervals between successive revolutions.
- **RPM Calculation**: Calculates the RPM based on the time intervals between peaks.
- **Statistical Analysis**: Provides minimum, maximum, average, and standard deviation for both time intervals and RPM values.

## Requirements
- Python 3
- Librosa
- NumPy
- SciPy

## Installation
1. Ensure Python 3 is installed on your system.
2. Install the required Python libraries using pip:

```bash
pip install librosa numpy scipy
```

## Usage
1. Directly record the output of your turntable with the stylus looping in a a dead-end groove (i.e. the end of the LP side) in stereo with a sound card (line input).
2. Save the audio file in a format supported by Librosa (e.g., WAV).
3. Update the `filename` variable in the script with the path to your audio file.
4. Update the `num_peaks` variable to indicated the number of clicks recorded in your audio file.
5. Update the `min_distance` variable to indicate mininum time in milliseconds expected between clicks (i.e. 1700 for 33 1/3 RPM,  1200 for 45 RPM)
6. Update the `channel_mode` mode variable if required. This defaults to 'left', which uses the left channel.  If the left channel cannot be analyzed, try the 'right', followed by 'mix'.
7. Run the script:

```bash
python3 rpm.py
```

## How It Works

A dead-end groove on an LP normally contains a prominent "click" or "pop" where the groove enters the dead-end groove. A well defined click is heard each rotation as the stylus passes over the entry groove. This script precisely measures the time between each click to
derive the precise RPM that the turntable platter is rotating at. A sound card must be used to capture a WAV file for the rpm.py script to post-process. It does not currently have real time analysis. No special LP is needed for this test, as all LPs contain
at least one dead-end groove at the end of a side. Some turntables auto-stop at the end of the LP side not allowing for these clicks to be recorded. In that case, an LP with a dead-end groove prior to the LP run out groove must be used. An example of that
would be the CBS STR-100 test record, where some tracks (bands) end with a dead-end groove to prevent the stylus from advancing to the next test track.  This script was tested specifically using the CBS STR-100 (issue 3) test LP.  After testing several
LP dead-end grooves, it was determined that the CBS STR-100 produced clean clicks that were more easily detected.  Not all dead-end grooves produce a sufficiently defined click that rises well above the surface noise of the LP.  This is why two parameters of
the script include the number of expected clicks (num_peaks) and a minimum expected distance between those clicks (min_distance).  This is to give the script enough of a hint to easily identify the target clicks.  If it cannot, then it will display a message.
It is also possible that some stylus profiles (ex. conical, elliptical),  phono preamps with limited headroom and/or certain LPs might not produce a well defined click peak that can be accurately analyzed. Another advantage of using the CBS STR-100 LP is that
the dead-end groove chosen can normally be closer to the null point of the stylus, depending on your particular cartridge alignment. This results in a click with less distortion components.  

You can use any bitrate and sampling rate.  You must record in 2 channel stereo mode.  The script currently expects stereo, because it provides more flexibility for analysis. Using a higher sampling rate increases the precision of the calculations.
For instance a sample rate of 48Khz results in a resolution of 0.0000052083 seconds per sample.  192Khz is 0.000001302075 seconds per sample. This results in a very precise timing of RPM, far beyond any other commonly available method. You must make
a recording via direct sound card connection (no microphones), as a high resolution capture is required.

The other variable is 'channel_mode' which can select the left, right or stereo (mix) channel(s) for analysis.  In testing, the 'left' channel normally produces the best result from a click. If this doesn't work, the 'right' channel can be used. If
that doesn't work, 'mix' can be used. Mix mixes the two channels into mono (in phase). This aggregation might be needed to get analysis working, but it might be slightly less accurate than using a single channel. In the event that none of these methods work,
it means that your equipment or test LP isn't providing a clean enough peak for the script to detect precise timing.

While not required, we recommend normalizing the WAV file to 0 dB and removing DC offset, using software such as Audacity. Normalizing in Audacity has the benefit in that you can clearly visualize the clicks and the noise floor within Audacity to make sure you have captured
something usable. We recommend saving the file with a name which indicates the number of clicks included, so that you do not have to remember or count them when you run the script, remembering that you must specify the `num_peaks` value in the script.
You should also include the speed you used (33 or 45) as well, since the `min_distance` must be specified according to the usage.

The longer your recorded sample, the more accuracy you will have regarding average speed over time, as well as variance. For the most part, 1 minute of sampling should be enough and is a good sample for comparison. (1 minute of sampling,  33 1/3 RPM  = ~ 35 clicks & 45 RPM = ~ 45 clicks)

The script calculates the minimum, maximum, average and standard deviation of each rotation in seconds, as well as in RPM. Because this calculation is made at
the same azimuth point each revolution, it cannot calculate flutter, which would rely on a continuous measurement of turntable speed. Rather these measurements are a precise averaging of speed over 1 revolution which would give an idea of wow. Ultimately, it should still
serve as a precise way to set turntable speed. It might be possible to take measurements by changing the record's azimuth orientation on the the platter and making a collection of measurements at a variation of angles to expose any minute flutter issues, which might show
up as a variance at a specific azimuth that is far different than the others. Another advantage of this method of measuring RPM is that it includes stylus friction normally incurred while playing an LP, not encountered when using strobe discs. 

Output will be directed to standard out.  Here is an example:

```
python3 rpm.py

Channel mode: mix
Revolutions: 44

Statistic            Time Intervals (s)                  RPM Values
------------------------------------------------------------------------------------------
Min                  1.3332031250000042633               44.9982422561619088697
Max                  1.3333854166666654351               45.0043949604452109270
Average              1.3332941524621211293               45.0013224919138608016
Std Dev              0.0000624258619264826               0.0021069934632214045
```
 



## Contributing
Contributions to improve the script are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

