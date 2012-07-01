#ifndef ME_BAKE_H
#define ME_BAKE_H
#include "me_util.h"
/*-----------------------------------------------------------*
  
 *-----------------------------------------------------------*/
float meBake3dFloat(
	point Q;
	normal QN;
	uniform string ChannelName;	 /* The channel name to bake */
	float Channel;							 /* baking value */
	uniform string PtcFile;
	uniform string CoordSys;
	uniform string CacheLifetime; /* specifies the lifetime of the cache. 
																	"file" or "" (the default) means that the data 
																	are read from a file. 
																	"frame" or "shadinggrid" means that the data 
																	are read from a cache of that lifetime. */
	float Radius;	/* the radius specifies the size of the area that the data point 
									represents. If no radius is specified, one will be automatically 
									computed from the distance to the nearest shading points.*/
	float RadiusScale; /* a multiplier on radius */
	float Interpolate; /* point positions, normals, radii, and data are interpolated 
												from four shading points when this parameter is set. 
												This means that micropolygon midpoints are baked out 
												instead of the exact shading points. 
												This is great for many applications because it eliminates 
												the double shading points along edges of shading grids. 
												This behavior is probably only useful if the P points 
												passed to bake3d() are the original shading point positions. 
												Off by default (but recommended for e.g. baking of direct 
												illumination for subsurface scattering). */

												
)
{
	
	float result = Channel;
	uniform float raydepth, disable = 0;	
	rayinfo("depth", raydepth);
	if(raydepth > 0) 
		disable = 1;
	if( disable != 1 && PtcFile != "") 
	{
		bake3d( PtcFile, ChannelName, Q , QN	
					, ChannelName, result
					, "coordsystem", CoordSys
					, "cachelifetime", CacheLifetime
					, "radius", Radius
					, "radiusscale", RadiusScale
					, "interpolate", Interpolate 
					);
	}
	return result;
}
 
#endif ME_BAKE_H
