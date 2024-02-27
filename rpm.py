import argparse
import librosa
import numpy as np
from scipy.signal import find_peaks

def mix_down_to_mono(audio_data, channel_mode='mix'):
    """Mix down stereo audio data to mono based on the selected channel mode."""
    if channel_mode == 'left':
        return audio_data[0]  # Left channel only
    elif channel_mode == 'right':
        return audio_data[1]  # Right channel only
    elif channel_mode == 'mix':
        return np.mean(audio_data, axis=0)  # Mix both channels
    else:
        raise ValueError("Invalid channel mode. Choose 'left', 'right', or 'mix'.")

def find_highest_peaks(audio_mono, sr, num_peaks, min_distance_samples):
    """Find the specified number of highest peaks in the mono audio signal, considering a minimum distance between peaks."""
    peaks, properties = find_peaks(audio_mono, height=0, distance=min_distance_samples)
    if len(peaks) == 0:
        print("No peaks found.")
        return [], []
    
    highest_peaks_indices = np.argsort(properties['peak_heights'])[-num_peaks:][::-1]
    highest_peaks = [(peaks[i], properties['peak_heights'][i]) for i in highest_peaks_indices]
    highest_peaks_sorted = sorted(highest_peaks, key=lambda x: x[0])
    peak_times = np.array([peak[0] for peak in highest_peaks_sorted]) / sr
    peak_heights = np.array([peak[1] for peak in highest_peaks_sorted])
    return peak_times, peak_heights

def calculate_intervals(peak_times):
    """Calculate time intervals between peaks."""
    return np.diff(peak_times)

def calculate_intervals_stats(intervals):
    """Calculate statistics for time intervals and convert them to RPM values."""
    if intervals.size == 0:
        return None
    rpm_values = 60 / intervals
    stats = {
        'Min': (np.min(intervals), np.min(rpm_values)),
        'Max': (np.max(intervals), np.max(rpm_values)),
        'Average': (np.mean(intervals), np.mean(rpm_values)),
        'Std Dev': (np.std(intervals), np.std(rpm_values))
    }
    return stats

def print_stats(stats, channel_mode, num_peaks):
    """Print statistics for the analysis."""
    max_decimal_places = max(max(len(str(value).split('.')[1]) if '.' in str(value) else 0 for value in pair) for pair in stats.values())
    
    print()
    print("Channel mode: " + channel_mode)
    print(f"Revolutions: {num_peaks - 1}")
    print()
    print(f"{'Statistic':<20} {'Time Intervals (s)':<35} {'RPM Values':<35}")
    print("-" * 90)
    
    for stat, (interval, rpm) in stats.items():
        interval_str = f"{interval:.{max_decimal_places}f}"
        rpm_str = f"{rpm:.{max_decimal_places}f}"
        print(f"{stat:<20} {interval_str:<35} {rpm_str:<35}")

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Turntable RPM Analysis")
    parser.add_argument("filename", type=str, help="Path to the audio file")
    parser.add_argument("num_peaks", type=int, help="Number of highest peaks to find")
    parser.add_argument("min_distance_ms", type=int, help="Minimum distance between peaks in milliseconds")
    parser.add_argument("--channel_mode", type=str, choices=['left', 'right', 'mix'], default='mix', help="Channel mode for analysis ('left', 'right', 'mix')")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    audio, sr = librosa.load(args.filename, sr=None, mono=False)  # Load the audio file
    audio_mono = mix_down_to_mono(audio, args.channel_mode)  # Process audio based on channel mode
    min_distance_samples = int((args.min_distance_ms / 1000.0) * sr)
    peak_times, peak_heights = find_highest_peaks(audio_mono, sr, args.num_peaks, min_distance_samples)
    
    if len(peak_times) == args.num_peaks:
        intervals = calculate_intervals(peak_times)
        stats = calculate_intervals_stats(intervals)
        if stats:
            print_stats(stats, args.channel_mode, args.num_peaks)
        else:
            print("Could not calculate statistics.")
    else:
        print(f"Expected {args.num_peaks} peaks, but found {len(peak_times)}. Unable to calculate statistics.")

if __name__ == "__main__":
    main()
