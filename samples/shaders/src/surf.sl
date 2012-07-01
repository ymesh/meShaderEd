/* Generated by meShaderEd */

#define SURFACE_SHADER surf
surface surf (
)
{
uniform float ST_angle = 0.000;
uniform float ST_repeatS = 1.000;
uniform float ST_repeatT = 1.000;
uniform float ST_offsetS = 0.000;
uniform float ST_offsetT = 0.000;
uniform float ST_flipS = 1.000;
uniform float ST_flipT = 1.000;
point ST_Q = point(0.000,0.000,0.000);
vector ST_duQ = vector(0.000,0.000,0.000);
vector ST_dvQ = vector(0.000,0.000,0.000);
point P_P = point(0.000,0.000,0.000);
float CurrentPoint_Frequency = 1.000;
point CurrentPoint_Q = point(0.000,0.000,0.000);
vector CurrentPoint_duQ = vector(0.000,0.000,0.000);
vector CurrentPoint_dvQ = vector(0.000,0.000,0.000);
float FractalV_Layers = 6.000;
float FractalV_Frequency = 1.000;
float FractalV_Lacunarity = 1.000;
float FractalV_Dimension = 0.000;
float FractalV_Flow = 0.000;
float FractalV_Variation = 0.000;
vector FractalV_result = vector(0.000,0.000,0.000);
vector MWarp_Kw = vector(1.000,1.000,1.000);
point MWarp_Q = point(0.000,0.000,0.000);
vector MWarp_duQ = vector(0.000,0.000,0.000);
vector MWarp_dvQ = vector(0.000,0.000,0.000);
color ImageFileC_defColor = color(0.000,0.000,0.000);
float ImageFileC_defFloat = 1.000;
uniform string ImageFileC_File = "grid.tif.tdl";
uniform float ImageFileC_fillOutside = 0.000;
uniform float ImageFileC_alphaOp = 0.000;
uniform string ImageFileC_filter = "gaussian";
uniform float ImageFileC_SFilt = 1.000;
uniform float ImageFileC_TFilt = 1.000;
uniform float ImageFileC_lerp = 1.000;
color ImageFileC_colorResult = color(0.000,0.000,0.000);
float ImageFileC_floatResult = 0.000;
color surf_Oi = color(1.000,1.000,1.000);

	  #ifdef SURFACE_SHADER
	  P_P = P;
	  #endif
	  #ifdef DISPLACEMENT_SHADER
	  P_P = P;
	  #endif
	  #ifdef LIGHT_SHADER
	  P_P = Ps;
	  #endif
	  #ifdef VOLUME_SHADER
	  P_P = Pv;
	  #endif
	  
	  CurrentPoint_Q = CurrentPoint_Frequency * P_P;
    CurrentPoint_duQ = Du( CurrentPoint_Q ) * du;
    CurrentPoint_dvQ = Dv( CurrentPoint_Q ) * dv;
	
	  vector FractalV_Noise(point Q)
		{
			extern float FractalV_Variation;
			vector	V;
			
			V = vector noise( Q, FractalV_Variation );
			V = vector( 
			    smoothstep(.2, .8, comp(V, 0)),
			    smoothstep(.2, .8, comp(V, 1)),
			    smoothstep(.2, .8, comp(V, 2))
			);
			return ( 2 * V - vector 1 );
		}
		       
		uniform float	FractalV_i;
		float	FractalV_sum, FractalV_mag, FractalV_f;
		point	FractalV_QQ;
		float	FractalV_dQ;
		vector FractalV_value = vector( 0 );   
		    
		FractalV_dQ = max(
			max( abs(xcomp( CurrentPoint_duQ )) + abs(xcomp( CurrentPoint_dvQ )), abs(ycomp( CurrentPoint_duQ )) + abs(ycomp( CurrentPoint_dvQ )) ),
			abs(zcomp( CurrentPoint_duQ )) + abs(zcomp( CurrentPoint_dvQ ))
		);

		FractalV_QQ = CurrentPoint_Q; 
		FractalV_f = FractalV_Frequency;
		FractalV_result = mix( FractalV_Noise( FractalV_f * FractalV_QQ ), vector 0, smoothstep (.25, 1, FractalV_f * FractalV_dQ ));
		FractalV_QQ += FractalV_Flow / FractalV_Layers * FractalV_result;
		FractalV_sum = 1;

		for ( FractalV_i = 1 ; FractalV_i < FractalV_Layers ; FractalV_i += 1) 
	  {
			FractalV_f *= FractalV_Lacunarity;
			FractalV_mag = 1/pow( FractalV_f, 3 - 2 * FractalV_Dimension );
			FractalV_value += FractalV_mag * mix( FractalV_Noise( FractalV_f * FractalV_QQ ), vector 0, smoothstep (.25, 1, FractalV_f * FractalV_dQ ));
			FractalV_QQ += FractalV_Flow / FractalV_Layers * FractalV_value;
			FractalV_result += FractalV_value;
			FractalV_sum += FractalV_mag;
		}

		FractalV_result /= FractalV_sum;	
  
		setxcomp( ST_Q, ST_repeatS * s + ST_offsetS);
    setycomp( ST_Q, ST_repeatT * t + ST_offsetT);
    setzcomp( ST_Q, 0);
    
    if ( ST_angle != 0 )
      ST_Q = rotate(ST_Q, radians(ST_angle), point(0,0,0), point(0,0,1)); 

    ST_duQ = vector Du( ST_Q ) * du;
    ST_dvQ = vector Dv( ST_Q ) * dv;
    
    if ( ST_flipS == 1 )
      setxcomp( ST_Q, 1 - xcomp(ST_Q) );
    if ( ST_flipT == 1 )
      setycomp( ST_Q, 1 - ycomp(ST_Q) );
  
	  MWarp_Q = ST_Q * MWarp_Kw * FractalV_result;
		MWarp_duQ = vector Du( MWarp_Q ) * du;
		MWarp_dvQ = vector Dv( MWarp_Q ) * dv;
	
	ImageFileC_colorResult = ImageFileC_defColor;
  ImageFileC_floatResult = ImageFileC_defFloat;
  
  float ImageFileC_x = xcomp( MWarp_Q );
  float ImageFileC_y = ycomp( MWarp_Q );
	
  if ( ImageFileC_File != "" ) 
  {
		ImageFileC_colorResult = color texture(
			ImageFileC_File, 
			ImageFileC_x,
			ImageFileC_y,
			"swidth", ImageFileC_SFilt,
			"twidth", ImageFileC_TFilt,
			"filter", ImageFileC_filter,
			"lerp", ImageFileC_lerp );
			
		if ( ImageFileC_alphaOp != 0 ) /* "nop" */
		{
			uniform float nChannels = 3;
			textureinfo( ImageFileC_File, "channels", nChannels );
			
			if ( nChannels > 3 )
			{
				ImageFileC_floatResult = float texture(
							ImageFileC_File[3],
							ImageFileC_x,
							ImageFileC_y,
							"swidth", ImageFileC_SFilt,
							"twidth", ImageFileC_TFilt,
							"filter", ImageFileC_filter,
							"lerp", ImageFileC_lerp );
				if ( ImageFileC_alphaOp == 2 )
				{
				  ImageFileC_colorResult *= ImageFileC_floatResult;
				}
				if ( ImageFileC_alphaOp == 3 ) /* assume AlphaOp == "unassociated" */
				{
					if( ImageFileC_floatResult != 0 )
					{
						ImageFileC_colorResult /= ImageFileC_floatResult;
						ImageFileC_colorResult = clamp( ImageFileC_colorResult, color(0), color(1) );
					}
				}
			}
				 
			/*	if ( fillOutside  == 1 ) */
			ImageFileC_colorResult = mix( ImageFileC_defColor, ImageFileC_colorResult, ImageFileC_floatResult ); 
		}
		if ( ( ImageFileC_fillOutside == 1 ) && ( ImageFileC_x < 0 || ImageFileC_x > 1 || ImageFileC_y < 0 || ImageFileC_y > 1) )   
				ImageFileC_colorResult = ImageFileC_defColor;
	} 
	 
  
	  Ci = ImageFileC_colorResult * surf_Oi; 
	  Oi = surf_Oi;
	
}
