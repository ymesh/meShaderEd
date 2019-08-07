#ifndef _H_pxslUtil
#define _H_pxslUtil

/* utility functions derived from, Apodaca/Gritze: 
       "Advanced RenderMan: Creating CGI for Motion Pictures"
       by Tony Apodaca and Larry Gritz cc 1999.
 
   $Revision: #3 $
*/


#include "filterwidth.h"
#include "noises.h"

/* pxslFilterWidth - a filtersize estimator based on the vectors
    dpu, dpv as passed through the standard slim manifold interface. */
#define pxslLooseFilterWidth(dpu,dpv) \
    max( length(dpu+dpv), MINFILTWIDTH )

#define pxslTightFilterWidth(dpu,dpv) \
    max( length(dpu^dpv), MINFILTWIDTH )

#if SLIM_SHADERTYPEID == SLIM_TYPEID_displacement
#define pxslFilterWidth(a, b) pxslLooseFilterWidth(a,b)
#else
#define pxslFilterWidth(a, b) pxslTightFilterWidth(a,b)
#endif

#define pxslFilteredFNoise(p, dpu, dpv) \
    (fadeout(float noise(p), .5, 1, pxslFilterWidth(dpu, dpv)))

#define pxslFilteredCNoise(p, dpu, dpv) \
    (fadeout(color noise(p), color(.5), 1, pxslFilterWidth(dpu, dpv)))

#define pxslFilteredVNoise(p, dpu, dpv) \
    (vector vsnoise(p)*(1-smoothstep (0.2,0.75,pxslFilterWidth(dpu, dpv))))


/* bimix: bilinear interpolation of 4 values. */
#define pxslBimix(c0,c1,c2,c3,x,y) \
    mix (mix (c2,c0,y), mix (c3,c1,y), x)

color pxslVaryColor(color avgcolor; float variance; float seed;)
{
    color hsl = ctransform("hsl", avgcolor);
    float h, s, l;
    h = comp(hsl, 0); s = comp(hsl, 1); l = comp(hsl, 2);
    h += variance * (cellnoise(seed+3)-0.5);
    s += variance * (cellnoise(seed-14)-0.5);
    l += variance * (cellnoise(seed+37)-0.5);
    hsl = color(mod(h,1), clamp(s, 0, 1), clamp(l, 0, 1));
    return ctransform("hsl", "rgb", hsl);
}

color pxslCmix(color a; color b; color mixture)
{
    return (1 - mixture) * a +  mixture * b;
}

vector pxslEnvDirCorrect(uniform string corr; vector R)
{
    vector result;
    if( corr == "none" )
    {
    result = R;
    }
    else
    if(corr == "XtoY")
    {
    result = vector(-ycomp(R), xcomp(R), zcomp(R));
    }
    else
    if(corr == "YtoX")
    {
    result = vector(ycomp(R), -xcomp(R), zcomp(R));
    }
    else
    if(corr == "XtoZ")
    {
    result = vector(-zcomp(R), ycomp(R), xcomp(R));
    }
    else
    if(corr == "ZtoX")
    {
    result = vector(zcomp(R), ycomp(R), -xcomp(R));
    }
    else
    if(corr == "YtoZ")
    {
        result = vector(xcomp(R), -zcomp(R), ycomp(R));
    }
    else
    if(corr == "ZtoY") 
    {
        result = vector(xcomp(R), zcomp(R), -ycomp(R));
    }
    else
    result = R;
    return result;
}

float pxslLuminance(color c)
{
    return .3 * comp(c, 0) + 
    .59 * comp(c, 1) + 
    .11 * comp(c, 2);
}

#endif
