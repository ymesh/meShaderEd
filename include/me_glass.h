#ifndef ME_GLASS_H
#define ME_GLASS_H
#include "me_util.h"
/*-----------------------------------------------------------*/
color meGlass(
        float ior; /* = 1.5; */
        uniform float twosided; /*  = 1; */
        uniform string traceset; /* = ""; */
        uniform float maxdist; /* = -1; */
        uniform float russian_roulette; /* = 2; */       
        uniform float krefl; /* = 1; */
        color crefl; /* = 1; */
        uniform float reflsamps; /* = 1; */
        uniform float reflblur; /* = 0; */
        uniform float reflection_depth; /* = 2; */
        uniform float krefr; /* = 1; */
        color crefr; /* = 1; */
        uniform float refrsamps; /* = 1; */
        uniform float refrblur; /* = 0; */
        uniform float refraction_depth; /* = 2; */ 
    )
{
    extern normal N;
    extern vector I;
    extern point P;
    
    vector In = normalize(I);
    vector V = -In;
    vector reflDir, refrDir;
    normal Nn = normalize(N);
    normal Ns = Nn; 
    
    float front = (In.N <= 0) ? 1 : 0;
    float kt, kr;
    uniform float sides = 2;
    uniform float raydepth, refrsamples = refrsamps, xsamples;
    uniform float reflsamples = reflsamps;
    color hci, ctmp;
    string ray_label = "";
    
    float rreflblur = reflblur;
    float rrefrblur = refrblur;
    color spec_res = 0;
    color c_specular = 0;
    color c_incandescence = 0;
    color c_reflection = 0;
    color c_refraction = 0;
    
    color refl_c = crefl;
    color refr_c = crefr;
    
    float rand = 0;
    hci = 0;

    color cresult = 0;

    attribute("Sides", sides);
    rayinfo("label", ray_label);
    rayinfo("depth", raydepth);
    
    if (sides == 2 || raydepth > 0)
#ifdef DELIGHT
        Ns = faceforward(Nn, I);
#else    
        Ns = faceforward(Nn, I, Nn);
#endif

    if( ior != 0 )
    { /* relative index of refraction */
        float eta = (front == 1) ? (1 / ior) : ior; 
        fresnel(In, Ns, eta, kr, kt, reflDir, refrDir);
        kt = krefr * (1-kr);
        kr *= krefl;
    }
    else
    {
        float eta = (front == 1) ? 1 / 1.5 : 1.5;
        reflDir = reflect(In, Ns);
        refrDir = refract (In, Ns, eta);
        kr = krefl;
        kt = krefr;
    }
    
    if( raydepth >= reflection_depth )
        kr = 0;
    else if (raydepth >= russian_roulette)
    {
        rand = random();
        if (rand >= kt)
            kt = 0;
        else
            kr = 0;
    }
    
    if( raydepth >= refraction_depth )
            kt = 0;
    
    if ( raydepth > 0 )
    {
        refrsamples = round (refrsamples*0.25);
        reflsamples = round (reflsamples*0.25);
        if ( refrsamples < 1 )
            refrsamples = 1;
        if ( reflsamples < 1 )
            reflsamples = 1;            
    }
    else if( raydepth == 0 && twosided == 0 && front == 0 )
    {
        /*
        kr = 0;
        kt = 0;
        */
    }
    
    xsamples = reflsamples;
    
    if( raydepth > 1 )
    {
        if( ray_label == "b_refr" || ray_label == "b_refl" )
        {
            rreflblur = 0;
            rrefrblur = 0;
        }
    }
         
    if( kr > 0 && xsamples > 0 )
    {
        ctmp = 0;
        if( rreflblur > 0 )
        {
            gather( "illuminance", P, reflDir, rreflblur*radians(5), 
                xsamples,
                "label", "b_refl",
                "subset", traceset,
                "maxdist", maxdist,
#ifdef DELIGHT
                "surface:Ci", hci
#else        
                "volume:Ci", hci
#endif   
            )
            {
                ctmp += hci;
            }
            else
            {
                illuminance( "environment", P+vector(0), Ns, 1.57, 
                    "send:light:__coneaxis", reflDir)
                {
                    ctmp += Cl;
                }
            }
        }
        else
        {
            gather( "illuminance", P, reflDir, 0, 
                xsamples,
                "label", "reflection",
                "subset", traceset,
                "maxdist", maxdist,
#ifdef DELIGHT
                "surface:Ci", hci
#else        
                "volume:Ci", hci
#endif      
            )
            {
                ctmp += hci;
            }
            else
            {
                illuminance( "environment", P+vector(0), Ns, 1.57, 
                    "send:light:__coneaxis", reflDir)
                {
                        ctmp += Cl;
                }
            }       
        }
        c_reflection = kr * crefl * ctmp/xsamples; 
        /* c_reflection = kr * refl_c * ctmp/xsamples; */
        cresult += c_reflection;
    }
    
    /* xsamples = pxslGetRaySamples(refrsamples); */
    xsamples =refrsamples;
    
    if( kt > 0 && xsamples > 0)
    {
        ctmp = 0;
        if( rrefrblur > 0 )
        {
            gather( "illuminance", P, refrDir, rrefrblur*radians(5), 
                xsamples,
             
                "label", "b_refr",
                "subset", traceset,
                "maxdist", maxdist,
#ifdef DELIGHT
                "surface:Ci", hci
#else        
                "volume:Ci", hci
#endif        
            )
            {
                ctmp += hci;
            }
            else
            {
                illuminance( "environment", P+vector(0), Ns, 1.57,
                    "send:light:__coneaxis", refrDir)
                {
                        ctmp += Cl;
                }
            }
        }
        else
        {
            gather( "illuminance", P, refrDir, 0, 
                xsamples,
                
                "label", "refraction",
                "subset", traceset,
                "maxdist", maxdist,
#ifdef DELIGHT
                "surface:Ci", hci
#else        
                "volume:Ci", hci
#endif         
            )
            {
                ctmp += hci;
            }
            else
            {
                illuminance( "environment", P+vector(0), Ns, 1.57,
                    "send:light:__coneaxis", refrDir )
                {
                        ctmp += Cl;
                }
            }       
        }
        c_refraction = kt * crefr * ctmp/xsamples; 
        /* c_refraction = kt * refr_c * ctmp/xsamples; */
        cresult += c_refraction;
    }
    return cresult;
}
#endif

