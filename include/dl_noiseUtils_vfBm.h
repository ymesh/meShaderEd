#ifndef _dl_noiseUtils_vfBm_h
#define _dl_noiseUtils_vfBm_h
#define vsnoise(p) (2 * (vector noise(p)) - 1)


/* A vector-valued fBm. */
vector vfBm( point p; uniform float octaves[2], lacunarity, ratio;
	uniform float i_ripples[3] )
{
	varying vector sum = 0;
	uniform float i = 0;
	uniform float amp = 1;

	point pp = p * point(i_ripples[0], i_ripples[1], i_ripples[2]) / 2;

	float pixel_size = sqrt( area(pp) );
	float nyquist = 2 * pixel_size;
	float pixel = 1.0;

	while( (i<octaves[1] && pixel>pixel_size) || i<octaves[0] )
	{
		sum += amp * vsnoise( pp );
		amp *= ratio;
		pp *= lacunarity;

		i += 1.0;
		pixel /= lacunarity;
	}

	if( pixel>pixel_size && i<=octaves[1])
	{
		float weight = clamp(pixel/pixel_size - 1, 0, 1);
		sum += weight * amp * vsnoise(pp);
	}

	return sum;
}


#endif