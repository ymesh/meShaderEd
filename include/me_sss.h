#ifndef ME_SSS_H
#define ME_SSS_H
#include "me_util.h"
/*-----------------------------------------------------------*/
//  A SubSurface Scattering template based on depth map data.
//  Based on ZJ translucence shader.       
/*-----------------------------------------------------------*/
color meSSS_DM_ZJ( 	
  uniform string category; /* subsurf */
  uniform string coord;
  float Ksss;
	float depth; /* = 0.1  */
	uniform float eta; /* = 0.5  */
	uniform float sigma; /* = 0.5   Absorbing Coefficient */
	uniform float ior; /* = 1.333  */
	color tint; /* = color(1)  */
)	
{
	vector efresnel(vector II; normal NN; float eta; output float Kr, Kt;) 
	{
    vector R, T;
    fresnel(II, NN, eta, Kr, Kt, R, T);
    Kr = smoothstep(0.,0.5, Kr);
    Kt = 1. - Kr;
    return normalize(T);
  }
      
  extern normal N;
  extern vector I;
  extern point P;
  normal Nn = normalize(N);
  vector Vn  = normalize(I);
       
  float Kr, Kt;
  vector T = normalize( efresnel(Vn, Nn, 1/ior, Kr, Kt) );
  point Q = P + T * depth;
  float idist[9] = { -1, -.5, -.3, -.1, 0, .5, .3, .5, 1 };
  float jdist[9] = { -1, -.5, -.3, -.1, 0, .5, .3, .5, 1 };
    
  point Psample, NDCP, cameraP, Pin;
  uniform matrix shadNDCSpace, shadcamSpace, shadinvSpace;
  float i, j, realsamples = 0, dist = 0, dot, NDCs, NDCt, Ddata;
  
  vector orient = vector "world" (0,0,1);
  if ( coord != "" )
    orient = normalize( vtransform( coord,"current",vector(0,0,-1) ) );
  
  vector up = vector "world" (0,1,0);
  if ( abs(orient.up) > 0.9 )
    up = vector "world" (1,0,0);
  vector base1 = normalize( orient^up );
  vector base2 = normalize( orient^base1 );
        
  color c = 0, Cdata = 1;
  uniform string handle = "subsurf";
  if ( category != "" )
    handle = category;
  
  P = P;
          
  illuminance( handle, Q )
  {
    extern vector L;
    extern color Cl;
    vector Ln = normalize( L );
          
    dot = Ln.orient;
    uniform string shdname, imgname;
    
    if ( lightsource("__shdname", shdname) != 0 && shdname != "" )
    {
      textureinfo( shdname, "projectionmatrix", shadNDCSpace );
      textureinfo( shdname, "viewingmatrix", shadcamSpace );
      shadinvSpace = 1 / shadcamSpace;
              
      for( i = 0 ; i <= 8 ; i= i + 1 )
      {
        for( j = 0 ; j <= 8 ; j = j + 1 )
        {
          Psample = Q + (idist[i] + 0.5*(random()-0.5)) * eta * base1 + (jdist[j]+0.5*(random()-0.5)) * eta * base2;
          NDCP = transform ( shadNDCSpace, Psample );
          NDCs = 0.5 * ( 1 + xcomp(NDCP) );
          NDCt = 0.5 * ( 1 - ycomp(NDCP) );
          Ddata = float texture( shdname, NDCs, NDCt, NDCs, NDCt, NDCs, NDCt, NDCs, NDCt, "samples", 1 );
          cameraP = transform( shadcamSpace, Psample );
          if ( zcomp(cameraP) + 0.1 > Ddata) 
          {
            Pin = cameraP * Ddata / zcomp(cameraP);
            Pin = transform( shadinvSpace, Pin );
            dist += distance( Q, Pin ) + depth;
            if (lightsource("__imgname", imgname) != 0 && imgname != "" )
              Cdata = color texture( imgname, NDCs, NDCt, NDCs, NDCt, NDCs, NDCt, NDCs, NDCt, "samples", 1 );
            
            c+= Cdata*Cl;
          }
          realsamples += dot;
        }
      }
    }
  }
  if ( realsamples > 0 )
  {
    dist /= realsamples;
    c /= realsamples;
  }
  else
    dist = 0;
  
  color result = Ksss * exp( -dist * sigma ) * c * tint;
  
  
	return result;
}
#endif            
