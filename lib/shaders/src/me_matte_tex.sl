surface me_matte_tex( float diff_Kd = 1.000;
 float diff_atten = 1.000;
 float diff_from = 0.000;
 string me_inShadowC_category = "";
 float me_inShadowC_opacity = 1.000;
 float me_inShadowC_angle = 90.000;
 uniform float me_inShadowC_invert = 0.000;
 uniform float occ_MaxSamples = 256.000;
 uniform float occ_MinSamples = 128.000;
 uniform float occ_MaxDist = 15.000;
 uniform float occ_SampleBase = 0.000;
 uniform float occ_Bias = 0.050;
 uniform string occ_HitMode = "default";
 uniform string occ_HitSides = "both";
 uniform float occ_MaxVar = 0.150;
 uniform float occ_MaxPixelDist = 0.000;
 uniform string occ_Distribution = "cosine";
 uniform float occ_FalloffMode = 0.000;
 uniform float occ_FalloffValue = 0.000;
 uniform float ST0_repeatS = 1.000;
 uniform float ST0_repeatT = 1.000;
 uniform float ST0_offsetS = 0.000;
 uniform float ST0_offsetT = 0.000;
 uniform float ST0_flipS = 0.000;
 uniform float ST0_flipT = 0.000;
 color image_defColor = color(1.000,1.000,1.000);
  uniform string image_File = "";
 uniform float image_fillOutside = 0.000;
 uniform float image_alphaOp = 0.000;
 uniform string image_filter = "gaussian";
 uniform float image_SFilt = 1.000;
 uniform float image_TFilt = 1.000;
 uniform float image_lerp = 1.000;
 float me_diff_ibi_dBlur = 0.700;
 float me_diff_ibi_Kd = 0.800;
 float diff_ibi_Saturation_value = 1.000;
 float spec_ibi1_rBlur = 0.100;
 float spec_ibi1_KrMin = 0.000;
 float spec_ibi1_KrMax = 0.250;
 float spec_ibi1_IOR = 1.500;
 float spec_ibi_Saturation_value = 1.000;
 
 float comp_diff_mult = 1.000;
 float comp_diff_ibi_mult = 1.000;
 float comp_spec_ibi_mult = 1.000;
 float comp_occ_mult = 1.000;
 float comp_shadow_mult = 1.000;
 
 float me_matte_tex_mask = 1.000;
 color me_matte_tex_mask_C = color(1.000,0.000,0.000);
 
 output varying vector __L = vector(0.000,0.000,1.000);
 output varying float __blur = 0.000;
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

// START NODE FaceForwardNormal0 


	normal FaceForwardNormal0_fwN = faceforward( normalizeN0_Nn, normalizeI1_In, normalizeN0_Nn);
// END NODE FaceForwardNormal0 

// START NODE diff 
string diff_category = "";
float diff_to = 1.000;
color diff_coloration = color(1.000,1.000,1.000);


	
	color diff_result = 0;
	color diff_diffColor = 0;
#if defined( PRMAN ) || defined( DELIGHT )             
	illuminance ( diff_category, P, FaceForwardNormal0_fwN, PI/2, "lightcache", "refresh" )
#else
	illuminance ( diff_category, P, FaceForwardNormal0_fwN, PI/2 )
#endif
	{
		float nondiff = 0;
		lightsource( "__nondiffuse", nondiff );
		if (nondiff < 1)
			diff_diffColor += ( 1 - nondiff ) * Cl *( FaceForwardNormal0_fwN.normalize(L) );
	}
	
	float diff_hueComp = comp( ctransform( "hsv" , diff_diffColor ) , 0 );
	float diff_satComp = comp( ctransform( "hsv" , diff_diffColor ), 1 );
	float diff_lumiComp = comp( ctransform( "hsv" , diff_diffColor ), 2 ); /*  get value component from HSV color space */
	color diff_hsvDiff = color "hsv" ( diff_hueComp, diff_satComp, ( diff_from + ( diff_to - diff_from ) * pow( diff_lumiComp, diff_atten ) ) );
  
	diff_result = diff_coloration * diff_Kd * diff_hsvDiff;
			
  
// END NODE diff 

// START NODE me_inShadowC 


	color me_inShadowC_result = 0;
	color	me_inShadowC_inShadow = color( 0 );
	color	me_inShadowC_value = color( 0 );
	uniform float me_inShadowC_count = 0;
#if defined( PRMAN ) || defined( DELIGHT )
  illuminance( me_inShadowC_category, P, normalizeN0_Nn, radians( me_inShadowC_angle ), "lightcache", "refresh" )  
  P = P; /* dirty light cache */
#else
  illuminance( me_inShadowC_category, P, normalizeN0_Nn, radians( me_inShadowC_angle ) )  
#endif
  {
    lightsource( "__inShadowC", me_inShadowC_inShadow ); 	
    me_inShadowC_value += me_inShadowC_inShadow;
    me_inShadowC_count += 1;
  } 
  
  me_inShadowC_result = clamp( me_inShadowC_value, color(0), color(1) ) * me_inShadowC_opacity;  /* value / count * opacity; */
  /* if ( count ) 
    result /= count; */
  if ( me_inShadowC_invert )
    me_inShadowC_result = 1 - me_inShadowC_result;
  
// END NODE me_inShadowC 

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

// START NODE occ 
uniform float occ_Invert = 0.000;
uniform float occ_Adaptive = 1.000;
uniform vector occ_SkyAxis = vector(0.000,1.000,0.000);
float occ_ConeAngle = 90.000;
uniform float occ_MaxError = -1.000;
uniform string occ_EnvMap = "";
uniform string occ_EnvSpace = "";
uniform float occ_BrtWarp = 1.000;
uniform string occ_coordsys = "";
uniform string occ_subset = "";
uniform string occ_label = "";
uniform float occ_seed = -1.000;
uniform float occ_pointbased = 0.000;
uniform string occ_PtcFile = "";
uniform float occ_MaxSolidAngle = 0.100;
uniform float occ_clamp = 1.000;


	
	varying color occ_env_color = 0;
  varying vector occ_bent_dir = 0;
  
	/* extern point P; */
  /* extern normal N; */
  /* normal Nss = meShadingNormal( N ); */
  
  /* if ( occ_MaxDist == -1 )
	  occ_MaxDist = 1.0e38; */
	
	float occ_result = 0;
	#ifdef AIR  
   color occ_occ_C = occlusion( P  
              ,ShadingNormal1_NS 
              ,radians( occ_ConeAngle )
              ,occ_bent_dir
              ,"samples",       occ_MaxSamples
              /* ,"blur", mapblur */
              ,"bias",          occ_Bias
              ,"label",         occ_label
              ,"subset",        occ_subset
              ,"maxdist",       occ_MaxDist
              ,"maxerror",      occ_MaxError 
              ,"maxpixeldist",  occ_MaxPixelDist );
             occ_result = comp( occ_occ_C, 0 ); 
#else                           
   #ifdef PIXIE
   occ_result = occlusion( P  
              ,ShadingNormal1_NS            
              ,occ_MaxSamples
              ,"irradiance",    occ_env_color /* The irradiance amount (output)  */
              /*,"minR",          MaxPixelDist  uniform float minR	 The closest distance between samples. */
              /*,"maxR",          MaxPixelDist uniform float maxR	The maximum distance between samples. */
              ,"bias",          occ_Bias
              ,"maxdist",       occ_MaxDist );
   #else
   occ_result = occlusion( P  
              ,ShadingNormal1_NS            
              ,occ_MaxSamples
              ,"adaptive",      occ_Adaptive
              ,"minsamples",    occ_MinSamples
              ,"maxdist",       occ_MaxDist
  #ifdef DELIGHT             
              ,"axis",          occ_SkyAxis
  #endif              
              ,"coneangle",     radians( occ_ConeAngle )
              ,"samplebase",    occ_SampleBase
              ,"bias",          occ_Bias
              ,"hitmode",       occ_HitMode
              ,"hitsides",      occ_HitSides
              ,"maxvariation",  occ_MaxVar
  #ifndef DELIGHT              
              ,"maxerror",      occ_MaxError
              ,"maxpixeldist",  occ_MaxPixelDist
              ,"seed",          occ_seed
              ,"brightnesswarp",  occ_BrtWarp
  #endif               
              ,"distribution",  occ_Distribution
              ,"falloffmode",   occ_FalloffMode
              ,"falloff",       occ_FalloffValue
              
              ,"environmentmap",    occ_EnvMap
              ,"environmentspace",  occ_EnvSpace
              
              ,"coordsystem",   occ_coordsys
              ,"subset",        occ_subset
              ,"label",         occ_label

              ,"pointbased",    occ_pointbased
              ,"filename",      occ_PtcFile
              ,"maxsolidangle", occ_MaxSolidAngle
              ,"clamp",         occ_clamp
              
              ,"environmentcolor",  occ_env_color
              ,"environmentdir",    occ_bent_dir );

  #endif /* PIXIE */             
#endif  /* AIR */           
              
  if ( occ_Invert == 1 )              
    occ_result = 1 - occ_result;            
  
// END NODE occ 

// START NODE floatToColor0 

color floatToColor0_outColor = color(occ_result, occ_result, occ_result);
// END NODE floatToColor0 

// START NODE ST0 
uniform float ST0_angle = 0.000;


		point ST0_Q;
		vector ST0_dQu;
		vector ST0_dQv;
		
		setxcomp( ST0_Q, ST0_repeatS * s + ST0_offsetS);
    setycomp( ST0_Q, ST0_repeatT * t + ST0_offsetT);
    setzcomp( ST0_Q, 0);
    
    if ( ST0_angle != 0 )
      ST0_Q = rotate(ST0_Q, radians(ST0_angle), point(0,0,0), point(0,0,1)); 

    ST0_dQu = vector Du(ST0_Q)*du;
    ST0_dQv = vector Dv(ST0_Q)*dv;
    
    if ( ST0_flipS == 1 )
      setxcomp( ST0_Q, 1 - xcomp(ST0_Q) );
    if ( ST0_flipT == 1 )
      setycomp( ST0_Q, 1 - ycomp(ST0_Q) );
  		    	
  	
  	
  
// END NODE ST0 

// START NODE image 


	color image_colorResult = image_defColor;
  float image_floatResult = 1;
  
  float image_x = xcomp( ST0_Q );
  float image_y = ycomp( ST0_Q );
	
  if ( image_File != "" ) 
  {
		image_colorResult = color texture(
			image_File, 
			image_x,
			image_y,
			"swidth", image_SFilt,
			"twidth", image_TFilt,
			"filter", image_filter,
			"lerp", image_lerp );
			
		if ( image_alphaOp != 0 ) /* "nop" */
		{
			uniform float nChannels = 3;
			textureinfo( image_File, "channels", nChannels );
			
			if ( nChannels > 3 )
			{
				image_floatResult = float texture(
							image_File[3],
							image_x,
							image_y,
							"swidth", image_SFilt,
							"twidth", image_TFilt,
							"filter", image_filter,
							"lerp", image_lerp );
				if ( image_alphaOp == 2 )
				{
				  image_colorResult *= image_floatResult;
				}
				if ( image_alphaOp == 3 ) /* assume AlphaOp == "unassociated" */
				{
					if( image_floatResult != 0 )
					{
						image_colorResult /= image_floatResult;
						image_colorResult = clamp( image_colorResult, color(0), color(1) );
					}
				}
			}
				 
			/*	if ( fillOutside  == 1 ) */
			image_colorResult = mix( image_defColor, image_colorResult, image_floatResult ); 
		}
		if ( ( image_fillOutside == 1 ) && ( image_x < 0 || image_x > 1 || image_y < 0 || image_y > 1) )   
				image_colorResult = image_defColor;
	} 
	 
  
// END NODE image 

// START NODE comp_diff 


	color comp_diff_outColor = image_colorResult * ( (1 - comp_diff_mult) + comp_diff_mult * diff_result );
	
	
// END NODE comp_diff 

// START NODE me_diff_ibi 
string me_diff_ibi_category = "environment";


	
	__L = vector ( normalizeN0_Nn );
  __blur = me_diff_ibi_dBlur;
	
	color me_diff_ibi_result = 0;
	#ifndef AIR   
	illuminance ( me_diff_ibi_category, P,  "lightcache", "refresh" )
	#else
	P = P; /* dirty light cache */
	illuminance ( me_diff_ibi_category, P )
	#endif 
  {
    me_diff_ibi_result += Cl;
  }     

  me_diff_ibi_result *= me_diff_ibi_Kd;
			
  
// END NODE me_diff_ibi 

// START NODE clampC0 
color clampC0_min = color(0.000,0.000,0.000);
color clampC0_max = color(1.000,1.000,1.000);

color clampC0_result = clamp((me_diff_ibi_result), (clampC0_min), (clampC0_max));
// END NODE clampC0 

// START NODE diff_ibi_Saturation 


	float diff_ibi_Saturation_lum = .2125*comp( clampC0_result, 0) + .7154*comp(clampC0_result, 1) + .0721*comp(clampC0_result, 2);
	color diff_ibi_Saturation_result = mix( color( diff_ibi_Saturation_lum ), clampC0_result, diff_ibi_Saturation_value );
	
// END NODE diff_ibi_Saturation 

// START NODE comp_diff_ibi 


	color comp_diff_ibi_outColor = comp_diff_outColor * ( (1 - comp_diff_ibi_mult) + comp_diff_ibi_mult * diff_ibi_Saturation_result );
	
	
// END NODE comp_diff_ibi 

// START NODE spec_ibi1 
string spec_ibi1_category = "environment";


	color spec_ibi1_result = 0;

  float spec_ibi1_Kr = spec_ibi1_KrMax;
	vector spec_ibi1_R = vector (0);
	vector spec_ibi1_V = normalize( I );  
  
  if ( spec_ibi1_IOR > 0 )
	{
    vector T;
    float Kt;
    float f = max( spec_ibi1_IOR, 1.0e-4 );
    fresnel( spec_ibi1_V, ShadingNormal1_NS, ( I.ShadingNormal1_NS < 0 ) ? 1.0/f : spec_ibi1_IOR , spec_ibi1_Kr, Kt, spec_ibi1_R, T );
    spec_ibi1_Kr = mix( spec_ibi1_KrMin, spec_ibi1_KrMax, spec_ibi1_Kr );
	}
	else
	{
    spec_ibi1_R = reflect( spec_ibi1_V, ShadingNormal1_NS );
	}
  
  __L = spec_ibi1_R;
  __blur = spec_ibi1_rBlur;
  /* P = P; dirty light cache */
  #ifndef AIR
  illuminance ( spec_ibi1_category, P, "lightcache", "refresh" ) /* , "lightcache", "refresh" */
  #else
  P = P; /* dirty light cache */
  illuminance ( spec_ibi1_category, P )
  #endif
  {
    spec_ibi1_result += Cl;
  }     

  spec_ibi1_result *= spec_ibi1_Kr;
			
  
// END NODE spec_ibi1 

// START NODE spec_ibi_Saturation 


	float spec_ibi_Saturation_lum = .2125*comp( spec_ibi1_result, 0) + .7154*comp(spec_ibi1_result, 1) + .0721*comp(spec_ibi1_result, 2);
	color spec_ibi_Saturation_result = mix( color( spec_ibi_Saturation_lum ), spec_ibi1_result, spec_ibi_Saturation_value );
	
// END NODE spec_ibi_Saturation 

// START NODE comp_spec_ibi 


	color comp_spec_ibi_outColor = comp_diff_ibi_outColor  + comp_spec_ibi_mult * spec_ibi_Saturation_result;
	
	
// END NODE comp_spec_ibi 

// START NODE comp_occ 


	color comp_occ_outColor = comp_spec_ibi_outColor * ( (1 - comp_occ_mult) + comp_occ_mult * ( 1 - floatToColor0_outColor ) );
	
	
// END NODE comp_occ 

// START NODE comp_shadow 


	color comp_shadow_outColor = comp_occ_outColor * ( (1 - comp_shadow_mult) + comp_shadow_mult * ( 1 - me_inShadowC_result ) );
	
	
// END NODE comp_shadow 

// START NODE psTrace0 

	
	  normal psTrace0_Nf;
 		normal psTrace0_Nc;
    color psTrace0_out = 0;		
 		psTrace0_Nf = faceforward(normalize(N), I);
    psTrace0_Nc = transform("camera", (psTrace0_Nf + point "camera" (0,0,0)));
    psTrace0_Nc = normalize(psTrace0_Nc);
		    
    setcomp(psTrace0_out, 0, clamp((0.5 - xcomp(psTrace0_Nc) / 2), 0, 1));
    setcomp(psTrace0_out, 1, clamp((0.5 + ycomp(psTrace0_Nc) / 2), 0, 1));
    setcomp(psTrace0_out, 2, clamp(abs(zcomp(psTrace0_Nc)), 0, 1));	
  
// END NODE psTrace0 

// START NODE me_matte_tex 
color me_matte_tex_Oi = color(1.000,1.000,1.000);
color me_matte_tex_spec = color(0.000,0.000,0.000);
color me_matte_tex_reflect = color(0.000,0.000,0.000);
color me_matte_tex_sss = color(0.000,0.000,0.000);
color me_matte_tex_occ_C = color(0.000,0.000,0.000);


	Ci = comp_shadow_outColor * me_matte_tex_Oi; 
	Oi = me_matte_tex_Oi;
	__color = image_colorResult;
	__diff = diff_result;
	__spec = me_matte_tex_spec;
	__diff_ibi = diff_ibi_Saturation_result;
	__spec_ibi = spec_ibi_Saturation_result;
	__shadow = me_inShadowC_result;
	__reflect = me_matte_tex_reflect;
	__sss = me_matte_tex_sss;
	
	__pstrace = psTrace0_out;
	
	__occ = occ_result;
	__occ_C = me_matte_tex_occ_C;
	
	__mask = me_matte_tex_mask;
	__mask_C = me_matte_tex_mask_C;
	
	
// END NODE me_matte_tex 

}
