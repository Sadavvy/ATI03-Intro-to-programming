# my info
Name: Ahmed A H AlSaadawi
pnumber:p419194
course code:IY499
I confirm that this assignment is my own work.Where I have referred to online sources, I have provided comments detailing the reference and included a link to the source.  

# my app title
Real-time Audio Waveform Visualization and Recording
This Python program allows you to visualize audio input in real-time using a matplotlib plot and simultaneously record the audio data to a WAV file. It provides a simple and interactive way to monitor and capture audio signals from various input devices.
Features

Real-time audio waveform visualization using matplotlib
Audio recording and saving to a WAV file
Command-line arguments for customization
Interactive selection of audio input devices
Error handling for invalid device indices

 # Libraries Used

PyAudio: for audio input and output
NumPy: for data manipulation and processing
Matplotlib: for plotting the audio waveform
Wave: for writing audio data to WAV files
ArgParse: for command-line argument parsing


# Installation process

Clone the repository or download the source code files.
Install the required libraries by running the following command:
Copy codepip install pyaudio numpy matplotlib wave argparse

#
Usage

Open a terminal or command prompt and navigate to the directory containing the program files.
Run the program using the following command:
Copy codepython audio_visualizer.py

If no command-line arguments are provided, the program will list the available audio input devices and prompt you to select a device by entering its index.
Optional command-line arguments:

-i or --input_device: Specify the audio input device index (default: None)
-s or --samples_per_frame: Specify the number of audio samples per frame (default: 2048)
-f or --audio_format: Specify the audio format (default: pyaudio.paInt16)
-c or --num_channels: Specify the number of audio channels (default: 1)
-r or --sample_rate: Specify the sample rate in Hz (default: 44100)
-o or --output_file: Specify the path to the output WAV file (default: 'output.wav')


The program will start visualizing the audio waveform in real-time and recording the audio data to the specified output file.
To stop the program, close the matplotlib window or press 'Ctrl+C' in the terminal.

Note: If an invalid audio input device index is provided, either through command-line arguments or during the interactive selection, the program will display an error message and prompt you to select a valid device.
Enjoy exploring and analyzing audio signals with this real-time audio waveform visualization and recording tool!

#source code:https://github.com/Sadavvy/ATI03-Intro-to-programming