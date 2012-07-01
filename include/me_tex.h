#ifndef ME_TEX_H
#define ME_TEX_H
#include "me_util.h"
/*-----------------------------------------------------------*/
/*        */
/*-----------------------------------------------------------*/
color meImageFile(
      uniform string File;
      color defColor;
      uniform float fillOutside;
      uniform float alphaOp;
      /*
      	"No Op" 0
		    "Apply" 1
		    "Multiply" 2
		    "Divide" 3
      */
      uniform string filter;
      /* filter values:
        "box"
		    "triangle"
		    "b-spline"
		    "radial-bspline"
		    "gaussian" 
		    "sinc"
		    "disk"
		  */
      uniform float SFilt;
			uniform float TFilt;
			uniform float lerp;
      point Pt;
      output color colorResult; 
      output float floatResult; 
      )
{
  colorResult = defColor;
  floatResult = 1;
  
  float x = xcomp(Pt);
  float y = ycomp(Pt);
	
  if ( File != "" ) 
  {
		colorResult = color texture(
			File, 
			x,
			y,
			"swidth", SFilt,
			"twidth", TFilt,
			"filter", filter,
			"lerp", lerp );
			
		if ( alphaOp != 0 ) /* "nop" */
		{
			uniform float nChannels = 3;
			textureinfo( File, "channels", nChannels );
			
			if ( nChannels > 3 )
			{
				floatResult = float texture(
							File[3],
							x,
							y,
							"swidth", SFilt,
							"twidth", TFilt,
							"filter", filter,
							"lerp", lerp);
				if ( alphaOp == 2 )
				{
						colorResult *= floatResult;
				}
				if ( alphaOp == 3 ) /* assume AlphaOp == "unassociated" */
				{
					if( floatResult != 0 )
					{
						colorResult /= floatResult;
						colorResult = clamp( colorResult, color(0), color(1) );
					}
				}
			}
				 
			/*	if ( fillOutside  == 1 ) */
			colorResult = mix( defColor, colorResult, floatResult ); 
		}
		if ( ( fillOutside == 1 ) && ( x < 0 || x > 1 || y < 0 || y > 1) )   
				colorResult = defColor;
		} 
		return colorResult;
}
/*-----------------------------------------------------------*/
/*        */
/*-----------------------------------------------------------*/
float meImageFileF(
      uniform string File;
      float defFloatResult;
      uniform float Channel;
      /*
      subtype selector
    	    range { "Red Channel" 0
    		    "Green Channel" 1
    		    "Blue Channel" 2
    		    "Alpha Channel" 3
    		   }
      */
      uniform float Invert;
      uniform string filter;
      /* filter values:
        "box"
		    "triangle"
		    "b-spline"
		    "radial-bspline"
		    "gaussian" 
		    "sinc"
		    "disk"
		  */
      uniform float SFilt;
			uniform float TFilt;
			uniform float Blur;
			uniform float lerp;
      point Pt;
      output float result; 
      )
{
  result = defFloatResult;
  
  float x = xcomp(Pt);
  float y = ycomp(Pt);
	
  if (File != ""   ) {
			result = float texture( 
				File[Channel],
				x, y, 
				"swidth", SFilt,
				"twidth", TFilt,
				"filter", filter,
				"blur", Blur,
				"lerp", lerp
			);
			
	} 
	
	if(Invert != 0) {
			result = 1 - result;
	}
	return result;
}
#endif            
