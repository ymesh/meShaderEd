#ifndef _H_PxslRemap
#define _H_PxslRemap

float
pxslFloatBias( float bias; float t; )
{
    float tb = t / ((1/max(bias,1e-4) - 2) * (1 - t) + 1);
    return tb;
}

color
pxslColorBias( color bias; color c; )
{
    color cb, w = color(1,1,1);
    cb = c / ((w/max(bias,color(1e-4)) - 2) * (w - c) + w);
    return cb;
}

float
pxslFloatGain( float gg; float t; )
{
    float tg, gain;
    gain = clamp(gg, .0001, .9999);
    if( t < .5 )
    {
	tg = t / ((1/gain - 2) * (1 - 2*t) + 1);
    }
    else
    {
	tg = ((1/gain - 2) * (1 - 2*t) - t) /
		((1/gain - 2) * (1 - 2*t) - 1);
    }
    return tg;
}

color
pxslColorGain( color gain; color c; )
{
    color cb;
    setcomp(cb, 0, pxslFloatGain( comp(gain,0), comp(c,0) ) );
    setcomp(cb, 1, pxslFloatGain( comp(gain,1), comp(c,1) ) );
    setcomp(cb, 2, pxslFloatGain( comp(gain,2), comp(c,2) ) );
    return cb;
}

#endif
