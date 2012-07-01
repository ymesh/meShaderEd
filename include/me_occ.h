#ifndef ME_OCC_H
#define ME_OCC_H
#include "me_util.h"
/*-----------------------------------------------------------*
  Occlusion with most availible parameters
 *-----------------------------------------------------------*/
float meOcclusion(
  normal Nss;
  uniform float Adaptive; 
  uniform float MaxSamples; 
  uniform float MinSamples; 
  uniform float MaxDist;
  
  uniform vector SkyAxis; /* 3Delight: indicates the direction of the light 
  													casting hemisphere. */
  
  uniform float ConeAngle;
  uniform float SampleBase;
  uniform float Bias;
  
  uniform string HitMode; /* "default" "primitive" "shader" */
  uniform string HitSides; /* "both" "front" "back" */

  uniform float MaxVar;
  uniform float MaxError;
  uniform float MaxPixelDist;

  uniform string Distribution; /* "cosine" "uniform" */
  uniform float FalloffMode; /* 0 = "exp(-falloff*dist)" 
  															1 = "(1 - dist/maxdist)^falloff" */
  uniform float FalloffValue;
  
  uniform string EnvMap;
  uniform string EnvSpace;
  uniform float BrtWarp; 

  uniform string coordsys;
  uniform string subset;
  uniform string label;
  
  uniform float pointbased;
  uniform string PtcFile;
  uniform float MaxSolidAngle;
  uniform float pclamp;
  
  output varying color env_color;
  output varying vector  bent_dir;
)  
{
  
  extern point P;

  float result = 0;
#ifdef AIR  
   color occ = occlusion( P  
              ,Nss 
              ,radians( ConeAngle )
              ,bent_dir
              ,"samples",       MaxSamples
              /* ,"blur", mapblur */
              ,"bias",          Bias
              ,"label",         label
              ,"subset",        subset
              ,"maxdist",       MaxDist
              ,"maxerror",      MaxError 
              ,"maxpixeldist",  MaxPixelDist );
              result = comp( occ, 0 ); 
#else                           
   #ifdef PIXIE
   float occ = occlusion( P  
              ,Nss            
              ,MaxSamples
              ,"irradiance",    env_color /* The irradiance amount (output)  */
              /*,"minR",          MaxPixelDist  uniform float minR	 The closest distance between samples. */
              /*,"maxR",          MaxPixelDist uniform float maxR	The maximum distance between samples. */
              ,"bias",          Bias
              ,"maxdist",       MaxDist );
   #else
   float occ = occlusion( P  
              ,Nss            
              ,MaxSamples
              ,"adaptive",      Adaptive
              ,"minsamples",    MinSamples
              ,"maxdist",       MaxDist
  #ifdef DELIGHT             
              ,"axis",          SkyAxis
  #endif              
              ,"coneangle",     radians( ConeAngle )
              ,"samplebase",    SampleBase
              ,"bias",          Bias
              ,"hitmode",       HitMode
              ,"hitsides",      HitSides
              ,"maxvariation",  MaxVar
  #ifndef DELIGHT              
              ,"maxerror",      MaxError
              ,"maxpixeldist",  MaxPixelDist
              ,"brightnesswarp",  BrtWarp
  #endif               
              ,"distribution",  Distribution
              ,"falloffmode",   FalloffMode
              ,"falloff",       FalloffValue
              
              ,"environmentmap",  EnvMap
              ,"environmentspace",EnvSpace
              
              ,"coordsystem",   coordsys
              ,"subset",        subset
              ,"label",         label

              ,"pointbased",    pointbased
              ,"filename",      PtcFile
              ,"maxsolidangle", MaxSolidAngle
              ,"clamp",         pclamp
              
              ,"environmentcolor",  env_color
              ,"environmentdir",    bent_dir );
              result = occ;  
  #endif /* PIXIE */             
#endif  /* AIR */           
  
  return result;
}
#endif