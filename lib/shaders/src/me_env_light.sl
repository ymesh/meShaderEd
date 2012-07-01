/*-----------------------------------------------------------*/
#include "me_util.h"
#include "me_env.h" 
/*-----------------------------------------------------------*/
light
me_env_light (
    uniform string envName = "";
    uniform string envSpace = "world";
    uniform float  envRadius = 0;
    uniform float  Intensity = 1.0;
		uniform float	 Coloration = 0;
		uniform color	 cFilt = 1;
		uniform string Filter = "gaussian";
		uniform float  filterWidth = 0;
		uniform float  useSampledBlur = 0;
		uniform float	 samples = 32;
    uniform float  lerp = 1;
    output uniform string __category = "environment";
    output varying float  __nondiffuse = 1;
    output varying float  __nonspecular = 1;
    )
{
    extern point Ps;
    point Q = Ps;

    extern vector I;
		extern normal N;
		
		varying float blur;
		
		uniform float  reflBlur = 0;
		uniform float  DiffHemisphere = .95; /* Controls the region of the hemisphere
		                                        above a shading point from which to gather
		                                        diffuse environmental illumination. */

		
#ifdef DELIGHT
    normal shading_normal = normalize( faceforward(Ns, I) );
#else
    normal Nn = normalize( N );
    normal Nf = faceforward( Nn, I, Nn );
    normal shading_normal = normalize( Nf );
#endif
    
    vector IN = normalize (I);
    vector Rfldir;
    vector r = 0;
    float kr = 1;
   
    Cl = 0;		
    solar () 
    {
     
      if( envName != "" ) 
      {

        color env = 0;
        float b = blur / PI;
        color filt = mix (color 1, cFilt, Coloration); 
         
        if( 0 == surface ("__L", Rfldir) )     
      	  Rfldir = reflect( IN, shading_normal );

      	if( 0 == surface ("__blur", blur) )
    		 	blur = reflBlur;
  		
    		
  
#ifndef AIR
        /* Avoid using hemisphere sampled blur for environment. 
           Reason -- Pixie an Air don't support "environment( envname, v1, v2, v3, v4,..." */
    		if ( useSampledBlur )
    		{
    		  float w = meCalculateEnvSampleArea( DiffHemisphere, samples ); 
    		  vector rs, v1, v2, v3, v4;
    		  
    		  gather( "samplepattern", Q, Rfldir,
                blur * DiffHemisphere,
                samples,
                "distribution", "cosine",
                "ray:direction", r) {
          }  
          else 
          {
  #ifdef PIXIE    		     
  		      rs = meRayEnvSphere( Q, envSpace, r, envRadius ); 
  #else
  		      meBuildEnvironmentVectors( w, r, v1, v2, v3, v4 ); 
    		    v1 = meRayEnvSphere( Q, envSpace, v1, envRadius );
    		    v2 = meRayEnvSphere( Q, envSpace, v2, envRadius );
    		    v3 = meRayEnvSphere( Q, envSpace, v3, envRadius );
    		    v4 = meRayEnvSphere( Q, envSpace, v4, envRadius );
  #endif    		    
    		    env += color environment ( 
    		        envName, 
  #ifdef PIXIE    		        
    		        rs
  #else    		        
    		        v1, v2, v3, v4
  #endif      		        
    		        ,"blur", b
    					  ); 
 		      }
 		      env /= samples;
    		}
    		else

#endif /* AIR */    		
    		{
    		  /*
    		  if ( envName != "raytrace" || envName != "reflection" )
    		    r = meRayEnvSphere( Q, envSpace, Rfldir, envRadius );  
    		  else
    		    r = Rfldir; 
    		  */
    		  r = meRayEnvSphere( Q, envSpace, Rfldir, envRadius );
   		    
    		  env = color environment ( 
    		        envName, r
    				    ,"blur", b 
    				    ,"samples", samples 
    				    ,"filter", Filter
    				    ,"width", filterWidth
#ifndef PIXIE     					  
    					  ,"lerp", lerp
#endif    					  
    					  ); 
    		}
    		Cl = env * filt;			  
      }

    }
    Cl *= Intensity;
    
   
}

