#ifndef ME_IBI_H
#define ME_IBI_H
#include "me_util.h"
/*-----------------------------------------------------------*/
color meIBI_diff(
    uniform string category;
    float dBlur;
    float Kd;
    normal Ns;
    output varying vector  __L;
    output varying float   __blur; )
{
    extern point P;
    
    color diffuse_color = 0;
    
    __L = Ns;
    __blur = dBlur;
    P = P; /* dirty light cache  , "lightcache", "refresh" */ 
    illuminance ( category, P ) 
    {
        diffuse_color += Cl;
    }     
    return ( diffuse_color * Kd );
}
/*-----------------------------------------------------------*/
color meIBI_spec (
    uniform string category;
    float rBlur;
    float KrMin;
    float KrMax;
    float IOR;
    normal Ns;
    output varying vector  __L;
    output varying float   __blur; 
)
{

    extern vector I;
    extern point P;

    float Kr;
    vector R;
    vector V = normalize (I);  
    
    color specular_color = 0;
    
    if(IOR > 0)
    {
            vector T;
            float Kt;
            float f = max(IOR, 1.0e-4);
             fresnel (V, Ns, (I.Ns < 0) ? 1.0/f : IOR,	Kr, Kt, R, T);
            Kr = mix( KrMin, KrMax, Kr );
    }
    else
    {
            R = reflect(V, Ns);
            Kr = KrMax;
    }
    
    __L = R;
    __blur = rBlur;
    P = P; /* dirty light cache */
    illuminance ( category, P ) /* , "lightcache", "refresh" */
    {
        specular_color += Cl;
    }     
    return ( specular_color * Kr );
}
#endif
