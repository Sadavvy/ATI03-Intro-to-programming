import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
import argparse
import wave
from tkinter import TclError

SAMPLES_PER_FRAME = 1024 * 2  # Number of audio samples per frame
AUDIO_FORMAT = pyaudio.paInt16  # Audio format (16-bit integer)
NUM_CHANNELS = 1  # Number of audio channels (mono)
SAMPLE_RATE = 44100  # Sample rate in Hz

def validate_device(device_index, audio_instance):
    """
    Validate the audio input device index.
    
    :param device_index: Index of the audio input device
    :param audio_instance: Instance of the PyAudio class
    :return: True if the device index is valid, False otherwise
    """
    info = audio_instance.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    if device_index < 0 or device_index >= num_devices:
        return False
    return True

def list_devices(audio_instance):
    """
    List available audio input devices.
    
    :param audio_instance: Instance of the PyAudio class
    """
    info = audio_instance.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(num_devices):
        if (audio_instance.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print(f"Audio Input Device Index {i} - {audio_instance.get_device_info_by_host_api_device_index(0, i).get('name')}")

def visualize_audio(device_index, samples_per_frame, audio_format, num_channels, sample_rate, output_file):
    """
    Visualize audio input in real-time using a matplotlib plot and save the audio data to a WAV file.
    
    :param device_index: Index of the audio input device
    :param samples_per_frame: Number of audio samples per frame
    :param audio_format: Audio format (e.g., pyaudio.paInt16)
    :param num_channels: Number of audio channels (e.g., 1 for mono)
    :param sample_rate: Sample rate in Hz
    :param output_file: Path to the output WAV file
    :return: True if visualization and recording are successful, False otherwise
    """
    # Create a matplotlib figure and axes
    fig, ax = plt.subplots(1, figsize=(15, 7))

    # Create a PyAudio instance
    audio = pyaudio.PyAudio()

    try:
        # Open an audio stream
        stream = audio.open(
            input_device_index=device_index,
            format=audio_format,
            channels=num_channels,
            rate=sample_rate,
            input=True,
            output=True,
            frames_per_buffer=samples_per_frame
        )
    except OSError:
        print("Invalid index. Please choose a valid audio input device.")
        return False

    # Open a WAV file for writing
    wav_file = wave.open(output_file, 'wb')
    wav_file.setnchannels(num_channels)
    wav_file.setsampwidth(audio.get_sample_size(audio_format))
    wav_file.setframerate(sample_rate)

    # Generate x-axis values for plotting
    x_values = np.arange(0, 2 * samples_per_frame, 2)
    # Create a line object with black color
    line, = ax.plot(x_values, np.random.rand(samples_per_frame), '-', lw=2, color='black')

    # Customize the plot
    ax.set_title('Real-time Audio Waveform')
    ax.set_xlabel('Samples')
    ax.set_ylabel('Amplitude')
    ax.set_ylim(0, 255)
    ax.set_xlim(0, 2 * samples_per_frame)
    plt.setp(ax, xticks=[0, samples_per_frame, 2 * samples_per_frame], yticks=[0, 128, 255])
    plt.grid(True)

    # Display the plot
    plt.show(block=False)

    print('Audio visualization and recording started')

    # Variables for measuring frame rate
    frame_count = 0
    start_time = time.time()

    while True:
        # Read audio data from the stream
        audio_data = stream.read(samples_per_frame)

        # Write audio data to the WAV file
        wav_file.writeframes(audio_data)

        # Convert audio data to integers and create a numpy array
        data_int = struct.unpack(str(2 * samples_per_frame) + 'B', audio_data)
        data_np = np.array(data_int, dtype='b')[::2] + 128

        # Update the plot data
        line.set_ydata(data_np)

        # Redraw the plot
        try:
            fig.canvas.draw()
            fig.canvas.flush_events()
            frame_count += 1
        except TclError:
            # Calculate and print the average frame rate
            frame_rate = frame_count / (time.time() - start_time)
            print('Audio visualization and recording stopped')
            print('Average frame rate = {:.0f} FPS'.format(frame_rate))
            break

    # Close the WAV file
    wav_file.close()

    # Clean up
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return True

def select_device():
    """
    Prompt the user to select a valid audio input device.
    
    :return: The selected device index
    """
    while True:
        audio_instance = pyaudio.PyAudio()
        list_devices(audio_instance)
        audio_instance.terminate()

        try:
            device_index = int(input("\n\nSelect a valid audio input device by index: "))
            if validate_device(device_index, pyaudio.PyAudio()):
                return device_index
            else:
                print("Invalid index. Please choose a valid audio input device.")
        except ValueError:
            print("Invalid input. Please enter a valid integer index.")

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Real-time Audio Waveform Visualization and Recording')
    parser.add_argument('-i', '--input_device', type=int, default=None,
                        help='Audio input device index (default: None)')
    parser.add_argument('-s', '--samples_per_frame', type=int, default=SAMPLES_PER_FRAME,
                        help='Samples per frame (default: 1024*2)')
    parser.add_argument('-f', '--audio_format', type=int, default=AUDIO_FORMAT,
                        help='Audio format (default: pyaudio.paInt16)')
    parser.add_argument('-c', '--num_channels', type=int, default=NUM_CHANNELS,
                        help='Number of audio channels (default: 1)')
    parser.add_argument('-r', '--sample_rate', type=int, default=SAMPLE_RATE,
                        help='Sample rate (default: 44100)')
    parser.add_argument('-o', '--output_file', type=str, default='output.wav',
                        help='Output WAV file path (default: output.wav)')
    args = parser.parse_args()

    # If no input device is specified or an invalid index is provided, prompt the user to select a device
    if args.input_device is None or not validate_device(args.input_device, pyaudio.PyAudio()):
        device_index = select_device()
    else:
        device_index = args.input_device

    # Start audio visualization and recording
    while True:
        success = visualize_audio(device_index, args.samples_per_frame, args.audio_format, args.num_channels, args.sample_rate, args.output_file)
        if not success:
            device_index = select_device()
        else:
            break
