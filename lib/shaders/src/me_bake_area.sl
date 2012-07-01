/*-----------------------------------------------------------*/
#include "me_bake.h"
/*-----------------------------------------------------------*/
surface me_bake_area(
	color SurfaceColor = color(0, .25, 1 );
	color SurfaceOpacity = 1;
/* meBake3d parameters */   
	/* uniform string ChannelName = "";	*/
	uniform string PtcFile = "";
	uniform string BakeCoordSys = "";
	uniform string CacheLifetime = "";
	float Radius = 0;
	float RadiusScale = 1;
	float Interpolate = 0;
)  
{
	extern point P;
  extern normal N;
  /* normal Nss = meShadingNormal( N ); */
  normal Nn = normalize(N);
  Oi = SurfaceOpacity;
  uniform string ChannelName = "_area";
  float a = area(P, "dicing"); /* micropolygon area */
  float opacity = 0.333333 * (Oi[0] + Oi[1] + Oi[2]); /* average opacity */
  a *= opacity; /* reduce area if non-opaque */
  if (a > 0)
  meBake3dFloat( P, Nn
  					  ,ChannelName            
  					  ,a
  					  ,PtcFile
  					  ,BakeCoordSys
              ,CacheLifetime        
              ,Radius        
              ,RadiusScale
              ,Interpolate ); 
              
  
  Ci = SurfaceColor * Oi;
}
