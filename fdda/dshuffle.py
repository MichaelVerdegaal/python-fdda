import numpy as np


def dominant_shuffle(
    signal: np.ndarray,
    rate: int = 4,
    clip_min: float | int | None = None,
    clip_max: float | int | None = None,
    offset: float = 0.0,
) -> np.ndarray:
    """
    Apply dominant frequency shuffling to the input signal.

    Args:
        signal: A numpy array representing the time series signal.
                Shape can be (time_steps,) for a single feature or
                (time_steps, features) for multiple features.
        rate: Number of top dominant frequencies to shuffle.
        clip_min: Minimum value for clipping the output signal.
        clip_max: Maximum value for clipping the output signal.
        offset: A float value to offset the signal after augmentation.

    Returns:
        A numpy array of the augmented signal, same shape as the input.
    """
    original_shape = signal.shape
    if signal.ndim == 1:
        signal = signal.reshape(-1, 1)

    time_steps, features = signal.shape

    # Perform rfft
    signal_f = np.fft.rfft(signal, axis=0)

    # Identify top-k dominant frequencies
    magnitude = np.abs(signal_f[1:])
    topk_indices = np.argsort(magnitude, axis=0)[-int(rate) :, :] + 1

    # Shuffle dominant frequencies for each feature
    new_signal_f = signal_f.copy()
    for i in range(features):
        for j in range(topk_indices.shape[0]):
            idx = topk_indices[j, i]
            random_idx = np.random.choice(topk_indices[:, i])
            new_signal_f[idx, i] = signal_f[random_idx, i]

    # Convert back to time domain
    augmented_signal = np.fft.irfft(new_signal_f, n=time_steps, axis=0)

    # Apply offset
    augmented_signal += offset

    # Apply clipping if specified
    if clip_min is not None or clip_max is not None:
        augmented_signal = np.clip(augmented_signal, clip_min, clip_max)

    # Restore original shape
    if len(original_shape) == 1:
        augmented_signal = augmented_signal.flatten()

    return augmented_signal
