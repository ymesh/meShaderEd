surface me_floor( uniform float occ0_MaxSamples = 256.000;
 uniform float occ0_MinSamples = 128.000;
 uniform float occ0_MaxDist = 15.000;
 uniform float occ0_SampleBase = 0.000;
 uniform float occ0_Bias = 0.050;
 uniform string occ0_HitMode = "default";
 uniform string occ0_HitSides = "both";
 uniform float occ0_MaxVar = 0.150;
 uniform float occ0_MaxPixelDist = 0.000;
 uniform string occ0_Distribution = "cosine";
 uniform float occ0_FalloffMode = 0.000;
 uniform float occ0_FalloffValue = 0.000;
 string me_inShadowC0_category = "";
 float me_inShadowC0_opacity = 1.000;
 float me_inShadowC0_angle = 90.000;
 uniform float me_inShadowC0_invert = 0.000;
 float comp_MultInvertedC1_mult = 1.000;
 color me_gather0_filter = color(1.000,1.000,1.000);
 color me_gather0_fill = color(0.000,0.000,0.000);
 uniform string me_gather0_traceSet = "";
 uniform string me_gather0_rayLabel = "";
 uniform float me_gather0_rayDepth = 2.000;
 uniform float me_gather0_samples = 1.000;
 uniform float me_gather0_sampleBase = 1.000;
 float me_gather0_blur = 0.000;
 uniform float me_gather0_maxdist = -1.000;
 uniform float me_gather0_twosided = 1.000;
 float me_floor_mask = 1.000;
 output varying color __color = color(0.000,0.000,0.000);
 output varying color __diff = color(0.000,0.000,0.000);
 output varying color __spec = color(0.000,0.000,0.000);
 output varying color __diff_ibi = color(0.000,0.000,0.000);
 output varying color __spec_ibi = color(0.000,0.000,0.000);
 output varying color __shadow = color(0.000,0.000,0.000);
 output varying color __reflect = color(0.000,0.000,0.000);
 output varying color __sss = color(0.000,0.000,0.000);
 output varying color __pstrace = color(0.000,0.000,0.000);
 output varying float __occ = 0.000;
 output varying color __occ_C = color(0.000,0.000,0.000);
 output varying float __mask = 1.000;
 output varying color __mask_C = color(1.000,0.000,0.000) )
{
// START NODE normalizeI1 

vector normalizeI1_In = normalize(I);
// END NODE normalizeI1 

// START NODE normalizeN0 

normal normalizeN0_Nn = normalize(N);
// END NODE normalizeN0 

// START NODE ShadingNormal1 


	normal ShadingNormal1_NS = normalizeN0_Nn;
	uniform float ShadingNormal1_depth;
	
	rayinfo("depth", ShadingNormal1_depth);
	if ( ShadingNormal1_depth > 0 )
		ShadingNormal1_NS = faceforward( normalizeN0_Nn, normalizeI1_In, normalizeN0_Nn);
	else
	{
		uniform float sides = 2;
		attribute( "Sides", sides );
		if  (sides == 2 )
		  ShadingNormal1_NS = faceforward( normalizeN0_Nn, normalizeI1_In, normalizeN0_Nn );
	}	    
	
	
// END NODE ShadingNormal1 

// START NODE occ0 
uniform float occ0_Invert = 0.000;
uniform float occ0_Adaptive = 1.000;
uniform vector occ0_SkyAxis = vector(0.000,1.000,0.000);
float occ0_ConeAngle = 90.000;
uniform float occ0_MaxError = -1.000;
uniform string occ0_EnvMap = "";
uniform string occ0_EnvSpace = "";
uniform float occ0_BrtWarp = 1.000;
uniform string occ0_coordsys = "";
uniform string occ0_subset = "";
uniform string occ0_label = "";
uniform float occ0_seed = -1.000;
uniform float occ0_pointbased = 0.000;
uniform string occ0_PtcFile = "";
uniform float occ0_MaxSolidAngle = 0.100;
uniform float occ0_clamp = 1.000;


	
	varying color occ0_env_color = 0;
  varying vector occ0_bent_dir = 0;
  
	/* extern point P; */
  /* extern normal N; */
  /* normal Nss = meShadingNormal( N ); */
  
  /* if ( occ0_MaxDist == -1 )
	  occ0_MaxDist = 1.0e38; */
	
	float occ0_result = 0;
	#ifdef AIR  
   color occ0_occ_C = occlusion( P  
              ,ShadingNormal1_NS 
              ,radians( occ0_ConeAngle )
              ,occ0_bent_dir
              ,"samples",       occ0_MaxSamples
              /* ,"blur", mapblur */
              ,"bias",          occ0_Bias
              ,"label",         occ0_label
              ,"subset",        occ0_subset
              ,"maxdist",       occ0_MaxDist
              ,"maxerror",      occ0_MaxError 
              ,"maxpixeldist",  occ0_MaxPixelDist );
             occ0_result = comp( occ0_occ_C, 0 ); 
#else                           
   #ifdef PIXIE
   occ0_result = occlusion( P  
              ,ShadingNormal1_NS            
              ,occ0_MaxSamples
              ,"irradiance",    occ0_env_color /* The irradiance amount (output)  */
              /*,"minR",          MaxPixelDist  uniform float minR	 The closest distance between samples. */
              /*,"maxR",          MaxPixelDist uniform float maxR	The maximum distance between samples. */
              ,"bias",          occ0_Bias
              ,"maxdist",       occ0_MaxDist );
   #else
   occ0_result = occlusion( P  
              ,ShadingNormal1_NS            
              ,occ0_MaxSamples
              ,"adaptive",      occ0_Adaptive
              ,"minsamples",    occ0_MinSamples
              ,"maxdist",       occ0_MaxDist
  #ifdef DELIGHT             
              ,"axis",          occ0_SkyAxis
  #endif              
              ,"coneangle",     radians( occ0_ConeAngle )
              ,"samplebase",    occ0_SampleBase
              ,"bias",          occ0_Bias
              ,"hitmode",       occ0_HitMode
              ,"hitsides",      occ0_HitSides
              ,"maxvariation",  occ0_MaxVar
  #ifndef DELIGHT              
              ,"maxerror",      occ0_MaxError
              ,"maxpixeldist",  occ0_MaxPixelDist
              ,"seed",          occ0_seed
              ,"brightnesswarp",  occ0_BrtWarp
  #endif               
              ,"distribution",  occ0_Distribution
              ,"falloffmode",   occ0_FalloffMode
              ,"falloff",       occ0_FalloffValue
              
              ,"environmentmap",    occ0_EnvMap
              ,"environmentspace",  occ0_EnvSpace
              
              ,"coordsystem",   occ0_coordsys
              ,"subset",        occ0_subset
              ,"label",         occ0_label

              ,"pointbased",    occ0_pointbased
              ,"filename",      occ0_PtcFile
              ,"maxsolidangle", occ0_MaxSolidAngle
              ,"clamp",         occ0_clamp
              
              ,"environmentcolor",  occ0_env_color
              ,"environmentdir",    occ0_bent_dir );

  #endif /* PIXIE */             
#endif  /* AIR */           
              
  if ( occ0_Invert == 1 )              
    occ0_result = 1 - occ0_result;            
  
// END NODE occ0 

// START NODE me_inShadowC0 


	color me_inShadowC0_result = 0;
	color	me_inShadowC0_inShadow = color( 0 );
	color	me_inShadowC0_value = color( 0 );
	uniform float me_inShadowC0_count = 0;
#if defined(PRMAN) || defined(DELIGHT) 
  illuminance( me_inShadowC0_category, P, normalizeN0_Nn, radians( me_inShadowC0_angle ), "lightcache", "refresh" ) 
#else
  P = P;
  illuminance( me_inShadowC0_category, P, normalizeN0_Nn, radians( me_inShadowC0_angle ) ) 
#endif
  {
    lightsource( "__inShadowC", me_inShadowC0_inShadow ); 	
    me_inShadowC0_value += me_inShadowC0_inShadow;
    me_inShadowC0_count += 1;
  } 
  
  me_inShadowC0_result = clamp( me_inShadowC0_value, color(0), color(1) ) * me_inShadowC0_opacity;  /* value / count * opacity; */
  /* if ( count ) 
    result /= count; */
  if ( me_inShadowC0_invert )
    me_inShadowC0_result = 1 - me_inShadowC0_result;
  
// END NODE me_inShadowC0 

// START NODE color0 
color color0_in = color(0.641,0.469,0.453);

color color0_out = color0_in;
// END NODE color0 

// START NODE comp_MultInvertedC1 


	color comp_MultInvertedC1_outColor = color0_out * ( (1 - comp_MultInvertedC1_mult) + comp_MultInvertedC1_mult * ( 1 - me_inShadowC0_result ) );
	
	
// END NODE comp_MultInvertedC1 

// START NODE P0 

point P0_P = P;
// END NODE P0 

// START NODE reflect0 

 vector reflect0_outVector = reflect(normalizeI1_In, normalizeN0_Nn);
// END NODE reflect0 

// START NODE me_gather0 
vector me_gather0_dQu = vector(0.000,0.000,0.000);
vector me_gather0_dQv = vector(0.000,0.000,0.000);


	/* extern normal N; */
	/* extern vector I; */
	uniform float me_gather0_raydepth = 0;
	color me_gather0_sci = 0, me_gather0_soi = 0;
	color me_gather0_outColor = 0;
	color me_gather0_outOpacity = 1;
	
	/* if ( me_gather0_maxdist == -1 )
	  me_gather0_maxdist = 1.0e38; */
	  
	rayinfo("depth", me_gather0_raydepth);
	
	if ( me_gather0_raydepth <= me_gather0_rayDepth )
	{
    if (( me_gather0_twosided != 0 || ShadingNormal1_NS.I <= 0) && me_gather0_samples > 0)
    {
      color me_gather0_outOpacity = 0;
      gather("illuminance", 
              P0_P, 
              reflect0_outVector, 
              me_gather0_blur * radians(5), 
              me_gather0_samples,
              "subset", me_gather0_traceSet,
              "label", me_gather0_rayLabel,
              "samplebase", me_gather0_sampleBase,
              "maxdist", me_gather0_maxdist,
              "surface:Ci", me_gather0_sci,
              "surface:Oi", me_gather0_soi 
      ) 
      {
        me_gather0_outColor += me_gather0_sci;
        me_gather0_outOpacity += me_gather0_soi;
      } 
      else 
      {
        me_gather0_outColor += me_gather0_fill;	
      }
      
      me_gather0_outColor /= me_gather0_samples;
      me_gather0_outOpacity /= me_gather0_samples;
    }
  }
  me_gather0_outColor *= me_gather0_filter;

	
// END NODE me_gather0 

// START NODE comp_AddC1 
float comp_AddC1_mult = 1.000;


	color comp_AddC1_outColor = comp_MultInvertedC1_outColor  + comp_AddC1_mult * me_gather0_outColor;
	
	
// END NODE comp_AddC1 

// START NODE me_floor 
color me_floor_Oi = color(1.000,1.000,1.000);
color me_floor_diff = color(1.000,1.000,1.000);
color me_floor_spec = color(0.000,0.000,0.000);
color me_floor_diff_ibi = color(1.000,1.000,1.000);
color me_floor_spec_ibi = color(0.000,0.000,0.000);
color me_floor_sss = color(0.000,0.000,0.000);
color me_floor_pstrace = color(0.000,0.000,0.000);
color me_floor_occ_C = color(0.000,0.000,0.000);


	Ci = comp_AddC1_outColor * me_floor_Oi; 
	Oi = me_floor_Oi;
	__color = color0_out;
	__diff = me_floor_diff;
	__spec = me_floor_spec;
	__diff_ibi = me_floor_diff_ibi;
	__spec_ibi = me_floor_spec_ibi;
	__shadow = me_inShadowC0_result;
	__reflect = me_gather0_outColor;
	__sss = me_floor_sss;
	
	__pstrace = me_floor_pstrace;
	
	__occ = occ0_result;
	__occ_C = me_floor_occ_C;
	
	__mask = me_floor_mask;
	__mask_C = me_gather0_outOpacity;
	
	
// END NODE me_floor 

}
