#ifndef ME_DIFF_H
#define ME_DIFF_H
#include "me_util.h"
/*-----------------------------------------------------------
    meDiffuse
    
    This is some mix of standart Pixar Slim Diffuse function  
    and Stefano Tobacco ST_Diffloat templates  
-----------------------------------------------------------*/
color meDiffuse(
      uniform string category;
      float Kd;
      float atten;
      float from;
      float to;
      color coloration; 
      )
{
  extern normal N;
    extern vector I;
    extern point P;
        
    normal Nf = faceforward( normalize(N), I );
    color diffColor = 0;
    color result = 0;
              
    illuminance ( category, P, Nf, PI/2, "lightcache", "refresh" ) 
    {
        float nondiff = 0;
        lightsource("__nondiffuse", nondiff);
        if (nondiff < 1)
            diffColor += ( 1 - nondiff ) * Cl*(Nf.normalize(L));
    }
    
    
    float hueComp = comp( ctransform( "hsv" , diffColor ) , 0 );
    float satComp = comp( ctransform( "hsv" , diffColor ), 1 );
    float lumiComp = comp( ctransform( "hsv" , diffColor ), 2 ); /*  get value component from HSV color space */
    color hsvDiff = color "hsv" ( hueComp, satComp, ( from + ( to - from ) * pow( lumiComp, atten ) ) );
  
    result = coloration * Kd * hsvDiff;
    return result;
}
/*-----------------------------------------------------------
    meWrappedDiffuse
    
    One shotcoming of the traditional lighting model is:
    diffuse falloff too fast. Wrapped Diffuse Lighting model 
    gave the light the ability 	to reach beyond the 90 degree point 
    on the surface of objects, producing softened 
    light, as if simulating an area light. 
    A few of directional lights is sufficient.
    Here is the float function used to vary a colorSpline 
    according to the wrapped diffuse.'said zj, July 26,2002."

-----------------------------------------------------------*/
color meWrappedDiffuse( 
        uniform string category;
        float Kw;
        float att;
    )
{
    extern vector I;
    extern normal N;
    extern point P;
    
    vector Nn = normalize(N);
    normal Nf = faceforward( normalize(N), I );
    float ang;
    color result = 0;
    
    illuminance( category, P, Nn, PI) 
    {
     extern vector L;
     vector Ln = normalize(L);
     ang = acos(Ln.Nn);
    }
    result = pow(max((1-ang/(PI*Kw)),0),att);
    return result;
}

#endif            
