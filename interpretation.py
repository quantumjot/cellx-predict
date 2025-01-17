from typing import Union

import numpy as np
import tensorflow.keras as K
from skimage.util import montage
from vizualisation import to_rgb


def latent_space_traversal(
    decoder: K.models.Model,
    l1: int,
    l2: int,
    l1_values: Union[list, np.array],
    l2_values: Union[list, np.array],
) -> np.array:

    latent_dim = decoder.layers[0].input_shape[-1]

    flat_grid_list = []

    for l1_value in l1_values:
        for l2_value in l2_values:

            latent_vector = np.zeros((latent_dim,))
            latent_vector[l1] = l1_value
            latent_vector[l2] = l2_value

            decoded = decoder.predict(latent_vector)
            decoded = to_rgb(decoded, axis=-1)
            decoded = decoded.astype(np.uint8)

            flat_grid_list.append(decoded)

    flat_grid = np.stack(flat_grid_list, axis=0, dtype=np.uint8)

    output_grid = montage(
        flat_grid,
        grid_shape=(len(l2_values), len(l1_values)),
        multichannel=True,
        fill=[255] * 3,
        padding_width=3,
    )

    return output_grid
