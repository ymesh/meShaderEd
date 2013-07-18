#ifndef _dl_utils_filteredpulsetrain_h
#define _dl_utils_filteredpulsetrain_h


/* Taken from ARMAN and improved. */
float filteredpulsetrain (float edge, period, x, dx)
{
	/* First, normalize so period == 1 and our domain of interest is > 0 */
    float w = dx/period;
    float x0 = x/period - w/2;
    float x1 = x0+w;
    float nedge = edge / period;

	/* Definite integral of normalized pulsetrain from 0 to t */
    float integral (float t) { 
        extern float nedge;
        return ((1-nedge)*floor(t) + max(0,t-floor(t)-nedge));
    }

	float result;
	if( x0 == x1 )
	{
		/* Trap the unfiltered case so it doesn't return 0 (when dx << x). */
		result = (x0 - floor(x0) < nedge) ? 0 : 1;
	}
	else
	{
    	result = (integral(x1) - integral(x0)) / w;

		/*
			The above integral is subject to its own aliasing as we go beyond
			where the pattern should be extinct. We try to avoid that by
			switching to a constant value.
		*/
		float extinct = smoothstep( 0.4, 0.5, w );
		result = result + extinct * (1 - nedge - result);
	}

	return result;
}


#endif