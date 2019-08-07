#ifndef ME_SPEC_H
#define ME_SPEC_H
#include "me_util.h"
/*-----------------------------------------------------------*/
/* Specular        */
/*-----------------------------------------------------------*/
color meSpecular (
    uniform string category;
    float Ks;
    color SpecColor;
    float roughness; )
{
 
    extern normal N;
    extern vector L, I;
    extern point P;
    extern color Cl;
    
    
    normal Nf = faceforward( normalize(N), I );
    vector Nn = normalize(N);
    color spec = 0;
            
    
    /* spec =  specular(Nf, -normalize(I), roughness); */
    illuminance( category, P, Nf, PI/2, "lightcache", "refresh" ) 
    { 
        float nonspec = 0;
        lightsource("__nonspecular", nonspec);
        if (nonspec < 1)
            spec += (1-nonspec) * Cl * specularbrdf(normalize(L), Nf, -normalize(I), roughness);
    }
    return Ks * spec * SpecColor;
}

/*-----------------------------------------------------------
 Specularity with close falloff for a wet apearance        
-----------------------------------------------------------*/
color meGlossySpecular (
    uniform string category;
    float Ks;
    float roughness;
    float sharpness;
    color coloration; )
{
    color GlossyColor( uniform string category; normal N; vector V; float roughness, sharpness; )
    {
        color C = 0;
        float w = .18 * (1-sharpness);
        extern point P;
        
        illuminance (P, N, PI/2) 
        {
        /* Must declare extern L & Cl because we're in a function */
        extern vector L;  
        extern color Cl; 
        float nonspec = 0;
        lightsource ("__nonspecular", nonspec);
        if (nonspec < 1) 
        {
            vector H = normalize(normalize(L)+V);
            C += Cl * ( (1-nonspec) * smoothstep (.72-w, .72+w, pow(max(0,N.H), 1/roughness)) );
        }
        }
        return C;
   }
   extern normal N;
   extern vector I;
   normal Ns = meShadingNormal( N );
   color spec = coloration * Ks * GlossyColor( category, Ns, -normalize(I), roughness, sharpness );
   return spec; 
}
#endif            
